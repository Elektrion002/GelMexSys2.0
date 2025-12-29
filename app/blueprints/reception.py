from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app.extensions import db

# Importación de Modelos
from app.models.production import OrdenProduccion
from app.models.stock import InventarioProducto, HistorialMovimiento
from app.models.infrastructure import UbicacionAlmacen, Almacen 

reception_bp = Blueprint('reception', __name__, url_prefix='/recepcion')

# --- 1. TABLERO DE RECEPCIÓN ---
@reception_bp.route('/')
@login_required
def index():
    # Filtramos las órdenes activas (POR_RECIBIR)
    lotes_activos = OrdenProduccion.query.filter(
        OrdenProduccion.estatus.in_(['POR_RECIBIR'])
    ).all()
    
    # Traemos AMBOS catálogos para el filtro en cascada
    almacenes = Almacen.query.order_by(Almacen.descripcion).all()
    ubicaciones = UbicacionAlmacen.query.order_by(UbicacionAlmacen.codigo).all()
    
    # Renderizamos la vista con nombre ÚNICO
    return render_template('reception/reception_dock.html', 
                           lotes=lotes_activos, 
                           almacenes=almacenes,
                           ubicaciones=ubicaciones)

# --- 2. PROCESAR EL INGRESO ---
@reception_bp.route('/confirmar', methods=['POST'])
@login_required
def confirmar():
    try:
        orden_id = int(request.form.get('orden_id'))
        # Recibimos el ID de la ubicación exacta (dropdown hijo)
        ubicacion_id = int(request.form.get('ubicacion_id'))
        cantidad_ingresar = float(request.form.get('cantidad_ingresar'))
        forzar_cierre = request.form.get('forzar_cierre') == 'on'
        # Capturamos las notas del usuario
        notas_usuario = request.form.get('notas', '').strip()
        
        orden = OrdenProduccion.query.get_or_404(orden_id)
        
        # Validaciones
        if cantidad_ingresar < 0:
            flash('No puedes ingresar cantidades negativas.', 'warning')
            return redirect(url_for('reception.index'))

        # Solo permitimos 0 si se está cerrando la orden (Merma total del resto)
        if cantidad_ingresar == 0 and not forzar_cierre:
            flash('Si la cantidad es 0, debes marcar "Cerrar Orden" para indicar merma.', 'warning')
            return redirect(url_for('reception.index'))

        # A. ACTUALIZAR STOCK FÍSICO (Solo si hay cantidad > 0)
        if cantidad_ingresar > 0:
            inventario = InventarioProducto.query.filter_by(
                producto_id=orden.producto_id, 
                ubicacion_id=ubicacion_id
            ).first()

            if inventario:
                inventario.cantidad_actual += cantidad_ingresar
            else:
                nuevo_inv = InventarioProducto(
                    producto_id=orden.producto_id,
                    ubicacion_id=ubicacion_id,
                    cantidad_actual=cantidad_ingresar,
                    fecha_ingreso_almacen=datetime.now()
                )
                db.session.add(nuevo_inv)

        # B. ACTUALIZAR EL ACUMULADO DE LA ORDEN
        acumulado_previo = orden.cantidad_recibida_almacen or 0
        nuevo_acumulado = acumulado_previo + cantidad_ingresar
        orden.cantidad_recibida_almacen = nuevo_acumulado
        
        # C. GENERAR EVIDENCIA (KÁRDEX) CON NOTAS
        texto_historial = f"Ingreso ({cantidad_ingresar}). Acumulado: {nuevo_acumulado}/{orden.cantidad_producida_real}."
        if notas_usuario:
            texto_historial += f" | NOTA: {notas_usuario}"

        movimiento = HistorialMovimiento(
            producto_id=orden.producto_id,
            ubicacion_id=ubicacion_id,
            tipo_movimiento='ENTRADA_PRODUCCION',
            cantidad=cantidad_ingresar,
            usuario_id=current_user.id,
            fecha=datetime.now(),
            referencia=orden.folio,
            notas=texto_historial
        )
        db.session.add(movimiento)

        # D. LÓGICA DE CIERRE (Superávit, Exacto o Merma)
        diferencia = orden.cantidad_producida_real - nuevo_acumulado
        
        # CASO 1: SUPERÁVIT (Sobrante positivo, diferencia negativa)
        if diferencia < -0.001:
            orden.estatus = 'TERMINADA'
            orden.fecha_termino = datetime.now()
            orden.notas_produccion = (orden.notas_produccion or "") + f" | SUPERÁVIT ALMACÉN: {abs(diferencia)} pzas extra."
            flash(f"✅ Lote completado con EXCEDENTE de {abs(diferencia)} pzas.", 'success')
            
        # CASO 2: EXACTO
        elif abs(diferencia) <= 0.001:
            orden.estatus = 'TERMINADA'
            orden.fecha_termino = datetime.now()
            flash(f"✅ Lote {orden.folio} completado exacto.", 'success')
            
        # CASO 3: FALTANTE (MERMA) CON CIERRE FORZADO
        elif forzar_cierre:
            orden.estatus = 'TERMINADA'
            orden.fecha_termino = datetime.now()
            
            nota_cierre = f" | FALTANTE (MERMA): {diferencia}."
            if notas_usuario:
                nota_cierre += f" Causa: {notas_usuario}"
            
            orden.notas_produccion = (orden.notas_produccion or "") + nota_cierre
            flash(f"⚠️ Orden cerrada con faltante de {diferencia} pzas.", 'warning')
            
        # CASO 4: PARCIAL (Sigue abierta)
        else:
            flash(f"📥 Ingreso parcial guardado. Faltan {diferencia} pzas.", 'info')

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error técnico: {str(e)}', 'danger')

    return redirect(url_for('reception.index'))