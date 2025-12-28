# app/blueprints/inventory.py
import os
from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.products import Producto
from app.models.catalogs import CatCategoriaProducto, CatUnidadMedida
from app.forms import ProductoForm # <--- Importamos el formulario nuevo

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventario')

@inventory_bp.route('/')
@inventory_bp.route('/lista')
@login_required
def index():
    productos = Producto.query.all()
    return render_template('inventory/list.html', productos=productos)

# --- NUEVA RUTA: CREAR PRODUCTO ---
@inventory_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def create():
    form = ProductoForm()
    
    # 1. Cargar los combos (Selects) con datos de la BD
    form.categoria_id.choices = [(c.id, c.nombre) for c in CatCategoriaProducto.query.all()]
    form.unidad_id.choices = [(u.id, u.nombre) for u in CatUnidadMedida.query.all()]

    if form.validate_on_submit():
        # 2. Lógica para guardar
        sku = form.sku.data.upper() # Siempre mayúsculas
        
        # Validar que no exista el SKU
        if Producto.query.filter_by(sku=sku).first():
            flash(f'Error: El SKU {sku} ya existe.', 'danger')
            return render_template('inventory/form.html', form=form, title="Nuevo Producto")

        # Manejo de Imagen
        filename = None
        if form.imagen.data:
            file = form.imagen.data
            filename = secure_filename(sku + "_" + file.filename)
            # Guardar en app/static/uploads/productos
            upload_path = os.path.join(current_app.root_path, 'static/uploads/productos')
            os.makedirs(upload_path, exist_ok=True)
            file.save(os.path.join(upload_path, filename))
            # Guardamos la ruta relativa para la BD
            filename = f"uploads/productos/{filename}"

        # Crear Objeto
        nuevo_prod = Producto(
            sku=sku,
            descripcion=form.descripcion.data,
            categoria_id=form.categoria_id.data,
            unidad_id=form.unidad_id.data,
            precio_costo_actual=form.precio_costo.data,
            precio_venta_general=form.precio_venta.data,
            stock_minimo=form.stock_minimo.data,
            imagen_producto=filename
        )

        db.session.add(nuevo_prod)
        db.session.commit()
        
        flash(f'Producto "{nuevo_prod.descripcion}" creado exitosamente.', 'success')
        return redirect(url_for('inventory.index'))

    return render_template('inventory/form.html', form=form, title="Nuevo Producto")