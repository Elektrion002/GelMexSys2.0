from app.extensions import db
from datetime import datetime

class SolicitudPedido(db.Model):
    __tablename__ = 'solicitudes_pedido'

    id = db.Column(db.Integer, primary_key=True)
    folio = db.Column(db.String(30), unique=True, nullable=False)
    
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.now)
    
    # Estados: 'ESPERANDO_VENDEDOR', 'PENDIENTE_CLIENTE', 'CONFIRMADO_CLIENTE', 'CONVERTIDO', 'RECHAZADO'
    estado = db.Column(db.String(30), default='ESPERANDO_VENDEDOR')
    
    total_estimado = db.Column(db.Numeric(12, 2), default=0.00)
    notas_cliente = db.Column(db.Text)
    notas_vendedor = db.Column(db.Text)
    
    # Relaciones
    cliente = db.relationship('Cliente', backref='solicitudes_portal')
    items = db.relationship('SolicitudPedidoDetalle', backref='solicitud', cascade="all, delete-orphan")

class SolicitudPedidoDetalle(db.Model):
    __tablename__ = 'solicitud_pedido_detalles'

    id = db.Column(db.Integer, primary_key=True)
    solicitud_id = db.Column(db.Integer, db.ForeignKey('solicitudes_pedido.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    
    cantidad = db.Column(db.Float, nullable=False)
    precio_unitario = db.Column(db.Numeric(12, 2), nullable=False)
    subtotal = db.Column(db.Numeric(12, 2), nullable=False)

    producto = db.relationship('Producto')
