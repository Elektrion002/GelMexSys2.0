import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.extensions import db

# Modelos
from app.models.products import Producto
from app.models.catalogs import CatCategoriaProducto, CatUnidadMedida
from app.models.stock import InventarioProducto
from app.forms import ProductoAdminForm

# Blueprint con nombre ÚNICO para evitar colisiones
product_admin_bp = Blueprint('product_admin', __name__, url_prefix='/admin-productos')

def guardar_foto_producto(file, sku):
    if not file or not file.filename: return None
    filename = secure_filename(f"{sku}_{file.filename}")
    db_path = f"uploads/productos/{filename}"
    save_path = os.path.join(current_app.root_path, 'static', 'uploads', 'productos')
    os.makedirs(save_path, exist_ok=True)
    file.save(os.path.join(save_path, filename))
    return db_path

# --- DASHBOARD GERENCIAL DE PRODUCTOS ---
@product_admin_bp.route('/')
@login_required
def index():
    if current_user.nivel_usuario < 4:
        flash('⛔ Acceso restringido a Gerencia.', 'danger')
        return redirect(url_for('home.dashboard'))

    # Traemos todos los productos (incluso inactivos para gestión)
    productos = Producto.query.order_by(Producto.categoria_id, Producto.descripcion).all()
    
    # Calculamos métricas rápidas para la vista (On-the-fly)
    lista_productos = []
    for p in productos:
        costo = float(p.precio_costo_actual or 0)
        precio = float(p.precio_venta_general or 0)
        margen = precio - costo
        margen_porc = (margen / precio * 100) if precio > 0 else 0
        
        # Sumamos stock real de todas las ubicaciones
        stock_total = sum(i.cantidad_actual for i in p.existencias)

        lista_productos.append({
            'obj': p,
            'margen': margen,
            'margen_porc': margen_porc,
            'stock_total': stock_total
        })

    # OJO: Busca en la carpeta 'product_admin'
    return render_template('product_admin/index.html', productos=lista_productos)

# --- CREAR PRODUCTO MAESTRO ---
@product_admin_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.nivel_usuario < 4: return redirect(url_for('home.dashboard'))

    form = ProductoAdminForm()
    # Cargar Selectores
    form.categoria_id.choices = [(c.id, c.nombre) for c in CatCategoriaProducto.query.all()]
    form.unidad_id.choices = [(u.id, f"{u.nombre} ({u.abreviatura})") for u in CatUnidadMedida.query.all()]

    if form.validate_on_submit():
        sku = form.sku.data.upper().strip()
        
        if Producto.query.filter_by(sku=sku).first():
            flash(f'⚠️ El SKU {sku} ya existe.', 'warning')
        else:
            nuevo = Producto()
            form.populate_obj(nuevo)
            nuevo.sku = sku 
            nuevo.activo = bool(int(form.activo.data)) 

            # Imagen
            if form.imagen_producto.data:
                nuevo.imagen_producto = guardar_foto_producto(form.imagen_producto.data, sku)

            db.session.add(nuevo)
            db.session.commit()
            flash(f'✅ Producto {sku} creado en el Catálogo Maestro.', 'success')
            return redirect(url_for('product_admin.index'))

    return render_template('product_admin/form.html', form=form, title="Alta de Producto Maestro", producto=None)

# --- EDITAR FICHA TÉCNICA ---
@product_admin_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.nivel_usuario < 4: return redirect(url_for('home.dashboard'))

    producto = Producto.query.get_or_404(id)
    form = ProductoAdminForm(obj=producto)
    
    # Cargar Selectores
    form.categoria_id.choices = [(c.id, c.nombre) for c in CatCategoriaProducto.query.all()]
    form.unidad_id.choices = [(u.id, f"{u.nombre} ({u.abreviatura})") for u in CatUnidadMedida.query.all()]

    # Ajuste para el campo Select de Activo
    if request.method == 'GET':
        form.activo.data = 1 if producto.activo else 0

    if form.validate_on_submit():
        ruta_foto_old = producto.imagen_producto
        
        form.populate_obj(producto)
        producto.sku = form.sku.data.upper().strip()
        producto.activo = bool(int(form.activo.data))

        # Gestión de Imagen (Rescate)
        if form.imagen_producto.data and form.imagen_producto.data.filename:
            producto.imagen_producto = guardar_foto_producto(form.imagen_producto.data, producto.sku)
        else:
            producto.imagen_producto = ruta_foto_old

        db.session.commit()
        flash('✅ Ficha Técnica actualizada.', 'success')
        return redirect(url_for('product_admin.index'))

    return render_template('product_admin/form.html', form=form, title="Ingeniería de Producto", producto=producto)