import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from datetime import datetime
from app.extensions import db
from sqlalchemy import func

# --- IMPORTACIONES ---
from app.models.products import Producto 
from app.models.production import OrdenProduccion
from app.models.stock import InventarioProducto
from app.models.users import Usuario
from app.models.orders import OrdenVenta, OrdenVentaDetalle

production_bp = Blueprint('production', __name__, url_prefix='/produccion')

# --- TABLERO DE NECESIDADES ---
@production_bp.route('/tablero-necesidades')
@login_required
def tablero_necesidades():
    productos = Producto.query.order_by(Producto.descripcion).all()
    data_tablero = []
    
    # Contadores Globales para el Encabezado
    conteo_criticos = 0
    conteo_recuperar = 0

    for p in productos:
        # 1. Existencia Física
        inventarios = InventarioProducto.query.filter_by(producto_id=p.id).all()
        cantidad_fisica = sum(i.cantidad_actual for i in inventarios)

        # 2. Producción en Camino
        ordenes_prod = OrdenProduccion.query.filter(
            OrdenProduccion.producto_id == p.id,
            OrdenProduccion.estatus.in_(['SOLICITADA', 'EN_PRODUCCION', 'BATIENDO'])
        ).all()
        cantidad_produccion = sum(o.cantidad for o in ordenes_prod)

        # 3. Ventas Comprometidas
        ventas_pendientes = db.session.query(func.sum(OrdenVentaDetalle.cantidad_pedida))\
            .join(OrdenVenta)\
            .filter(OrdenVentaDetalle.producto_id == p.id)\
            .filter(OrdenVenta.estado.in_(['CONFIRMADA', 'EN_RUTA']))\
            .scalar() or 0

        # 4. Cálculo Real (MRP)
        stock_disponible_real = cantidad_fisica - ventas_pendientes
        meta = p.stock_ideal if p.stock_ideal else 0
        a_fabricar = meta - (stock_disponible_real + cantidad_produccion)

        # 5. Semáforos y Lógica de Estado
        if a_fabricar <= 0:
            a_fabricar = 0 
            if stock_disponible_real >= meta:
                estado = "SURTIDO"
                clase_estado = "success"
            else:
                estado = "EN CAMINO"
                clase_estado = "info" 
        else:
            if stock_disponible_real <= 0:
                estado = "CRÍTICO"
                clase_estado = "danger"
                conteo_criticos += 1 # Sumamos al contador de alerta
            else:
                estado = "RECUPERAR"
                clase_estado = "warning"
                conteo_recuperar += 1

        data_tablero.append({
            'id': p.id,
            'sku': p.sku,
            'descripcion': p.descripcion,
            'existencia': cantidad_fisica,
            'comprometido': ventas_pendientes,
            'disponible': stock_disponible_real,
            'en_proceso': cantidad_produccion,
            'meta': meta,
            'a_fabricar': a_fabricar,
            'estado': estado,
            'clase_estado': clase_estado
        })

    # --- DATOS PARA EL ENCABEZADO (LO QUE FALTABA) ---
    total_ordenes_activas = OrdenProduccion.query.filter(
        OrdenProduccion.estatus.in_(['SOLICITADA', 'EN_PRODUCCION', 'BATIENDO'])
    ).count()

    # Determinamos el estado global del sistema
    if conteo_criticos > 0:
        estado_global = "ALERTA CRÍTICA"
        clase_global = "danger"
        accion_global = "Producir Urgente"
    elif conteo_recuperar > 0:
        estado_global = "PRECAUCIÓN"
        clase_global = "warning"
        accion_global = "Programar Lotes"
    else:
        estado_global = "ESTABLE"
        clase_global = "success"
        accion_global = "Monitoreo"

    return render_template('production/dashboard.html', 
                           items=data_tablero, 
                           now=datetime.now(),
                           total_ordenes=total_ordenes_activas, # <--- AQUÍ SE ENVÍA EL DATO
                           estado_sys=estado_global,
                           clase_sys=clase_global,
                           accion_sys=accion_global)

# --- CREAR ORDEN ---
@production_bp.route('/crear-orden', methods=['POST'])
@login_required
def crear_orden():
    try:
        producto_id = int(request.form.get('producto_id'))
        cantidad = float(request.form.get('cantidad'))
        
        if cantidad <= 0:
            flash('Cantidad inválida.', 'danger')
            return redirect(url_for('production.tablero_necesidades'))

        orden_existente = OrdenProduccion.query.filter(
            OrdenProduccion.producto_id == producto_id,
            OrdenProduccion.estatus.in_(['SOLICITADA']) 
        ).first()

        if orden_existente:
            flash(f'⚠️ Ya hay orden pendiente ({orden_existente.folio}).', 'warning')
            return redirect(url_for('production.tablero_necesidades'))

        fecha_str = datetime.now().strftime('%Y%m%d')
        nueva_orden = OrdenProduccion(
            folio=f"ORD-{fecha_str}-{producto_id}",
            producto_id=producto_id,
            cantidad=cantidad,
            usuario_solicita_id=current_user.id,
            estatus='SOLICITADA'
        )
        db.session.add(nueva_orden)
        db.session.commit()
        
        # Actualizar folio con ID
        nueva_orden.folio = f"ORD-{fecha_str}-{nueva_orden.id}"
        db.session.commit()

        flash(f'✅ Orden {nueva_orden.folio} enviada.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('production.tablero_necesidades'))

# --- RUTAS MAESTRO HELADERO ---
@production_bp.route('/ordenes-maestro')
@login_required
def ordenes_maestro():
    ordenes = OrdenProduccion.query.filter(
        OrdenProduccion.estatus.in_(['SOLICITADA', 'EN_PRODUCCION', 'BATIENDO'])
    ).order_by(OrdenProduccion.fecha_solicitud.desc()).all()
    return render_template('production/orders_list.html', ordenes=ordenes)

@production_bp.route('/cambiar-estatus/<int:orden_id>/<string:nuevo_estatus>')
@login_required
def cambiar_estatus(orden_id, nuevo_estatus):
    orden = OrdenProduccion.query.get_or_404(orden_id)
    if nuevo_estatus in ['EN_PRODUCCION', 'BATIENDO', 'TERMINADA', 'CANCELADA']:
        orden.estatus = nuevo_estatus
        if nuevo_estatus == 'TERMINADA': orden.fecha_termino = datetime.now()
        db.session.commit()
        flash(f'Estado actualizado a {nuevo_estatus}.', 'success')
    return redirect(url_for('production.ordenes_maestro'))