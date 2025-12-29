from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app.extensions import db
from sqlalchemy import desc

# Modelos
from app.models.orders import OrdenVenta, OrdenVentaDetalle
from app.models.stock import InventarioProducto, HistorialMovimiento
from app.models.infrastructure import UbicacionAlmacen, Almacen
from app.models.shipping import OrdenPaquete

shipping_bp = Blueprint('shipping', __name__, url_prefix='/envios')

# --- 1. DASHBOARD DE SURTIDO ---
@shipping_bp.route('/')
@login_required
def index():
    # 1. PEDIDOS ACTIVOS (Pendientes de trabajo)
    pendientes = OrdenVenta.query.filter(
        OrdenVenta.estado.in_(['CONFIRMADA', 'EN_PRODUCCION', 'EMPACADO'])
    ).order_by(OrdenVenta.fecha_promesa_entrega.asc()).all()
    
    # 2. PEDIDOS LISTOS (Historial reciente para referencia)
    terminados = OrdenVenta.query.filter(
        OrdenVenta.estado.in_(['LISTO_RUTA', 'EN_RUTA'])
    ).order_by(desc(OrdenVenta.fecha_promesa_entrega)).limit(10).all()
    
    return render_template('shipping/dashboard.html', pendientes=pendientes, terminados=terminados)

# --- 2. PANTALLA DE TRABAJO (PICKING) ---
@shipping_bp.route('/surtir/<int:orden_id>')
@login_required
def picking(orden_id):
    orden = OrdenVenta.query.get_or_404(orden_id)
    ids_productos = [item.producto_id for item in orden.items]
    
    # Consulta de Stock optimizada para evitar errores de ORM
    stock_data = db.session.query(InventarioProducto, UbicacionAlmacen, Almacen)\
        .select_from(InventarioProducto)\
        .join(UbicacionAlmacen, InventarioProducto.ubicacion_id == UbicacionAlmacen.id)\
        .join(Almacen, UbicacionAlmacen.almacen_id == Almacen.id)\
        .filter(InventarioProducto.producto_id.in_(ids_productos))\
        .filter(InventarioProducto.cantidad_actual > 0)\
        .order_by(Almacen.descripcion, UbicacionAlmacen.codigo)\
        .all()

    # Estructuramos datos para los Comboboxes (Selectores)
    stock_por_producto = {}
    for inv, ubi, alm in stock_data:
        if inv.producto_id not in stock_por_producto:
            stock_por_producto[inv.producto_id] = []
        stock_por_producto[inv.producto_id].append({
            'inv_id': inv.id,
            'almacen_id': alm.id,
            'almacen_nombre': alm.descripcion,
            'ubicacion_codigo': ubi.codigo,
            'cantidad': int(inv.cantidad_actual)
        })
    
    return render_template('shipping/picking.html', orden=orden, stock_por_producto=stock_por_producto)

# --- 3. CONFIRMAR PICKING (CON CANDADO DE SEGURIDAD) ---
@shipping_bp.route('/confirmar-picking', methods=['POST'])
@login_required
def confirmar_picking():
    try:
        detalle_id = int(request.form.get('detalle_id'))
        inventario_id = int(request.form.get('inventario_id')) 
        cantidad = float(request.form.get('cantidad'))
        
        detalle = OrdenVentaDetalle.query.get_or_404(detalle_id)
        
        # --- CANDADO DE SEGURIDAD ---
        # Si la orden ya está cerrada, impedimos cualquier movimiento
        if detalle.orden.estado in ['LISTO_RUTA', 'EN_RUTA', 'ENTREGADA', 'CANCELADA']:
            flash('⛔ ACCIÓN DENEGADA: Esta orden ya fue finalizada. No se puede modificar el inventario.', 'danger')
            return redirect(url_for('shipping.picking', orden_id=detalle.orden_id))
        # ----------------------------

        inv = InventarioProducto.query.get(inventario_id)
        
        # Validaciones de Inventario
        if not inv:
            flash('❌ Error: El registro de inventario ya no existe o cambió.', 'danger')
            return redirect(url_for('shipping.picking', orden_id=detalle.orden_id))
            
        if inv.cantidad_actual < cantidad:
            flash(f'❌ Stock Insuficiente: Solo quedan {inv.cantidad_actual} pzas disponibles ahí.', 'danger')
            return redirect(url_for('shipping.picking', orden_id=detalle.orden_id))
            
        # 1. Ejecutar Descuento (Salida de Almacén)
        inv.cantidad_actual -= cantidad
        
        # 2. Actualizar Detalle Orden
        detalle.cantidad_surtida = (detalle.cantidad_surtida or 0) + cantidad
        
        # 3. Registrar en Kárdex
        mov = HistorialMovimiento(
            producto_id=detalle.producto_id,
            ubicacion_id=inv.ubicacion_id,
            tipo_movimiento='SALIDA_VENTA',
            cantidad=cantidad,
            usuario_id=current_user.id,
            fecha=datetime.now(),
            referencia=f"Pedido {detalle.orden.folio}",
            notas=f"Surtido para: {detalle.orden.cliente.nombre_negocio}"
        )
        db.session.add(mov)
        
        # Actualizar estado si es el primer movimiento
        if detalle.orden.estado == 'CONFIRMADA':
            detalle.orden.estado = 'EN_PRODUCCION'
            
        db.session.commit()
        flash(f'✅ Tomadas {cantidad} pzas correctamente.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error técnico: {str(e)}', 'danger')
        
    return redirect(url_for('shipping.picking', orden_id=detalle.orden_id))

