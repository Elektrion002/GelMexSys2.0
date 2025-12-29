from app.extensions import db
from datetime import datetime

class OrdenPaquete(db.Model):
    __tablename__ = 'orden_paquetes'

    id = db.Column(db.Integer, primary_key=True)
    orden_id = db.Column(db.Integer, db.ForeignKey('ordenes_venta.id'), nullable=False)
    
    codigo_etiqueta = db.Column(db.String(50), unique=True)
    numero_caja = db.Column(db.Integer)
    total_cajas_orden = db.Column(db.Integer)
    
    descripcion_contenido = db.Column(db.Text)
    peso_kg = db.Column(db.Float, default=0.0)
    
    creado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)

    # Relación inversa: orden.paquetes
    orden = db.relationship('OrdenVenta', backref='paquetes')
    usuario = db.relationship('Usuario')