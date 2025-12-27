# app/blueprints/inventory.py
from flask import Blueprint, render_template
from flask_login import login_required
from app.models.products import Producto

# Definimos el Blueprint
inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventario')

@inventory_bp.route('/')
@inventory_bp.route('/lista')
@login_required
def index():
    # 1. Consultar todos los productos de la BD
    #    (SQLAlchemy hace: SELECT * FROM productos)
    productos = Producto.query.all()
    
    # 2. Enviarlos a la vista (HTML)
    return render_template('inventory/list.html', productos=productos)