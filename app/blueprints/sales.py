from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from sqlalchemy import func

# Modelos
from app.models.clients import Cliente
from app.models.products import Producto
from app.models.orders import OrdenVenta, OrdenVentaDetalle
from datetime import datetime

sales_bp = Blueprint('sales', __name__, url_prefix='/ventas')

# --- 1. RUTA PARA CARGAR LA CONSOLA ---
@sales_bp.route('/preventa')
@login_required
def preventa():
    clientes = Cliente.query.all()
    productos_db = Producto.query.filter_by(activo=True).all()
    
    catalogo_js = []
    for p in productos_db:
        catalogo_js.append({
            "id": p.id,
            "sku": p.sku,
            "nombre": p.descripcion,
            "precio": float(p.precio_venta_general)
        })
        
    return render_template('sales/console.html', 
                           clientes=clientes, 
                           catalogo=catalogo_js,
                           date_now=datetime.now().strftime('%Y-%m-%d'))

# --- 2. API INTELIGENTE (CRÉDITO VIRTUAL) ---
@sales_bp.route('/api/cliente/<int:id>')
@login_required
def api_cliente(id):
    c = Cliente.query.get_or_404(id)
    
    # A. Deuda Contable
    deuda_contable = float(c.saldo_actual)

    # B. Deuda Virtual (Pedidos vivos)
    ventas_en_curso = db.session.query(func.sum(OrdenVenta.total_venta))\
        .filter(OrdenVenta.cliente_id == id)\
        .filter(OrdenVenta.estado.in_(['CONFIRMADA', 'EN_RUTA', 'EN_PRODUCCION', 'EMPACADO']))\
        .scalar() or 0.0
    
    ventas_en_curso = float(ventas_en_curso)

    # C. Cálculo
    deuda_total_real = deuda_contable + ventas_en_curso
    limite = float(c.limite_credito)
    disponible_real = limite - deuda_total_real

    precios = {p.producto_id: float(p.valor_descuento) for p in c.precios_especiales}
    
    return jsonify({
        "limite_credito": limite,
        "saldo_actual": deuda_total_real,
        "disponible": disponible_real,
        "precios_especiales": precios
    })

