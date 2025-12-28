import os
from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.extensions import db
from datetime import datetime

# Importación de Modelos
from app.models.products import Producto
from app.models.catalogs import CatCategoriaProducto, CatUnidadMedida, CatTipoMovimientoAlmacen
from app.models.stock import InventarioProducto, HistorialMovimiento
from app.models.infrastructure import Almacen, UbicacionAlmacen
from app.forms import ProductoForm 

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventario')

# --- RUTAS DE CATÁLOGO (Index y Nuevo Producto) ---
@inventory_bp.route('/')
@inventory_bp.route('/lista')
@login_required
def index():
    productos = Producto.query.all()
    return render_template('inventory/list.html', productos=productos)

@inventory_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def create():
    form = ProductoForm()
    form.categoria_id.choices = [(c.id, c.nombre) for c in CatCategoriaProducto.query.all()]
    form.unidad_id.choices = [(u.id, u.nombre) for u in CatUnidadMedida.query.all()]

    if form.validate_on_submit():
        sku = form.sku.data.upper()
        if Producto.query.filter_by(sku=sku).first():
            flash(f'Error: El SKU {sku} ya existe.', 'danger')
            return render_template('inventory/form.html', form=form, title="Nuevo Producto")

        filename = None
        if form.imagen.data:
            file = form.imagen.data
            filename = secure_filename(sku + "_" + file.filename)
            upload_path = os.path.join(current_app.root_path, 'static/uploads/productos')
            os.makedirs(upload_path, exist_ok=True)
            file.save(os.path.join(upload_path, filename))
            filename = f"uploads/productos/{filename}"

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
        flash(f'Producto "{nuevo_prod.descripcion}" creado.', 'success')
        return redirect(url_for('inventory.index'))

    return render_template('inventory/form.html', form=form, title="Nuevo Producto")

# --- CONSOLA DE MOVIMIENTOS (ALMACENISTA) ---
@inventory_bp.route('/movimientos', methods=['GET', 'POST'])
@login_required
def movimientos():
    # Cargas para los selectores
    productos = Producto.query.order_by(Producto.descripcion).all()
    almacenes = Almacen.query.all()
    ubicaciones = UbicacionAlmacen.query.all() # Necesario para el filtro de JS
    tipos_movimiento = CatTipoMovimientoAlmacen.query.all()
    
    if request.method == 'POST':
        try:
            # 1. Datos del Formulario
            producto_id = int(request.form.get('producto_id'))
            
            # Validación de Ubicación (Vital)
            ubicacion_id_raw = request.form.get('ubicacion_id')
            if not ubicacion_id_raw:
                flash('Error: Debes seleccionar una ubicación exacta (Pasillo/Rack).', 'danger')
                return redirect(url_for('inventory.movimientos'))
            ubicacion_id = int(ubicacion_id_raw)

            cantidad = float(request.form.get('cantidad'))
            tipo_mov_id = int(request.form.get('tipo_movimiento_id'))
            notas = request.form.get('notas')

            # Obtenemos el objeto del catálogo para saber qué hacer
            tipo_obj = CatTipoMovimientoAlmacen.query.get(tipo_mov_id)
            desc_mov = tipo_obj.descripcion.upper()

            # 2. Buscar Inventario
            stock_record = InventarioProducto.query.filter_by(
                producto_id=producto_id,
                ubicacion_id=ubicacion_id
            ).first()

            saldo_anterior = stock_record.cantidad_actual if stock_record else 0
            
            # Si no existe registro, lo creamos en 0 para operar sobre él
            if not stock_record:
                stock_record = InventarioProducto(
                    producto_id=producto_id,
                    ubicacion_id=ubicacion_id,
                    cantidad_actual=0,
                    fecha_ingreso_almacen=datetime.now()
                )
                db.session.add(stock_record)

            # 3. Lógica de Negocio BLINDADA
            if "INICIAL" in desc_mov: 
                # MODO RESET: Ignora lo que había, pone lo que dices.
                # ESTO CORRIGE TU SALDO NEGATIVO AUTOMÁTICAMENTE
                stock_record.cantidad_actual = cantidad 
                
            elif "ENTRADA" in desc_mov or "DEVOLUCION" in desc_mov or "PRODUCCION" in desc_mov:
                # MODO SUMA
                stock_record.cantidad_actual += cantidad
                
            elif "SALIDA" in desc_mov or "MERMA" in desc_mov or "AJUSTE" in desc_mov:
                # MODO RESTA (Con validación)
                if stock_record.cantidad_actual < cantidad:
                    db.session.rollback()
                    flash(f'⛔ ERROR: No tienes suficiente stock. Tienes {stock_record.cantidad_actual} y quieres sacar {cantidad}.', 'danger')
                    return redirect(url_for('inventory.movimientos'))
                
                stock_record.cantidad_actual -= cantidad

            # 4. Evidencia en Kárdex
            kardex = HistorialMovimiento(
                producto_id=producto_id,
                ubicacion_id=ubicacion_id,
                tipo_movimiento=desc_mov,
                cantidad=cantidad,
                usuario_id=current_user.id,
                fecha=datetime.now(),
                notas=f"{notas} | Saldo: {saldo_anterior} -> {stock_record.cantidad_actual}"
            )
            db.session.add(kardex)
            
            db.session.commit()
            flash(f'✅ Movimiento registrado: {desc_mov}. Nuevo Saldo: {stock_record.cantidad_actual}', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Error técnico: {str(e)}', 'danger')

    return render_template('inventory/movements.html', 
                           productos=productos, 
                           almacenes=almacenes,
                           ubicaciones=ubicaciones,
                           tipos_movimiento=tipos_movimiento,
                           now=datetime.now())