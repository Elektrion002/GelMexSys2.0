from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.clients import Cliente
from app.models.products import Producto
from app.models.orders import OrdenVenta, OrdenVentaDetalle
from datetime import datetime

sales_bp = Blueprint('sales', __name__, url_prefix='/ventas')

# --- 1. RUTA PARA CARGAR LA CONSOLA (LO QUE YA TENÍAS) ---
@sales_bp.route('/preventa')
@login_required
def preventa():
    clientes = Cliente.query.all()
    productos_db = Producto.query.all()
    
    catalogo_js = []
    for p in productos_db:
        catalogo_js.append({
            "id": p.id,
            "sku": p.sku,
            "nombre": p.descripcion,
            "precio": float(p.precio_venta_general)
        })
        
    return render_template('sales/console.html', 
                           clientes=clientes, 
                           catalogo=catalogo_js,
                           date_now=datetime.now().strftime('%Y-%m-%d'))

# --- 2. API PARA PRECIOS ESPECIALES Y CRÉDITO ---
@sales_bp.route('/api/cliente/<int:id>')
@login_required
def api_cliente(id):
    c = Cliente.query.get_or_404(id)
    # Diccionario de precios especiales {id_producto: precio_especial}
    precios = {p.producto_id: float(p.valor_descuento) for p in c.precios_especiales}
    return jsonify({
        "limite_credito": float(c.limite_credito),
        "saldo_actual": float(c.saldo_actual),
        "disponible": float(c.limite_credito - c.saldo_actual),
        "precios_especiales": precios
    })

# --- 3. EL "OÍDO" QUE RECIBE EL PEDIDO DEL CELULAR ---
@sales_bp.route('/crear-pedido', methods=['POST'])
@login_required
def crear_pedido():
    data = request.json
    
    if not data or not data.get('items'):
        return jsonify({"status": "error", "message": "El pedido está vacío"}), 400

    try:
        # Generar Folio: PV + AñoMesDiaHoraMinutoSegundo
        folio_gen = f"PV-{datetime.now().strftime('%y%m%d%H%M%S')}"

        # A. Crear la Cabecera
        nueva_orden = OrdenVenta(
            folio = folio_gen,
            cliente_id = int(data['cliente_id']),
            vendedor_id = current_user.id,
            fecha_promesa_entrega = datetime.strptime(data['fecha_entrega'], '%Y-%m-%d'),
            metodo_pago_esperado = data['metodo_pago'],
            total_venta = 0, # Se actualiza abajo
            estado = 'CONFIRMADA'
        )
        
        db.session.add(nueva_orden)
        db.session.flush() 

        total_calculado = 0
        
        # B. Crear los Renglones (Items)
        # El JS manda 'items' como un objeto donde la llave es el ID del producto
        for prod_id, info in data['items'].items():
            subtotal = float(info['cant']) * float(info['precio'])
            total_calculado += subtotal
            
            detalle = OrdenVentaDetalle(
                orden_id = nueva_orden.id,
                producto_id = int(prod_id),
                cantidad_pedida = float(info['cant']),
                precio_unitario = float(info['precio']),
                subtotal = subtotal
            )
            db.session.add(detalle)

        # C. Actualizar total final
        nueva_orden.total_venta = total_calculado
        
        db.session.commit()
        
        return jsonify({
            "status": "success", 
            "message": f"Pedido {folio_gen} guardado!", 
            "folio": folio_gen
        })

    except Exception as e:
        db.session.rollback()
        print(f"Error en crear_pedido: {str(e)}") # Esto sale en tu consola negra
        return jsonify({"status": "error", "message": str(e)}), 500