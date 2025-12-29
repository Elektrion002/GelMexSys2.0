from app.extensions import db
from datetime import datetime
from app.models.users import Usuario 

class OrdenProduccion(db.Model):
    __tablename__ = 'ordenes_produccion'

    id = db.Column(db.Integer, primary_key=True)
    folio = db.Column(db.String(50), unique=True, nullable=False)
    
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    receta_id = db.Column(db.Integer, nullable=True)
    
    # LO QUE SE PIDE (Teórico)
    cantidad = db.Column(db.Float, nullable=False)
    
    # LO QUE SALE (Realidad - Reportado por Maestro Heladero)
    cantidad_producida_real = db.Column(db.Float, default=0)
    notas_produccion = db.Column(db.Text, nullable=True)

    # --- NUEVO CAMPO PARA RECEPCIÓN PARCIAL (ALMACÉN) ---
    # Aquí se va sumando lo que el almacenista mete al refri poco a poco.
    cantidad_recibida_almacen = db.Column(db.Float, default=0)
    # ----------------------------------------------------

    usuario_solicita_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    fecha_solicitud = db.Column(db.DateTime, default=datetime.now)
    fecha_inicio = db.Column(db.DateTime, nullable=True)
    fecha_termino = db.Column(db.DateTime, nullable=True)
    
    # ESTATUS: 
    # 'SOLICITADA' -> 'BATIENDO' -> 'POR_RECIBIR' (En tránsito/Parcial) -> 'TERMINADA' (Cerrada)
    estatus = db.Column(db.String(20), default='SOLICITADA')
    prioridad = db.Column(db.String(20), default='NORMAL')

    producto = db.relationship('Producto', backref='ordenes')
    usuario = db.relationship('Usuario', backref='ordenes_creadas')