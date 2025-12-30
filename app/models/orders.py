from app.extensions import db
from datetime import datetime

class OrdenVenta(db.Model):
    __tablename__ = 'ordenes_venta'

    id = db.Column(db.Integer, primary_key=True)
    folio = db.Column(db.String(20), unique=True, nullable=False)
    
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    fecha_registro = db.Column(db.DateTime, default=datetime.now)
    fecha_promesa_entrega = db.Column(db.Date, nullable=False)
    
    # Estados: 'CONFIRMADA', 'PRODUCCION', 'LISTO_RUTA', 'EN_RUTA', 'ENTREGADA', 'PAGADO', 'CANCELADA'
    estado = db.Column(db.String(25), default='CONFIRMADA')
    
    metodo_pago_esperado = db.Column(db.String(20)) # 'Contado', 'Credito'
    
    # Dineros
    total_venta = db.Column(db.Float, default=0.0)    
    
    # Esta es la columna que faltaba y hacía tronar el ticket
    saldo_pendiente = db.Column(db.Numeric(12, 2), default=0.00) 
    # -----------------------------------

    notas_vendedor = db.Column(db.Text)

    # Relaciones
    cliente = db.relationship('Cliente', backref='ordenes')
    vendedor = db.relationship('Usuario', backref='ventas_realizadas')
    items = db.relationship('OrdenVentaDetalle', backref='orden', cascade="all, delete-orphan")
    
    # Relación con pagos (definida en el modelo Payment, pero accesible aquí por backref 'pagos_registrados')

class OrdenVentaDetalle(db.Model):
    __tablename__ = 'orden_venta_detalles'

    id = db.Column(db.Integer, primary_key=True)
    orden_id = db.Column(db.Integer, db.ForeignKey('ordenes_venta.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    
    cantidad_pedida = db.Column(db.Float, nullable=False)
    cantidad_surtida = db.Column(db.Float, default=0)   # Lo que salió de almacén
    cantidad_entregada = db.Column(db.Float, default=0) # Lo que recibió el cliente
    
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    producto = db.relationship('Producto')