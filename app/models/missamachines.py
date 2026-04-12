from app.extensions import db
from datetime import datetime

class MissaCliente(db.Model):
    __tablename__ = 'missa_clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(50))
    direccion = db.Column(db.String(255))
    sector = db.Column(db.String(100))
    email = db.Column(db.String(150))
    activo = db.Column(db.Boolean, default=True)
    
    ventas = db.relationship('MissaVenta', backref='cliente', lazy=True)

class MissaVenta(db.Model):
    __tablename__ = 'missa_ventas'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('missa_clientes.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    tipo_documento = db.Column(db.String(50), default='venta') # 'cotizacion', 'venta'
    
    # Financials Totals
    subtotal = db.Column(db.Numeric(12, 2), default=0.00)
    impuestos = db.Column(db.Numeric(12, 2), default=0.00)
    anticipo = db.Column(db.Numeric(12, 2), default=0.00)
    resta = db.Column(db.Numeric(12, 2), default=0.00)
    total = db.Column(db.Numeric(12, 2), default=0.00)
    
    # Seller
    vendedor = db.Column(db.String(150))
    telefono_vendedor = db.Column(db.String(50))

    detalles = db.relationship('MissaVentaDetalle', backref='venta', lazy=True, cascade="all, delete-orphan")

class MissaVentaDetalle(db.Model):
    __tablename__ = 'missa_venta_detalles'

    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('missa_ventas.id'), nullable=False)
    
    cantidad = db.Column(db.Integer, default=1)
    descripcion = db.Column(db.Text, nullable=False) # Here they can type "DESPULPADORA DE FRUTAS... MODELO:... VOLTAJE:..." or "TRANSPORTE"
    
    subtotal = db.Column(db.Numeric(12, 2), default=0.00)
    anticipo = db.Column(db.Numeric(12, 2), default=0.00)
    resta = db.Column(db.Numeric(12, 2), default=0.00)
