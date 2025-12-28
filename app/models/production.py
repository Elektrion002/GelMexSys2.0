from app.extensions import db
from datetime import datetime
# IMPORTAMOS EL MODELO CORRECTO (Usuario, no User)
from app.models.users import Usuario 

class OrdenProduccion(db.Model):
    __tablename__ = 'ordenes_produccion'

    id = db.Column(db.Integer, primary_key=True)
    folio = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relación con Producto
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    
    # Receta (Opcional por ahora)
    receta_id = db.Column(db.Integer, nullable=True)
    
    cantidad = db.Column(db.Float, nullable=False)
    
    # Quién la pidió
    # CORRECCIÓN 1: La tabla real se llama 'usuarios', no 'users'
    usuario_solicita_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Fechas
    fecha_solicitud = db.Column(db.DateTime, default=datetime.now)
    fecha_inicio = db.Column(db.DateTime, nullable=True)
    fecha_termino = db.Column(db.DateTime, nullable=True)
    
    # Estatus: SOLICITADA, EN_PRODUCCION, BATIENDO, TERMINADA, CANCELADA
    estatus = db.Column(db.String(20), default='SOLICITADA')
    prioridad = db.Column(db.String(20), default='NORMAL')

    # Relaciones
    producto = db.relationship('Producto', backref='ordenes')
    
    # CORRECCIÓN 2: Usamos la clase 'Usuario' que importamos arriba
    usuario = db.relationship('Usuario', backref='ordenes_creadas')