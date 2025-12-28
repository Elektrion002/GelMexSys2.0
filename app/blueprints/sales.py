from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from sqlalchemy import func # <--- NECESARIO PARA SUMAR

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
    productos_db = Producto.query.all()
    
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

# --- 2. API INTELIGENTE (AQUÍ ESTÁ LA MAGIA DEL CRÉDITO) ---
@sales_bp.route('/api/cliente/<int:id>')
@login_required
def api_cliente(id):
    c = Cliente.query.get_or_404(id)
    
    # A. Deuda "Dura" (Lo que ya se entregó y no ha pagado)
    deuda_contable = float(c.saldo_actual)

    # B. Deuda "Virtual" (Pedidos en vuelo: Confirmados o En Ruta, pero no entregados)
    # Buscamos todas las ventas activas de este cliente que aún no se cobran
    ventas_en_curso = db.session.query(func.sum(OrdenVenta.total_venta))\
        .filter(OrdenVenta.cliente_id == id)\
        .filter(OrdenVenta.estado.in_(['CONFIRMADA', 'EN_RUTA', 'EN_PRODUCCION', 'EMPACADO']))\
        .scalar() or 0.0
    
    ventas_en_curso = float(ventas_en_curso)

    # C. Cálculo Real
    deuda_total_real = deuda_contable + ventas_en_curso
    limite = float(c.limite_credito)
    disponible_real = limite - deuda_total_real

    # Precios especiales
    precios = {p.producto_id: float(p.valor_descuento) for p in c.precios_especiales}
    
    return jsonify({
        "limite_credito": limite,
        "saldo_actual": deuda_total_real, # Le mandamos la suma total para asustar a Don Pepe
        "disponible": disponible_real,
        "precios_especiales": precios,
        # Dato extra por si quieres depurar después:
        "desglose_deuda": {
            "contable": deuda_contable,
            "en_pedidos": ventas_en_curso
        }
    })

# --- 3. EL "OÍDO" QUE RECIBE EL PEDIDO ---
@sales_bp.route('/crear-pedido', methods=['POST'])
@login_required
def crear_pedido():
    data = request.json
    
    if not data or not data.get('items'):
        return jsonify({"status": "error", "message": "El pedido está vacío"}), 400

    try:
        # VALIDACIÓN FINAL DE CRÉDITO (DOBLE SEGURIDAD)
        if data['metodo_pago'] == 'Credito':
            cliente = Cliente.query.get(int(data['cliente_id']))
            total_pedido = float(data['total'])
            
            # Recalculamos rápido para que no nos hagan trampa
            ventas_en_curso = db.session.query(func.sum(OrdenVenta.total_venta))\
                .filter(OrdenVenta.cliente_id == cliente.id)\
                .filter(OrdenVenta.estado.in_(['CONFIRMADA', 'EN_RUTA', 'EN_PRODUCCION', 'EMPACADO']))\
                .scalar() or 0.0
            
            deuda_total = float(cliente.saldo_actual) + float(ventas_en_curso)
            
            if (deuda_total + total_pedido) > float(cliente.limite_credito):
                return jsonify({
                    "status": "error", 
                    "message": f"⛔ CRÉDITO INSUFICIENTE. Disponible real: ${float(cliente.limite_credito) - deuda_total:.2f}"
                }), 400

        # --- CREACIÓN DEL PEDIDO ---
        folio_gen = f"PV-{datetime.now().strftime('%y%m%d%H%M%S')}"

        nueva_orden = OrdenVenta(
            folio = folio_gen,
            cliente_id = int(data['cliente_id']),
            vendedor_id = current_user.id,
            fecha_promesa_entrega = datetime.strptime(data['fecha_entrega'], '%Y-%m-%d'),
            metodo_pago_esperado = data['metodo_pago'],
            total_venta = 0, 
            estado = 'CONFIRMADA' # Nace confirmada para que descuente crédito y aparezca en producción
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

        nueva_orden.total_venta = total_calculado
        db.session.commit()
        
        return jsonify({
            "status": "success", 
            "message": f"Pedido {folio_gen} guardado! Crédito actualizado.", 
            "folio": folio_gen
        })

    except Exception as e:
        db.session.rollback()
        print(f"Error ventas: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500