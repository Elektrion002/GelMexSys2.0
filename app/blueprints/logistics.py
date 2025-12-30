import random
import string
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from sqlalchemy import func, or_, desc
from sqlalchemy.exc import IntegrityError
from app.extensions import db

# --- IMPORTACIÓN DE MODELOS ---
from app.models.orders import OrdenVenta, OrdenVentaDetalle
from app.models.payments import Pago
from app.models.clients import Cliente
from app.models.catalogs import CatTipoMovimientoFinanzas 

logistics_bp = Blueprint('logistics', __name__, url_prefix='/logistica')

# ==========================================
#  SECCIÓN 1: OPERATIVA DE REPARTO
# ==========================================

@logistics_bp.route('/')
@login_required
def index():
    pendientes = OrdenVenta.query.filter(
        OrdenVenta.estado.in_(['LISTO_RUTA', 'EN_RUTA'])
    ).order_by(OrdenVenta.fecha_promesa_entrega.asc()).all()

    terminadas = OrdenVenta.query.filter(
        OrdenVenta.estado.in_(['ENTREGADA', 'PAGADO', 'SINAUDITARPAGO'])
    ).order_by(OrdenVenta.id.desc()).limit(10).all()

    return render_template('logistics/route_dashboard.html', 
                           ordenes=pendientes, 
                           terminadas=terminadas)

@logistics_bp.route('/cargar/<int:orden_id>')
@login_required
def cargar_orden(orden_id):
    orden = OrdenVenta.query.get_or_404(orden_id)
    if orden.estado == 'LISTO_RUTA':
        orden.estado = 'EN_RUTA'
        db.session.commit()
        flash(f'📦 Orden {orden.folio} cargada.', 'success')
    return redirect(url_for('logistics.index'))

@logistics_bp.route('/entrega/<int:orden_id>')
@login_required
def entrega_cliente(orden_id):
    orden = OrdenVenta.query.get_or_404(orden_id)
    metodos_pago = CatTipoMovimientoFinanzas.query.filter_by(activo=True).all()
    
    deuda_historica = float(orden.cliente.saldo_actual or 0)
    ventas_en_curso = db.session.query(func.sum(OrdenVenta.total_venta))\
        .filter(OrdenVenta.cliente_id == orden.cliente_id)\
        .filter(OrdenVenta.id != orden.id)\
        .filter(OrdenVenta.estado.in_(['CONFIRMADA', 'EN_RUTA', 'EN_PRODUCCION', 'EMPACADO', 'ENTREGADA', 'SINAUDITARPAGO']))\
        .scalar() or 0.0
    saldo_global_previo = deuda_historica + float(ventas_en_curso)

    items_data = []
    total_piezas_bajar = 0
    for item in orden.items:
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
                           total_piezas=total_piezas_bajar, 
                           saldo_global_previo=saldo_global_previo,
                           metodos_pago=metodos_pago)