# --- 3. CREAR PEDIDO (PARCHEADO) ---
@sales_bp.route('/crear-pedido', methods=['POST'])
@login_required
def crear_pedido():
    data = request.json
    
    if not data or not data.get('items'):
        return jsonify({"status": "error", "message": "El pedido está vacío"}), 400

    try:
        # 1. VALIDACIÓN DE NOTA
        notas = data.get('notas', '').strip()
        if len(notas) < 15:
            return jsonify({
                "status": "error", 
                "message": "⚠️ Escribe una nota detallada (mínimo 15 letras)."
            }), 400

        # 2. VALIDACIÓN DE CRÉDITO
        if data['metodo_pago'] == 'Credito':
            cliente = Cliente.query.get(int(data['cliente_id']))
            total_pedido = float(data['total'])
            
            ventas_en_curso = db.session.query(func.sum(OrdenVenta.total_venta))\
                .filter(OrdenVenta.cliente_id == cliente.id)\
                .filter(OrdenVenta.estado.in_(['CONFIRMADA', 'EN_RUTA', 'EN_PRODUCCION', 'EMPACADO']))\
                .scalar() or 0.0
            
            deuda_total = float(cliente.saldo_actual) + float(ventas_en_curso)
            
            if (deuda_total + total_pedido) > float(cliente.limite_credito):
                return jsonify({
                    "status": "error", 
                    "message": f"⛔ CRÉDITO INSUFICIENTE. Disp: ${float(cliente.limite_credito) - deuda_total:.2f}"
                }), 400

        # --- GUARDAR VENTA ---
        folio_gen = f"PV-{datetime.now().strftime('%y%m%d%H%M%S')}"

        nueva_orden = OrdenVenta(
            folio = folio_gen,
            cliente_id = int(data['cliente_id']),
            vendedor_id = current_user.id,
            fecha_promesa_entrega = datetime.strptime(data['fecha_entrega'], '%Y-%m-%d'),
            metodo_pago_esperado = data['metodo_pago'],
            total_venta = 0, 
            estado = 'CONFIRMADA',
            notas_vendedor = notas
        )
        
        db.session.add(nueva_orden)
        db.session.flush() 

        total_calculado = 0
        
        for prod_id, info in data['items'].items():
            subtotal = float(info['cant']) * float(info['precio'])
            total_calculado += subtotal
            
            detalle = OrdenVentaDetalle(
                orden_id = nueva_orden.id,
                producto_id = int(prod_id),
                cantidad_pedida = float(info['cant']),
                precio_unitario = float(info['precio']),
                subtotal = subtotal
            )
            db.session.add(detalle)

        # PARCHE: Inicializar Deuda
        nueva_orden.total_venta = total_calculado
        nueva_orden.saldo_pendiente = total_calculado 
        
        db.session.commit()
        
        return jsonify({
            "status": "success", 
            "message": f"Pedido {folio_gen} guardado correctamente.", 
            "folio": folio_gen
        })

    except Exception as e:
        db.session.rollback()
        print(f"Error ventas: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- 4. BANDEJA DE PEDIDOS PORTAL (STAGING) ---
from app.models.portal import SolicitudPedido, SolicitudPedidoDetalle

@sales_bp.route('/portal-pedidos')
@login_required
def portal_pedidos():
    # Solo personal administrativo o con nivel puede ver esto
    if current_user.nivel_usuario < 2:
        flash('No tienes permiso para gestionar pedidos del portal.', 'danger')
        return redirect(url_for('home.dashboard'))
        
    solicitudes = SolicitudPedido.query.order_by(SolicitudPedido.fecha_registro.desc()).all()
    return render_template('sales/portal_inbox.html', solicitudes=solicitudes)

# --- 5. ENVIAR LINK POR WHATSAPP ---
@sales_bp.route('/enviar-whatsapp/<int:solicitud_id>')
@login_required
def enviar_whatsapp(solicitud_id):
    solicitud = SolicitudPedido.query.get_or_404(solicitud_id)
    cliente = solicitud.cliente
    
    # Marcamos como "Pendiente de Cliente" (Paso 2 del flujo)
    if solicitud.estado == 'ESPERANDO_VENDEDOR':
        solicitud.estado = 'PENDIENTE_CLIENTE'
        db.session.commit()
    
    # URL para que el cliente revise (requiere login de portal)
    url_revision = url_for('customer_portal.revisar_pedido', solicitud_id=solicitud.id, _external=True)
    
    mensaje = (
        f"Hola *{cliente.nombre_negocio}*, hemos recibido tu solicitud de pedido en GelMex. "
        f"Por favor, revisa el detalle y confírmalo aquí: {url_revision} . "
        "Una vez que lo confirmes, lo pasaremos a producción."
    )
    
    # Limpiamos el teléfono (asumiendo formato simple)
    telefono = cliente.telefono.replace(' ', '').replace('-', '').replace('+', '') if cliente.telefono else '0000000000'
    if len(telefono) == 10:
        telefono = '52' + telefono 
        
    wa_link = f"https://wa.me/{telefono}?text={mensaje.replace(' ', '%20')}"
    return redirect(wa_link)

# --- 6. CONVERTIR SOLICITUD EN ORDEN REAL ---
@sales_bp.route('/convertir-pedido/<int:solicitud_id>', methods=['POST'])
@login_required
def convertir_pedido(solicitud_id):
    solicitud = SolicitudPedido.query.get_or_404(solicitud_id)
    
    if solicitud.estado != 'CONFIRMADO_CLIENTE':
        flash('La solicitud debe estar confirmada por el cliente antes de procesarla.', 'warning')
        return redirect(url_for('sales.portal_pedidos'))

    try:
        # Generar folio oficial
        folio_oficial = f"PORTAL-V-{datetime.now().strftime('%y%m%d%H%M')}"
        
        # Fecha de entrega mañana por defecto
        from datetime import date, timedelta
        fecha_entrega = date.today() + timedelta(days=1)

        nueva_orden = OrdenVenta(
            folio = folio_oficial,
            cliente_id = solicitud.cliente_id,
            vendedor_id = current_user.id,
            fecha_promesa_entrega = fecha_entrega,
            metodo_pago_esperado = 'Contado', 
            total_venta = float(solicitud.total_estimado),
            saldo_pendiente = float(solicitud.total_estimado),
            estado = 'CONFIRMADA', 
            notas_vendedor = f"SOLICITUD PORTAL {solicitud.folio}. Notas Cliente: {solicitud.notas_cliente}"
        )
        
        db.session.add(nueva_orden)
        db.session.flush()

        for item in solicitud.items:
            detalle = OrdenVentaDetalle(
                orden_id = nueva_orden.id,
                producto_id = item.producto_id,
                cantidad_pedida = item.cantidad,
                precio_unitario = float(item.precio_unitario),
                subtotal = float(item.subtotal)
            )
            db.session.add(detalle)

        # Actualizar estado de la solicitud
        solicitud.estado = 'CONVERTIDO'
        solicitud.notas_vendedor = f"Convertido a Orden {folio_oficial} por {current_user.nombres}"
        
        db.session.commit()
        flash(f'✅ Pedido {folio_oficial} creado con éxito desde la solicitud portal.', 'success')
        
    except Exception as e:
        db.session.rollback()
        print(f"Error al convertir: {e}")
        flash('Error al procesar la conversión del pedido.', 'danger')

    return redirect(url_for('sales.portal_pedidos'))