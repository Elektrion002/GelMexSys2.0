from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.extensions import db
from app.models.products import Producto
from app.models.clients import Cliente

customer_portal_bp = Blueprint('customer_portal', __name__, url_prefix='/portal')

@customer_portal_bp.route('/catalogo')
def catalog():
    # Solo mostramos productos activos
    productos = Producto.query.filter_by(activo=True).all()
    return render_template('customer_portal/catalog.html', productos=productos)

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
    
    if request.method == 'POST':
        # Aquí iría la lógica para procesar el pedido (crear registro en BD)
        flash('Tu pedido ha sido enviado con éxito. Un ejecutivo de GelMex se comunicará contigo.', 'success')
        return redirect(url_for('customer_portal.catalog'))
        
    return render_template('customer_portal/order.html', cliente=cliente, productos=productos)
