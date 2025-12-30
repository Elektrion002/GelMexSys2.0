import random
import string
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from sqlalchemy import func, desc
from sqlalchemy.exc import IntegrityError
from app.extensions import db

# Modelos
from app.models.finance import CajaEmpresa, TransaccionFinanciera, GastoOperativo
from app.models.payments import Pago
from app.models.orders import OrdenVenta
from app.models.catalogs import CatConceptoFinanzas

finance_bp = Blueprint('finance', __name__, url_prefix='/finanzas')

# --- UTILIDAD: GENERADOR DE FOLIOS ---
def generar_folio_tesoreria(tipo):
    prefijo = "ING" if tipo == 'INGRESO' else "EGR"
    fecha = datetime.now().strftime('%y%m%d')
    sufijo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"TES-{prefijo}-{fecha}-{sufijo}"

@finance_bp.route('/')
@login_required
def dashboard():
    caja = CajaEmpresa.query.get(1)
    if not caja:
        caja = CajaEmpresa(id=1, saldo_actual=0)
        db.session.add(caja)
        db.session.commit()

    dinero_en_calle = db.session.query(func.sum(Pago.monto_pago))\
        .filter(Pago.estado == 'POR_AUDITAR').scalar() or 0.0

    mes_actual = datetime.now().month
    gastos_mes = db.session.query(func.sum(GastoOperativo.monto))\
        .filter(func.extract('month', GastoOperativo.fecha_registro) == mes_actual).scalar() or 0.0

    # Historial General
    ultimos_movimientos = TransaccionFinanciera.query\
        .order_by(desc(TransaccionFinanciera.fecha))\
        .limit(30).all()

    return render_template('finance/dashboard.html', 
                           caja=caja, 
                           en_calle=dinero_en_calle,
                           gastos=gastos_mes,
                           movimientos=ultimos_movimientos)

# --- SECCIÓN INGRESOS ---
@finance_bp.route('/ingresos')
@login_required
def ingresos():
    conceptos_ingreso = CatConceptoFinanzas.query.filter_by(tipo_flujo='INGRESO', activo=True).all()
    
    # Historial de INGRESOS (Transacciones)
    ultimos_ingresos = TransaccionFinanciera.query\
        .filter_by(tipo='INGRESO')\
        .order_by(desc(TransaccionFinanciera.fecha))\
        .limit(20).all()

    return render_template('finance/income.html', 
                           conceptos=conceptos_ingreso, 
                           ultimos_ingresos=ultimos_ingresos)

@finance_bp.route('/registrar-ingreso-extra', methods=['POST'])
@login_required
def registrar_ingreso_extra():
    try:
        monto = float(request.form.get('monto'))
        concepto_id = int(request.form.get('concepto_id'))
        detalle_texto = request.form.get('detalle')
        notas = request.form.get('notas')
    except (ValueError, TypeError):
        flash('❌ Error: Datos numéricos inválidos.', 'danger')
        return redirect(url_for('finance.ingresos'))

    cat_concepto = CatConceptoFinanzas.query.get(concepto_id)
    descripcion_base = cat_concepto.descripcion if cat_concepto else "Ingreso General"
    concepto_final = f"{descripcion_base} - {detalle_texto}" if detalle_texto else descripcion_base

    caja = CajaEmpresa.query.get(1)
    if not caja:
        caja = CajaEmpresa(id=1, saldo_actual=0)
        db.session.add(caja)

    caja.saldo_actual = float(caja.saldo_actual) + monto

    folio = generar_folio_tesoreria('INGRESO')

    transaccion = TransaccionFinanciera(
        folio=folio,
        tipo='INGRESO',
        monto=monto,
        concepto=concepto_final,
        notas=notas,
        usuario_id=current_user.id
    )
    db.session.add(transaccion)
    db.session.commit()

    flash(f"💰 Ingreso registrado correctamente. Folio: {folio}", 'success')
    return redirect(url_for('finance.ingresos'))

# --- AUDITORÍA ---
@finance_bp.route('/auditoria')
@login_required
def auditoria():
    pagos_pendientes = Pago.query.filter_by(estado='POR_AUDITAR')\
        .order_by(Pago.fecha_registro.desc()).all()
    return render_template('finance/audit.html', pagos=pagos_pendientes)

