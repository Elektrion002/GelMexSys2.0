# app/models/infrastructure.py
from app.extensions import db
from datetime import datetime

class Almacen(db.Model):
    __tablename__ = 'almacenes'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)
    imagen_almacen = db.Column(db.String(255))
    tipo_id = db.Column(db.Integer, db.ForeignKey('cat_tipos_almacen.id'))
    planta_id = db.Column(db.Integer, db.ForeignKey('cat_plantas.id'))
    area_id = db.Column(db.Integer, db.ForeignKey('cat_areas.id'))
    
    tipo = db.relationship('CatTipoAlmacen')
    planta = db.relationship('CatPlanta')
    area = db.relationship('CatArea')

class UbicacionAlmacen(db.Model):
    __tablename__ = 'ubicaciones_almacen'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    notas = db.Column(db.String(255))
    almacen_id = db.Column(db.Integer, db.ForeignKey('almacenes.id'))
    cat_ubicacion_id = db.Column(db.Integer, db.ForeignKey('cat_ubicaciones.id'), nullable=True)
    
    almacen = db.relationship('Almacen', backref='ubicaciones')

class RutaReparto(db.Model):
    __tablename__ = 'rutas_reparto'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)
    img_mapa = db.Column(db.String(255))
    notas = db.Column(db.Text)

# --- CLASES FALTANTES AGREGADAS (CORRIGE EL ERROR CRÍTICO DEL AUDITOR) ---

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'
    id = db.Column(db.Integer, primary_key=True)
    placas = db.Column(db.String(20), unique=True)
    serie_vehiculo = db.Column(db.String(50))
    tipo_id = db.Column(db.Integer, db.ForeignKey('cat_tipos_vehiculo.id'))
    modelo_id = db.Column(db.Integer, db.ForeignKey('cat_modelos_vehiculo.id'))
    
    # Estado
    asignado = db.Column(db.Boolean, default=False)
    kilometraje_ultimo_servicio = db.Column(db.Float)
    
    # Relaciones
    tipo = db.relationship('CatTipoVehiculo')
    # modelo = db.relationship('CatModeloVehiculo') # Descomentar si el catálogo existe

class ActivoFrio(db.Model):
    __tablename__ = 'activos_frio'
    id = db.Column(db.Integer, primary_key=True)
    serie = db.Column(db.String(50), unique=True)
    descripcion = db.Column(db.String(100))
    modelo_id = db.Column(db.Integer, db.ForeignKey('cat_modelos_activo.id'))
    estado_id = db.Column(db.Integer, db.ForeignKey('cat_estados_fisicos.id'))
    asignado = db.Column(db.Boolean, default=False)