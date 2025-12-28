from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.extensions import db
from datetime import datetime
from app.models.products import Producto
from app.models.orders import OrdenVenta, OrdenVentaDetalle
from sqlalchemy import text # Para no pelear con modelos

production_bp = Blueprint('production', __name__, url_prefix='/produccion')

@production_bp.route('/tablero-necesidades')
@login_required
def tablero_necesidades():
    db.session.expire_all() 
    productos = Producto.query.all()
    analisis = []

    for p in productos:
        # Demanda Nueva (Ventas que apenas entraron)
        demanda = db.session.query(db.func.sum(OrdenVentaDetalle.cantidad_pedida))\
            .join(OrdenVenta, OrdenVentaDetalle.orden_id == OrdenVenta.id)\
            .filter(OrdenVentaDetalle.producto_id == p.id)\
            .filter(OrdenVenta.estado == 'CONFIRMADA').scalar() or 0

        # WIP: Ventas que ya mandaste a fabricar (PRODUCCION)
        en_proceso = db.session.query(db.func.sum(OrdenVentaDetalle.cantidad_pedida))\
            .join(OrdenVenta, OrdenVentaDetalle.orden_id == OrdenVenta.id)\
            .filter(OrdenVentaDetalle.producto_id == p.id)\
            .filter(OrdenVenta.estado == 'PRODUCCION').scalar() or 0

        # EXISTENCIA REAL (SQL Puro - usando 'cantidad_actual' de tu DB)
        sql_stock = text("SELECT SUM(cantidad_actual) FROM inventario_productos WHERE producto_id = :pid")
        fisico_total = db.session.execute(sql_stock, {"pid": p.id}).scalar() or 0

        meta_optima = p.stock_ideal if p.stock_ideal is not None else 0
        
        # CÁLCULO DEFINITIVO: (Venta + Meta) - (Fisico + Ya batiéndose)
        necesidad_final = (demanda + meta_optima) - (fisico_total + en_proceso)
        final = max(0, necesidad_final)

        color = "success"
        if fisico_total < demanda: color = "danger"
        elif final > 0: color = "warning"

        # IMPORTANTE: El nombre debe ser "en_proceso" para que el HTML lo vea
        analisis.append({
            "id": p.id,
            "sku": p.sku,
            "descripcion": p.descripcion,
            "demanda": demanda,
            "en_proceso": en_proceso, # <-- ANTES DECÍA "batiendo", POR ESO TRONABA
            "stock_actual": fisico_total,
            "stock_ideal": meta_optima,
            "producir": final,
            "semaforo": color
        })

    return render_template('production/needs_board.html', 
                           analisis=analisis, 
                           now=datetime.now().strftime('%H:%M'))

@production_bp.route('/guardar-orden', methods=['POST'])
@login_required
def guardar_orden():
    try:
        db.session.query(OrdenVenta).filter(
            OrdenVenta.estado == 'CONFIRMADA'
        ).update({"estado": "PRODUCCION"}, synchronize_session='fetch')
        db.session.commit()
        return jsonify({"status": "success", "message": "Tablero actualizado."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)})