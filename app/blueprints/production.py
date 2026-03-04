import os
import uuid  # <--- CORRECCIÓN CLAVE: Para generar códigos únicos y evitar el error de llave duplicada
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from datetime import datetime
from app.extensions import db
from sqlalchemy import func

# --- IMPORTACIÓN DE MODELOS ---
from app.models.products import Producto 
from app.models.production import OrdenProduccion
from app.models.stock import InventarioProducto
from app.models.users import Usuario
from app.models.orders import OrdenVenta, OrdenVentaDetalle

production_bp = Blueprint('production', __name__, url_prefix='/produccion')

# --- 1. TABLERO DE NECESIDADES (DASHBOARD PRINCIPAL) ---
@production_bp.route('/tablero-necesidades')
@login_required
def tablero_necesidades():
    productos = Producto.query.filter_by(activo=True).order_by(Producto.descripcion).all()
    data_tablero = []
    
    # Contadores para el estado general del sistema
    conteo_criticos = 0
    conteo_recuperar = 0

    for p in productos:
        # A. Existencia Física (Lo que ya está guardado en ubicaciones)
        inventarios = InventarioProducto.query.filter_by(producto_id=p.id).all()
        cantidad_fisica = sum(i.cantidad_actual for i in inventarios)

        # B. En Proceso + En Tránsito (Lo que viene en camino)
        # Sumamos: SOLICITADA (Espera), EN_PRODUCCION/BATIENDO (Cocina), POR_RECIBIR (Puerta Almacén)
        ordenes_activas = OrdenProduccion.query.filter(
            OrdenProduccion.producto_id == p.id,
            OrdenProduccion.estatus.in_(['SOLICITADA', 'EN_PRODUCCION', 'BATIENDO', 'POR_RECIBIR'])
        ).all()
        
        # Si ya se reportó producción real (POR_RECIBIR), usamos ese dato. Si no, usamos lo estimado.
        cantidad_en_camino = 0
        for o in ordenes_activas:
            if o.estatus == 'POR_RECIBIR' and o.cantidad_producida_real > 0:
                cantidad_en_camino += o.cantidad_producida_real
            else:
                cantidad_en_camino += o.cantidad

        # C. Ventas Comprometidas (Lo que ya se vendió pero no ha salido)
        ventas_pendientes = db.session.query(func.sum(OrdenVentaDetalle.cantidad_pedida))\
            .join(OrdenVenta)\
            .filter(OrdenVentaDetalle.producto_id == p.id)\
            .filter(OrdenVenta.estado.in_(['CONFIRMADA', 'EN_RUTA']))\
            .scalar() or 0

        # D. Cálculo MRP (Disponible Real)
        stock_disponible_real = cantidad_fisica - ventas_pendientes
        
        meta = p.stock_ideal if p.stock_ideal else 0
        # Fórmula: Meta - (Lo que tengo libre + Lo que viene en camino)
        a_fabricar = meta - (stock_disponible_real + cantidad_en_camino)

        # E. Semáforos Visuales
        if a_fabricar <= 0:
            a_fabricar = 0 
            if stock_disponible_real >= meta:
                estado = "SURTIDO"
                clase_estado = "success" # Verde
            else:
                estado = "EN CAMINO" # Azul (Ya viene en camino suficiente)
                clase_estado = "info" 
        else:
            if stock_disponible_real <= 0:
                estado = "CRÍTICO" # Debes más de lo que tienes
                clase_estado = "danger"
                conteo_criticos += 1
            else:
                estado = "RECUPERAR" # Hay stock, pero bajo
                clase_estado = "warning"
                conteo_recuperar += 1

        data_tablero.append({
            'id': p.id,
            'sku': p.sku,
            'descripcion': p.descripcion,
            'existencia': cantidad_fisica,
            'comprometido': ventas_pendientes,
            'disponible': stock_disponible_real,
            'en_proceso': cantidad_en_camino,
            'meta': meta,
            'a_fabricar': a_fabricar,
            'estado': estado,
            'clase_estado': clase_estado
        })

    # F. Datos para el Encabezado
    total_ordenes_activas = OrdenProduccion.query.filter(
        OrdenProduccion.estatus.in_(['SOLICITADA', 'EN_PRODUCCION', 'BATIENDO'])
    ).count()

    if conteo_criticos > 0:
        estado_sys = "ALERTA CRÍTICA"
        clase_sys = "danger"
        accion_sys = "Producir Urgente"
    elif conteo_recuperar > 0:
        estado_sys = "PRECAUCIÓN"
        clase_sys = "warning"
        accion_sys = "Programar Lotes"
    else:
        estado_sys = "ESTABLE"
        clase_sys = "success"
        accion_sys = "Monitoreo"

    return render_template('production/dashboard.html', 
                           items=data_tablero, 
                           now=datetime.now(),
                           total_ordenes=total_ordenes_activas, 
                           estado_sys=estado_sys,
                           clase_sys=clase_sys,
                           accion_sys=accion_sys)

