# app/models/infrastructure.py
from app.extensions import db

class Almacen(db.Model):
    __tablename__ = 'almacenes'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)
    imagen_almacen = db.Column(db.String(255))
    
    # FKs
    tipo_id = db.Column(db.Integer, db.ForeignKey('cat_tipos_almacen.id'))
    planta_id = db.Column(db.Integer, db.ForeignKey('cat_plantas.id'))
    area_id = db.Column(db.Integer, db.ForeignKey('cat_areas.id'))

    # Relaciones
    tipo = db.relationship('CatTipoAlmacen')
    planta = db.relationship('CatPlanta')
    area = db.relationship('CatArea')

class UbicacionAlmacen(db.Model):
    __tablename__ = 'ubicaciones_almacen'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False) # Ej: CFPA001B004
    notas = db.Column(db.String(255))
    
    almacen_id = db.Column(db.Integer, db.ForeignKey('almacenes.id'))
    
    # Vinculación opcional con catálogo visual (Pasillo, Nivel)
    cat_ubicacion_id = db.Column(db.Integer, db.ForeignKey('cat_ubicaciones.id'), nullable=True)

    almacen = db.relationship('Almacen', backref='ubicaciones')

class RutaReparto(db.Model):
    __tablename__ = 'rutas_reparto'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)
    img_mapa = db.Column(db.String(255))
    notas = db.Column(db.Text)