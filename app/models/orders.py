# app/models/orders.py
from app.extensions import db
from datetime import datetime

class OrdenVenta(db.Model):
    __tablename__ = 'ordenes_venta'

    id = db.Column(db.Integer, primary_key=True)
    folio = db.Column(db.String(20), unique=True, nullable=False)
    
    # Actores
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Fechas
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_promesa_entrega = db.Column(db.Date, nullable=False)
    
    # Estados: BORRADOR, CONFIRMADA, EN_EMPAQUE, EN_RUTA, ENTREGADA, CANCELADA
    estado = db.Column(db.String(25), default='BORRADOR')
    
    # Condiciones
    metodo_pago_esperado = db.Column(db.String(20)) # CREDITO / CONTADO
    total_venta = db.Column(db.Float, default=0.0)
    notas_vendedor = db.Column(db.Text)

    # Relaciones
    items = db.relationship('OrdenVentaDetalle', backref='orden', cascade="all, delete-orphan")
    cliente = db.relationship('Cliente', backref='historial_pedidos')
    vendedor = db.relationship('Usuario', backref='preventas_realizadas')

class OrdenVentaDetalle(db.Model):
    __tablename__ = 'orden_venta_detalles'

    id = db.Column(db.Integer, primary_key=True)
    orden_id = db.Column(db.Integer, db.ForeignKey('ordenes_venta.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    
    # Cantidades para trazabilidad total
    cantidad_pedida = db.Column(db.Float, nullable=False)
    cantidad_surtida = db.Column(db.Float, default=0.0)
    cantidad_entregada = db.Column(db.Float, default=0.0)
    
    # Costos en el momento de la venta
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    producto = db.relationship('Producto')