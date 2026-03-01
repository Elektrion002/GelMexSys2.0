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
    
    # Calcular precios finales para el pedido
    productos_con_precio = []
    for prod in productos:
        especial = PrecioEspecialCliente.query.filter_by(
            cliente_id=cliente.id, 
            producto_id=prod.id
        ).first()
        
        precio_final = especial.valor_descuento if especial else prod.precio_venta_general
        es_vip = True if especial else False
        
        productos_con_precio.append({
            'obj': prod,
            'precio_final': precio_final,
            'es_vip': es_vip
        })
    
    if request.method == 'POST':
        # Aquí iría la lógica para procesar el pedido
        flash('Tu pedido ha sido enviado con éxito. Un ejecutivo de GelMex se comunicará contigo.', 'success')
        return redirect(url_for('customer_portal.catalog'))
        
    return render_template('customer_portal/order.html', cliente=cliente, productos=productos_con_precio)
