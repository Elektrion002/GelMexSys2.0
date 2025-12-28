# app/models/stock.py
from app.extensions import db
from datetime import datetime

class InventarioProducto(db.Model):
    __tablename__ = 'inventario_productos'

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=True)
    materia_prima_id = db.Column(db.Integer, db.ForeignKey('materia_prima.id'), nullable=True)
    ubicacion_id = db.Column(db.Integer, db.ForeignKey('ubicaciones_almacen.id'), nullable=False)

    # --- CORRECCIÓN CRÍTICA: Nombre alineado con Postgres ---
    cantidad_actual = db.Column(db.Float, default=0.0)  # ANTES: cantidad_fisica
    cantidad_reservada = db.Column(db.Float, default=0.0) 
    
    # Propiedad calculada para saber qué puede vender el preventista
    @property
    def cantidad_disponible(self):
        # AQUÍ TAMBIÉN HABÍA QUE CORREGIR EL NOMBRE
        return self.cantidad_actual - self.cantidad_reservada

    # --- TRAZABILIDAD ---
    fecha_produccion = db.Column(db.Date, nullable=True) 
    fecha_ingreso_almacen = db.Column(db.DateTime, default=datetime.utcnow)

    # --- SEMÁFOROS POR UBICACIÓN ---
    stock_minimo = db.Column(db.Float, default=0.0)
    stock_maximo = db.Column(db.Float, default=0.0)
    stock_ideal = db.Column(db.Float, default=0.0)

    # Relaciones
    producto = db.relationship('Producto', backref='existencias')
    ubicacion = db.relationship('UbicacionAlmacen', backref='productos_almacenados')

class MovimientoTemporal(db.Model):
    """Guarda las reservas mientras el almacenista está empacando"""
    __tablename__ = 'movimientos_temporales'
    
    id = db.Column(db.Integer, primary_key=True)
    orden_venta_id = db.Column(db.Integer, nullable=False) # Relación a la orden
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    ubicacion_origen_id = db.Column(db.Integer, db.ForeignKey('ubicaciones_almacen.id'))
    cantidad = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), default='RESERVADO') # RESERVADO, CONFIRMADO, MERMA

class HistorialMovimiento(db.Model):
    """Kárdex Profesional para auditoría de cada pieza"""
    __tablename__ = 'historial_movimientos'
    
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    ubicacion_id = db.Column(db.Integer, db.ForeignKey('ubicaciones_almacen.id'))
    tipo_movimiento = db.Column(db.String(50)) # ENTRADA_PRODUCCION, MERMA, AJUSTE, SALIDA_VENTA
    cantidad = db.Column(db.Float, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    referencia = db.Column(db.String(100)) # ID de Orden o Lote
    notas = db.Column(db.Text)