@finance_bp.route('/confirmar-ingreso', methods=['POST'])
@login_required
def confirmar_ingreso():
    pago_id = request.form.get('pago_id')
    accion = request.form.get('accion') 

    pago = Pago.query.get_or_404(pago_id)
    caja = CajaEmpresa.query.get(1)

    if accion == 'AUDITAR':
        pago.estado = 'AUDITADO'
        pago.auditado_por_id = current_user.id
        pago.fecha_auditoria = datetime.now()

        caja.saldo_actual = float(caja.saldo_actual) + float(pago.monto_pago)

        folio_tesoreria = generar_folio_tesoreria('INGRESO')

        transaccion = TransaccionFinanciera(
            folio=folio_tesoreria,
            tipo='INGRESO',
            monto=pago.monto_pago,
            concepto=f"Corte Caja - Pago Chofer {pago.folio_recibo}",
            notas=f"Orden: {pago.orden.folio}. Cliente: {pago.cliente.nombre_negocio}",
            usuario_id=current_user.id,
            pago_origen_id=pago.id
        )
        db.session.add(transaccion)

        orden = OrdenVenta.query.get(pago.orden_id)
        if orden.estado == 'SINAUDITARPAGO':
            orden.estado = 'PAGADO'

        msg = f"✅ Auditado correctamente. Generado Ticket: {folio_tesoreria}"

    elif accion == 'RECHAZAR':
        pago.estado = 'RECHAZADO'
        pago.notas = (pago.notas or '') + " | RECHAZADO POR FINANZAS."
        msg = "⚠️ Pago rechazado."

    db.session.commit()
    flash(msg, 'success' if accion == 'AUDITAR' else 'warning')
    return redirect(url_for('finance.auditoria'))

# --- SECCIÓN GASTOS ---
@finance_bp.route('/gastos')
@login_required
def gastos():
    conceptos_egreso = CatConceptoFinanzas.query.filter_by(tipo_flujo='EGRESO', activo=True).all()
    
    # CORRECCIÓN AQUÍ: Consultamos TransaccionFinanciera (que tiene folio) filtrando por EGRESO
    # en lugar de GastoOperativo.
    ultimos_gastos = TransaccionFinanciera.query\
        .filter_by(tipo='EGRESO')\
        .order_by(desc(TransaccionFinanciera.fecha))\
        .limit(20).all()
    
    return render_template('finance/expenses.html', 
                           gastos=ultimos_gastos,
                           conceptos=conceptos_egreso)

@finance_bp.route('/registrar-gasto', methods=['POST'])
@login_required
def registrar_gasto():
    try:
        monto = float(request.form.get('monto'))
        concepto_id = int(request.form.get('concepto_id'))
        detalle_texto = request.form.get('detalle')
        notas = request.form.get('notas')
    except (ValueError, TypeError):
        flash('❌ Error: Datos inválidos.', 'danger')
        return redirect(url_for('finance.gastos'))

    caja = CajaEmpresa.query.get(1)
    if not caja:
        caja = CajaEmpresa(id=1, saldo_actual=0)
        db.session.add(caja)
        
    saldo_actual = float(caja.saldo_actual)

    if saldo_actual < monto:
        flash(f'❌ Fondos insuficientes. Tienes ${saldo_actual:,.2f}', 'danger')
        return redirect(url_for('finance.gastos'))

    cat_concepto = CatConceptoFinanzas.query.get_or_404(concepto_id)
    nombre_categoria = cat_concepto.descripcion

    caja.saldo_actual = saldo_actual - monto

    # Guardamos el detalle en GastoOperativo
    nuevo_gasto = GastoOperativo(
        categoria=nombre_categoria,
        descripcion=detalle_texto,
        monto=monto,
        notas=notas,
        registrado_por_id=current_user.id
    )
    db.session.add(nuevo_gasto)
    db.session.flush()

    folio_tesoreria = generar_folio_tesoreria('EGRESO')

    # Guardamos la transacción maestra
    transaccion = TransaccionFinanciera(
        folio=folio_tesoreria,
        tipo='EGRESO',
        monto=monto,
        concepto=f"{nombre_categoria} - {detalle_texto}", 
        notas=notas,
        usuario_id=current_user.id,
        gasto_id=nuevo_gasto.id
    )
    db.session.add(transaccion)

    db.session.commit()
    flash(f"💸 Gasto registrado: {folio_tesoreria}", 'success')
    return redirect(url_for('finance.gastos'))

@finance_bp.route('/ticket/<string:folio>')
@login_required
def ver_ticket(folio):
    movimiento = TransaccionFinanciera.query.filter_by(folio=folio).first_or_404()
    return render_template('finance/ticket_movement.html', mov=movimiento)