# --- 2. CREAR ORDEN (CON SOLUCIÓN DE ERROR 'UNIQUEVIOLATION') ---
@production_bp.route('/crear-orden', methods=['POST'])
@login_required
def crear_orden():
    try:
        producto_id = int(request.form.get('producto_id'))
        cantidad = float(request.form.get('cantidad'))
        
        if cantidad <= 0:
            flash('Error: La cantidad debe ser mayor a 0.', 'danger')
            return redirect(url_for('production.tablero_necesidades'))

        # A. Blindaje Anti-Spam (Si ya hay una solicitada, no duplicar)
        orden_existente = OrdenProduccion.query.filter(
            OrdenProduccion.producto_id == producto_id,
            OrdenProduccion.estatus.in_(['SOLICITADA']) 
        ).first()

        if orden_existente:
            flash(f'⚠️ Ya existe una orden pendiente ({orden_existente.folio}).', 'warning')
            return redirect(url_for('production.tablero_necesidades'))

        # B. Generación de Folio Único (SOLUCIÓN DEFINITIVA)
        # Usamos UUID para asegurar que NUNCA se repita, ni aunque borres la BD.
        # Formato: ORD-YYMMDD-IDPROD-XXXX (4 caracteres aleatorios)
        suffix = uuid.uuid4().hex[:4].upper()
        fecha_str = datetime.now().strftime('%y%m%d')
        folio_unico = f"ORD-{fecha_str}-{producto_id}-{suffix}"
        
        nueva_orden = OrdenProduccion(
            folio=folio_unico,
            producto_id=producto_id,
            cantidad=cantidad,
            usuario_solicita_id=current_user.id,
            fecha_solicitud=datetime.now(),
            estatus='SOLICITADA',
            prioridad='NORMAL'
        )

        db.session.add(nueva_orden)
        db.session.commit()
        
        flash(f'✅ Orden {nueva_orden.folio} enviada correctamente.', 'success')

    except Exception as e:
        db.session.rollback()
        print(f"ERROR PRODUCCION: {str(e)}")
        flash(f'❌ Error al crear orden: {str(e)}', 'danger')

    return redirect(url_for('production.tablero_necesidades'))

# --- 3. VISTA DEL MAESTRO HELADERO ---
@production_bp.route('/ordenes-maestro')
@login_required
def ordenes_maestro():
    # Mostramos lo nuevo y lo que se está cocinando
    ordenes = OrdenProduccion.query.filter(
        OrdenProduccion.estatus.in_(['SOLICITADA', 'EN_PRODUCCION', 'BATIENDO'])
    ).order_by(OrdenProduccion.estatus.asc(), OrdenProduccion.fecha_solicitud.asc()).all()
    
    return render_template('production/orders_list.html', ordenes=ordenes)

# --- 4. CAMBIAR ESTATUS (SOLO INICIO) ---
@production_bp.route('/cambiar-estatus/<int:orden_id>/<string:nuevo_estatus>')
@login_required
def cambiar_estatus(orden_id, nuevo_estatus):
    orden = OrdenProduccion.query.get_or_404(orden_id)
    
    # Solo permitimos iniciar la producción aquí. El cierre se hace por el modal.
    if nuevo_estatus == 'BATIENDO':
        orden.estatus = 'BATIENDO'
        orden.fecha_inicio = datetime.now()
        db.session.commit()
        flash(f'🔥 Lote {orden.folio} iniciado. ¡A cocinar!', 'info')
    
    return redirect(url_for('production.ordenes_maestro'))

# --- 5. REPORTAR PRODUCCIÓN REAL (CIERRE DE LOTE) ---
@production_bp.route('/reportar-produccion', methods=['POST'])
@login_required
def reportar_produccion_real():
    try:
        orden_id = int(request.form.get('orden_id'))
        cantidad_real = float(request.form.get('cantidad_real'))
        notas = request.form.get('notas')

        orden = OrdenProduccion.query.get_or_404(orden_id)
        
        # Guardamos la realidad operativa
        orden.cantidad_producida_real = cantidad_real
        orden.notas_produccion = notas
        orden.fecha_termino = datetime.now()
        
        # CAMBIO IMPORTANTE:
        # No ponemos 'TERMINADA' todavía. Ponemos 'POR_RECIBIR'.
        # Esto envía la orden a la "puerta del almacén" para que el Almacenista la cuente.
        orden.estatus = 'POR_RECIBIR'
        
        db.session.commit()
        
        flash(f'✅ Lote enviado a Almacén. Reportaste {cantidad_real} piezas. Pendiente de recepción.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error al reportar producción: {str(e)}', 'danger')

    return redirect(url_for('production.ordenes_maestro'))