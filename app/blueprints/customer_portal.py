from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.extensions import db
from app.models.products import Producto
from app.models.clients import Cliente

customer_portal_bp = Blueprint('customer_portal', __name__, url_prefix='/portal')

@customer_portal_bp.route('/catalogo')
def catalog():
    productos = Producto.query.filter_by(activo=True).all()
    
    # Lógica de precios personalizados
    catalogo_precios = []
    cliente_id = session.get('customer_id')
    
    from app.models.clients import PrecioEspecialCliente
    
    for prod in productos:
        precio_final = None # Oculto por defecto
        es_vip = False
        
        if cliente_id:
            # Intentar buscar precio especial
            especial = PrecioEspecialCliente.query.filter_by(
                cliente_id=cliente_id, 
                producto_id=prod.id
            ).first()
            
            if especial:
                precio_final = especial.valor_descuento
                es_vip = True
            else:
                precio_final = prod.precio_venta_general
                es_vip = False
        
        catalogo_precios.append({
            'obj': prod,
            'precio_final': precio_final,
            'es_vip': es_vip
        })
        
    return render_template('customer_portal/catalog.html', items=catalogo_precios)

@customer_portal_bp.route('/acceso', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        negocio = request.form.get('negocio')
        codigo = request.form.get('codigo')
        
        cliente = Cliente.query.filter_by(nombre_negocio=negocio, access_code=codigo, activo=True).first()
        
        if cliente:
            session['customer_id'] = cliente.id
            session['customer_name'] = cliente.nombre_negocio
            flash(f'¡Bienvenido a GelMex, {cliente.nombre_negocio}!', 'success')
            return redirect(url_for('customer_portal.catalog'))
        else:
            flash('Credenciales incorrectas. Por favor verifica tu nombre de negocio y código.', 'danger')
            
    return render_template('customer_portal/login.html')

@customer_portal_bp.route('/salir')
def logout():
    session.pop('customer_id', None)
    session.pop('customer_name', None)
    return redirect(url_for('customer_portal.catalog'))

@customer_portal_bp.route('/pedido', methods=['GET', 'POST'])
def order():
    if 'customer_id' not in session:
        flash('Debes ingresar con tu credencial para realizar pedidos.', 'warning')
        return redirect(url_for('customer_portal.login'))
        
    cliente = Cliente.query.get(session['customer_id'])
    productos = Producto.query.filter_by(activo=True).all()
    
    from app.models.clients import PrecioEspecialCliente
    from app.models.portal import SolicitudPedido, SolicitudPedidoDetalle
    
    # Calcular precios finales para la vista
    productos_con_precio = []
    for prod in productos:
        especial = PrecioEspecialCliente.query.filter_by(
            cliente_id=cliente.id, 
            producto_id=prod.id
        ).first()
        
        precio_final = float(especial.valor_descuento) if especial else float(prod.precio_venta_general)
        es_vip = True if especial else False
        
        productos_con_precio.append({
            'obj': prod,
            'precio_final': precio_final,
            'es_vip': es_vip
        })
    
    if request.method == 'POST':
        # Capturar items del formulario
        items_solicitados = []
        total_estimado = 0
        
        for prod in productos:
            cantidad = request.form.get(f'qty_{prod.id}')
            if cantidad and float(cantidad) > 0:
                especial = PrecioEspecialCliente.query.filter_by(
                    cliente_id=cliente.id, 
                    producto_id=prod.id
                ).first()
                precio_unitario = float(especial.valor_descuento) if especial else float(prod.precio_venta_general)
                
                cant_float = float(cantidad)
                subtotal = cant_float * precio_unitario
                total_estimado += subtotal
                
                items_solicitados.append({
                    'producto_id': prod.id,
                    'cantidad': cant_float,
                    'precio_unitario': precio_unitario,
                    'subtotal': subtotal
                })
        
        if not items_solicitados:
            flash('No has seleccionado ningún producto para tu pedido.', 'danger')
            return redirect(url_for('customer_portal.order'))

        try:
            # Generar Folio para Solicitud
            folio_req = f"REQ-{datetime.now().strftime('%y%m%d%H%M')}-{cliente.id}"
            
            nueva_solicitud = SolicitudPedido(
                folio=folio_req,
                cliente_id=cliente.id,
                estado='ESPERANDO_VENDEDOR', # Primer paso: El vendedor debe verlo
                total_estimado=total_estimado,
                notas_cliente=request.form.get('notas', '')
            )
            
            db.session.add(nueva_solicitud)
            db.session.flush()
            
            for item in items_solicitados:
                detalle = SolicitudPedidoDetalle(
                    solicitud_id=nueva_solicitud.id,
                    producto_id=item['producto_id'],
                    cantidad=item['cantidad'],
                    precio_unitario=item['precio_unitario'],
                    subtotal=item['subtotal']
                )
                db.session.add(detalle)
            
            db.session.commit()
            flash('✅ Tu solicitud de pedido ha sido enviada. Un vendedor de GelMex la revisará y te contactará por WhatsApp para la confirmación final.', 'success')
            return redirect(url_for('customer_portal.catalog'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error al guardar solicitud: {e}")
            flash('Ocurrió un error al procesar tu solicitud. Inténtalo de nuevo.', 'danger')
            return redirect(url_for('customer_portal.order'))
        
    return render_template('customer_portal/order.html', cliente=cliente, productos=productos_con_precio)

# --- REVISIÓN Y CONFIRMACIÓN SEGURA ---
@customer_portal_bp.route('/revisar-pedido/<int:solicitud_id>')
def revisar_pedido(solicitud_id):
    if 'customer_id' not in session:
        flash('Debes iniciar sesión para revisar tu pedido.', 'warning')
        return redirect(url_for('customer_portal.login'))

    from app.models.portal import SolicitudPedido
    solicitud = SolicitudPedido.query.get_or_404(solicitud_id)

    # Seguridad: Solo el dueño del pedido puede verlo
    if solicitud.cliente_id != session['customer_id']:
        flash('No tienes permiso para ver este pedido.', 'danger')
        return redirect(url_for('customer_portal.catalog'))

    return render_template('customer_portal/review_request.html', solicitud=solicitud)

@customer_portal_bp.route('/confirmar-pedido-cliente/<int:solicitud_id>', methods=['POST'])
def confirmar_pedido_cliente(solicitud_id):
    if 'customer_id' not in session:
        return jsonify({"status": "error", "message": "No session"}), 403

    from app.models.portal import SolicitudPedido
    solicitud = SolicitudPedido.query.get_or_404(solicitud_id)

    if solicitud.cliente_id != session['customer_id']:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    try:
        solicitud.estado = 'CONFIRMADO_CLIENTE'
        db.session.commit()
        flash('¡Gracias! Has confirmado tu pedido. Un ejecutivo de GelMex lo procesará de inmediato.', 'success')
        return redirect(url_for('customer_portal.catalog'))
    except Exception as e:
        db.session.rollback()
        flash('Ocurrió un error al confirmar. Por favor contacta a tu vendedor.', 'danger')
        return redirect(url_for('customer_portal.revisar_pedido', solicitud_id=solicitud_id))