# --- 4. GENERAR ETIQUETAS MASIVAS (CON CANDADO) ---
@shipping_bp.route('/generar-etiquetas', methods=['POST'])
@login_required
def generar_etiquetas():
    try:
        orden_id = int(request.form.get('orden_id'))
        total_cajas = int(request.form.get('total_cajas'))
        contenido = request.form.get('contenido', '')
        
        orden = OrdenVenta.query.get_or_404(orden_id)
        
        # --- CANDADO DE SEGURIDAD ---
        if orden.estado in ['LISTO_RUTA', 'EN_RUTA', 'ENTREGADA', 'CANCELADA']:
            flash('⛔ ERROR: La orden está cerrada. Solo puedes reimprimir etiquetas, no generar nuevas.', 'danger')
            return redirect(url_for('shipping.picking', orden_id=orden.id))
        # ----------------------------

        # Limpiar etiquetas previas para regenerar
        OrdenPaquete.query.filter_by(orden_id=orden.id).delete()
        
        ruta_str = orden.cliente.ruta.descripcion.split(':')[0] if orden.cliente.ruta else "SR"
        folio_clean = orden.folio.replace('PV-', '')
        
        for i in range(1, total_cajas + 1):
            # Formato QR: #FOLIO_RUTA_CajaX/Y
            codigo_qr = f"#{folio_clean}_{ruta_str}_C{i}/{total_cajas}"
            
            paq = OrdenPaquete(
                orden_id=orden.id,
                codigo_etiqueta=codigo_qr,
                numero_caja=i,
                total_cajas_orden=total_cajas,
                descripcion_contenido=contenido if contenido else f"Caja {i} de {total_cajas}",
                creado_por_id=current_user.id
            )
            db.session.add(paq)
        
        orden.estado = 'EMPACADO'
        db.session.commit()
        
        flash(f'✅ {total_cajas} etiquetas de caja generadas.', 'success')
        return redirect(url_for('shipping.imprimir_etiquetas', orden_id=orden.id))

    except Exception as e:
        db.session.rollback()
        flash(f'Error generando etiquetas: {str(e)}', 'danger')
        return redirect(url_for('shipping.picking', orden_id=orden_id))

# --- 5. VISTA DE IMPRESIÓN (SIN CANDADO, SIEMPRE ACCESIBLE) ---
@shipping_bp.route('/imprimir/<int:orden_id>')
@login_required
def imprimir_etiquetas(orden_id):
    orden = OrdenVenta.query.get_or_404(orden_id)
    return render_template('shipping/labels.html', orden=orden)

# --- 6. GENERAR CAJA MANUAL (CON CANDADO) ---
@shipping_bp.route('/generar-caja', methods=['POST'])
@login_required
def generar_caja():
    try:
        orden_id = int(request.form.get('orden_id'))
        num_caja = int(request.form.get('num_caja'))
        total_cajas = int(request.form.get('total_cajas'))
        contenido = request.form.get('contenido')
        
        orden = OrdenVenta.query.get_or_404(orden_id)

        # --- CANDADO DE SEGURIDAD ---
        if orden.estado in ['LISTO_RUTA', 'EN_RUTA', 'ENTREGADA', 'CANCELADA']:
            flash('⛔ ERROR: Orden cerrada.', 'danger')
            return redirect(url_for('shipping.picking', orden_id=orden.id))
        # ----------------------------

        codigo = f"PAQ-{orden.folio}-C{num_caja}"
        
        paq = OrdenPaquete(
            orden_id=orden.id,
            codigo_etiqueta=codigo,
            numero_caja=num_caja,
            total_cajas_orden=total_cajas,
            descripcion_contenido=contenido,
            creado_por_id=current_user.id
        )
        db.session.add(paq)
        
        if num_caja == total_cajas:
            orden.estado = 'EN_RUTA' # Opcional, o esperar a finalizar
        else:
            orden.estado = 'EMPACADO'
            
        db.session.commit()
        flash(f'📦 Caja {num_caja} registrada.', 'info')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
        
    return redirect(url_for('shipping.picking', orden_id=orden_id))

# --- 7. FINALIZAR ORDEN (CIERRE DEFINITIVO) ---
@shipping_bp.route('/finalizar/<int:orden_id>', methods=['POST'])
@login_required
def finalizar_orden(orden_id):
    try:
        orden = OrdenVenta.query.get_or_404(orden_id)
        
        # Si ya estaba cerrada, no hacemos nada (idempotencia)
        if orden.estado == 'LISTO_RUTA':
            flash('Esta orden ya estaba finalizada.', 'info')
            return redirect(url_for('shipping.index'))

        if not orden.paquetes:
            flash('⚠️ Advertencia: Finalizaste la orden sin generar etiquetas de caja.', 'warning')
            
        orden.estado = 'LISTO_RUTA'
        db.session.commit()
        
        flash(f'🚀 Orden {orden.folio} finalizada correctamente y enviada a Logística.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al finalizar: {str(e)}', 'danger')
        
    return redirect(url_for('shipping.index'))