@logistics_bp.route('/confirmar-entrega', methods=['POST'])
@login_required
def confirmar_entrega():
    # --- BLOQUE DE SEGURIDAD CONTRA COLISIONES ---
    intentos = 0
    max_intentos = 5
    
    while intentos < max_intentos:
        try:
            data = request.json
            orden_id = data.get('orden_id')
            items_ajuste = data.get('items') 
            info_pago = data.get('pago')     
            notas = data.get('notas')

            orden = OrdenVenta.query.get_or_404(orden_id)
            
            # 1. Ajuste de inventario
            nuevo_total_venta = 0
            for item_data in items_ajuste:
                detalle = OrdenVentaDetalle.query.get(int(item_data['detalle_id']))
                if item_data.get('cant_real'):
                    cant_real = float(item_data['cant_real'])
                    detalle.cantidad_entregada = cant_real
                    detalle.subtotal = cant_real * detalle.precio_unitario
                    nuevo_total_venta += detalle.subtotal
                
            if nuevo_total_venta > 0:
                orden.total_venta = nuevo_total_venta
                if orden.estado not in ['ENTREGADA', 'PAGADO', 'SINAUDITARPAGO']:
                    orden.saldo_pendiente = nuevo_total_venta 
            
            # 2. Registrar Pago
            monto_abono = float(info_pago.get('monto', 0))
            pago_id = None
            
            if monto_abono > 0:
                # --- GENERADOR DE FOLIO ROBUSTO ---
                fecha_server = datetime.now().strftime('%y%m%d')
                sufijo_random = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
                folio_pago = f"PAG-{fecha_server}-{sufijo_random}"
                
                nuevo_pago = Pago(
                    folio_recibo=folio_pago,
                    cliente_id=orden.cliente_id,
                    orden_id=orden.id,
                    tipo_movimiento_id=int(info_pago.get('tipo_id')), 
                    cobrado_por_id=current_user.id,
                    monto_pago=monto_abono,
                    dinero_recibido=float(info_pago.get('recibido', 0)),
                    cambio_devuelto=float(info_pago.get('cambio', 0)),
                    estado='POR_AUDITAR', 
                    notas=notas
                )
                db.session.add(nuevo_pago)
                db.session.flush() # Aquí validamos unicidad
                pago_id = nuevo_pago.id
                
                # Descuento de saldo (safe float)
                saldo_actual_safe = float(orden.saldo_pendiente or 0)
                orden.saldo_pendiente = saldo_actual_safe - monto_abono

            # 3. Saldos Globales
            deuda_previa = float(orden.cliente.saldo_actual or 0)
            if nuevo_total_venta > 0 and orden.estado not in ['ENTREGADA', 'PAGADO', 'SINAUDITARPAGO']:
                orden.cliente.saldo_actual = deuda_previa + nuevo_total_venta - monto_abono
            else:
                orden.cliente.saldo_actual = deuda_previa - monto_abono

            # 4. Estados
            if float(orden.saldo_pendiente) <= 0.5:
                orden.saldo_pendiente = 0 
                orden.estado = 'SINAUDITARPAGO' 
            else:
                orden.estado = 'ENTREGADA' 

            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Operación procesada.', 'orden_id': orden.id, 'pago_id': pago_id})

        except IntegrityError:
            db.session.rollback()
            intentos += 1
            print(f"⚠️ Colisión de Folio detectada. Reintentando ({intentos}/5)...")
            continue
            
        except Exception as e:
            db.session.rollback()
            print(f"Error Logistica: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    return jsonify({'status': 'error', 'message': 'El sistema está saturado, intenta de nuevo.'}), 500

@logistics_bp.route('/ticket/<int:orden_id>')
@login_required
def ver_ticket(orden_id):
    orden = OrdenVenta.query.get_or_404(orden_id)
    # Traemos TODOS los pagos para el historial en el ticket
    todos_los_pagos = Pago.query.filter_by(orden_id=orden.id).order_by(Pago.fecha_registro.asc()).all()
    return render_template('logistics/ticket.html', orden=orden, pagos=todos_los_pagos)


# ==========================================
#  SECCIÓN 2: COBRANZA
# ==========================================

@logistics_bp.route('/cobranza')
@login_required
def cobranza_buscar():
    deudores = Cliente.query.filter(
        Cliente.saldo_actual > 1.0
    ).order_by(desc(Cliente.saldo_actual)).limit(100).all()

    return render_template('logistics/collection_search.html', deudores=deudores)

@logistics_bp.route('/api/buscar-deudores')
@login_required
def api_buscar_deudores():
    q = request.args.get('q', '').strip()
    if not q or len(q) < 3: return jsonify([])

    resultados = Cliente.query.filter(
        or_(
            Cliente.nombre_negocio.ilike(f'%{q}%'),
            Cliente.nombres_encargado.ilike(f'%{q}%'),
            Cliente.apellidos_encargado.ilike(f'%{q}%'),
            Cliente.calle.ilike(f'%{q}%'),
            Cliente.colonia.ilike(f'%{q}%')
        )
    ).limit(20).all()

    data = []
    for c in resultados:
        nombre_completo = f"{c.nombres_encargado or ''} {c.apellidos_encargado or ''}".strip()
        direccion_full = f"{c.calle or ''} {c.num_exterior or ''}, {c.colonia or ''}".strip()
        if direccion_full.startswith(','): direccion_full = direccion_full[1:].strip()

        data.append({
            'id': c.id,
            'negocio': c.nombre_negocio,
            'contacto': nombre_completo if nombre_completo else '---',
            'direccion': direccion_full if direccion_full else '---',
            'saldo': float(c.saldo_actual or 0)
        })
    
    return jsonify(data)

@logistics_bp.route('/cobranza/cliente/<int:cliente_id>')
@login_required
def cobranza_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    
    candidatos = OrdenVenta.query.filter(
        OrdenVenta.cliente_id == cliente.id,
        OrdenVenta.estado.in_(['ENTREGADA', 'PAGADO', 'SINAUDITARPAGO']), 
        OrdenVenta.estado != 'CANCELADA'
    ).order_by(OrdenVenta.fecha_registro.asc()).all()

    ordenes_reales = []

    for orden in candidatos:
        pagos_registrados = db.session.query(func.sum(Pago.monto_pago))\
            .filter(Pago.orden_id == orden.id)\
            .scalar() or 0.0
        
        deuda_operativa = float(orden.total_venta) - float(pagos_registrados)

        if deuda_operativa > 0.5:
            orden.saldo_pendiente = deuda_operativa 
            ordenes_reales.append(orden)

    return render_template('logistics/collection_client.html', 
                           cliente=cliente, 
                           ordenes=ordenes_reales)

# NUEVA API PARA EL HISTORIAL DE PAGOS DEL CLIENTE
@logistics_bp.route('/api/historial-pagos/<int:cliente_id>')
@login_required
def api_historial_pagos(cliente_id):
    # Últimos 20 pagos
    pagos = Pago.query.filter_by(cliente_id=cliente_id)\
        .order_by(Pago.fecha_registro.desc())\
        .limit(20).all()
    
    data = []
    for p in pagos:
        data.append({
            'folio': p.folio_recibo,
            'fecha': p.fecha_registro.strftime('%d/%m/%Y %H:%M'),
            'monto': float(p.monto_pago),
            'orden': p.orden.folio,
            'orden_id': p.orden_id
        })
    return jsonify(data)