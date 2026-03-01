# app/blueprints/api_test.py
from flask import Blueprint, jsonify
from app.models.users import Usuario
from app.models.products import Producto
from app.models.clients import Cliente

# Definimos el "Mapa" de rutas para pruebas
api_bp = Blueprint('api_test', __name__, url_prefix='/api/v1')

@api_bp.route('/status', methods=['GET'])
def check_status():
    return jsonify({"status": "OK", "message": "GelMexSys 2.0 Backend Operativo", "db": "PostgreSQL"})

@api_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    # Consulta real a la Base de Datos
    users = Usuario.query.all()
    # Convertimos los objetos de Python a lista de diccionarios (JSON)
    data = [{
        "id": u.id, 
        "nombre": f"{u.nombres} {u.apellido_paterno}", 
        "email": u.email_acceso,
        "puesto": u.puesto.nombre if u.puesto else "Sin Asignar"
    } for u in users]
    return jsonify(data)

@api_bp.route('/productos', methods=['GET'])
def get_productos():
    prods = Producto.query.all()
    data = [{
        "sku": p.sku,
        "descripcion": p.descripcion,
        "precio_venta": float(p.precio_venta_general),
        "stock_actual": 0 # Ahorita está en 0 porque no hemos hecho entradas de almacén
    } for p in prods]
    return jsonify(data)

@api_bp.route('/clientes', methods=['GET'])
def get_clientes():
    clients = Cliente.query.all()
    data = []
    for c in clients:
        # Sacamos sus precios especiales
        precios = []
        for p_esp in c.precios_especiales:
            precios.append({
                "producto": p_esp.producto.descripcion,
                "descuento_tipo": p_esp.tipo_descuento.descripcion,
                "valor": float(p_esp.valor_descuento)
            })
            
        data.append({
            "negocio": c.nombre_negocio,
            "encargado": c.nombres_encargado,
            "precios_especiales": precios
        })
    return jsonify(data)