from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from sqlalchemy import func
from app.extensions import db

# Modelos
from app.models.orders import OrdenVenta, OrdenVentaDetalle
from app.models.payments import Pago
from app.models.clients import Cliente
# Importamos el catálogo real basado en tu archivo models/catalogs.py
from app.models.catalogs import CatTipoMovimientoFinanzas 

logistics_bp = Blueprint('logistics', __name__, url_prefix='/logistica')

# --- 1. DASHBOARD DE RUTA ---
@logistics_bp.route('/')
@login_required
def index():
    # A. Pendientes (Lo que falta entregar)
    pendientes = OrdenVenta.query.filter(
        OrdenVenta.estado.in_(['LISTO_RUTA', 'EN_RUTA'])
    ).order_by(OrdenVenta.fecha_promesa_entrega.asc()).all()

    # B. Historial Reciente (Últimas 10 sin importar fecha para que no se pierdan)
    terminadas = OrdenVenta.query.filter(
        OrdenVenta.estado.in_(['ENTREGADA', 'PAGADO'])
    ).order_by(OrdenVenta.id.desc()).limit(10).all()

    return render_template('logistics/route_dashboard.html', 
                           ordenes=pendientes, 
                           terminadas=terminadas)

# --- 2. CARGAR AL CAMIÓN ---
@logistics_bp.route('/cargar/<int:orden_id>')
@login_required
def cargar_orden(orden_id):
    orden = OrdenVenta.query.get_or_404(orden_id)
    if orden.estado == 'LISTO_RUTA':
        orden.estado = 'EN_RUTA'
        db.session.commit()
        flash(f'📦 Orden {orden.folio} cargada.', 'success')
    return redirect(url_for('logistics.index'))

# --- 3. PANTALLA DE CONTRA-ENTREGA (CARGA DINÁMICA) ---
@logistics_bp.route('/entrega/<int:orden_id>')
@login_required
def entrega_cliente(orden_id):
    orden = OrdenVenta.query.get_or_404(orden_id)
    
    # 1. TRAER CATÁLOGO DE PAGOS DE LA BD (Sin hardcodeo)
    # Usamos 'activo' porque hereda de CatalogoBase
    metodos_pago = CatTipoMovimientoFinanzas.query.filter_by(activo=True).all()
    
    # 2. Deuda Histórica Global
    deuda_historica = float(orden.cliente.saldo_actual or 0)
    
    # Ventas en curso (excluyendo la actual)
    ventas_en_curso = db.session.query(func.sum(OrdenVenta.total_venta))\
        .filter(OrdenVenta.cliente_id == orden.cliente_id)\
        .filter(OrdenVenta.id != orden.id)\
        .filter(OrdenVenta.estado.in_(['CONFIRMADA', 'EN_RUTA', 'EN_PRODUCCION', 'EMPACADO', 'ENTREGADA']))\
        .scalar() or 0.0
    
    saldo_global_previo = deuda_historica + float(ventas_en_curso)

    # 3. Preparar Items y AYUDA VISUAL (Total Piezas)
    items_data = []
    total_piezas_bajar = 0
    
    for item in orden.items:
        # Lógica: Entregar lo surtido. Si no hay surtido, lo pedido.
        cant_sugerida = item.cantidad_surtida if item.cantidad_surtida > 0 else item.cantidad_pedida
        total_piezas_bajar += cant_sugerida
        
        items_data.append({
            'detalle_id': item.id,
            'producto': item.producto.descripcion,
            'sku': item.producto.sku,
            'pedida': item.cantidad_pedida,
            'surtida': item.cantidad_surtida,
            'precio': float(item.precio_unitario),
            'sugerida': cant_sugerida
        })
        
    return render_template('logistics/delivery_handover.html', 
                           orden=orden, 
                           items=items_data,
                           total_piezas=total_piezas_bajar, # Dato para la ayuda visual
                           saldo_global_previo=saldo_global_previo,
                           metodos_pago=metodos_pago) # <--- AQUÍ VA EL CATÁLOGO

# --- 4. PROCESAR ENTREGA ---
@logistics_bp.route('/confirmar-entrega', methods=['POST'])
@login_required
def confirmar_entrega():
    try:
        data = request.json
        orden_id = data.get('orden_id')
        items_ajuste = data.get('items') 
        info_pago = data.get('pago')     
        notas = data.get('notas')

        orden = OrdenVenta.query.get_or_404(orden_id)
        
        # 1. Ajuste de Inventario / Total
        nuevo_total_venta = 0
        for item_data in items_ajuste:
            detalle = OrdenVentaDetalle.query.get(int(item_data['detalle_id']))
            cant_real = float(item_data['cant_real'])
            
            detalle.cantidad_entregada = cant_real
            detalle.subtotal = cant_real * detalle.precio_unitario
            nuevo_total_venta += detalle.subtotal
            
        orden.total_venta = nuevo_total_venta
        orden.saldo_pendiente = nuevo_total_venta 
        
        # 2. Registrar Pago Contra-Entrega
        monto_abono = float(info_pago.get('monto', 0))
        pago_id = None
        
        if monto_abono > 0:
            folio_pago = f"PAG-{datetime.now().strftime('%y%m%d')}-{orden.id}"
            
            nuevo_pago = Pago(
                folio_recibo=folio_pago,
                cliente_id=orden.cliente_id,
                orden_id=orden.id,
                tipo_movimiento_id=int(info_pago.get('tipo_id')), # ID real del catálogo
                cobrado_por_id=current_user.id,
                
                monto_pago=monto_abono,
                dinero_recibido=float(info_pago.get('recibido', 0)),
                cambio_devuelto=float(info_pago.get('cambio', 0)),
                
                estado='POR_AUDITAR',
                notas=notas
            )
            db.session.add(nuevo_pago)
            db.session.flush()
            pago_id = nuevo_pago.id
            
            orden.saldo_pendiente -= monto_abono

        # 3. Saldos y Estados
        deuda_previa = float(orden.cliente.saldo_actual or 0)
        orden.cliente.saldo_actual = deuda_previa + nuevo_total_venta - monto_abono

        if orden.saldo_pendiente <= 0.5:
            orden.estado = 'PAGADO'
            orden.saldo_pendiente = 0 
        else:
            orden.estado = 'ENTREGADA' 

        db.session.commit()
        
        return jsonify({
            'status': 'success', 
            'message': 'Entrega procesada.',
            'orden_id': orden.id,
            'pago_id': pago_id
        })

    except Exception as e:
        db.session.rollback()
        print(f"Error Logistica: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# --- 5. TICKET ---
@logistics_bp.route('/ticket/<int:orden_id>')
@login_required
def ver_ticket(orden_id):
    orden = OrdenVenta.query.get_or_404(orden_id)
    # Buscamos el último pago de esta orden
    ultimo_pago = Pago.query.filter_by(orden_id=orden.id).order_by(Pago.id.desc()).first()
    return render_template('logistics/ticket.html', orden=orden, pago=ultimo_pago)