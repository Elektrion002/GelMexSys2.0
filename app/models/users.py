# app/models/users.py
from app.extensions import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    
    # --- IDENTIDAD ---
    nombres = db.Column(db.String(100), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100))
    fecha_nacimiento = db.Column(db.Date)
    estado_civil = db.Column(db.String(50))
    profesion = db.Column(db.String(100))
    curp = db.Column(db.String(18))
    rfc = db.Column(db.String(13)) # Fiscal

    # --- DOMICILIO (Desglosado) ---
    calle = db.Column(db.String(100))
    num_exterior = db.Column(db.String(20))
    num_interior = db.Column(db.String(20))
    colonia = db.Column(db.String(100))
    ciudad = db.Column(db.String(100))
    codigo_postal = db.Column(db.String(10))
    estado = db.Column(db.String(100))
    pais = db.Column(db.String(100), default="México")

    # --- CONTACTO ---
    telefono_casa = db.Column(db.String(20))
    telefono_celular = db.Column(db.String(20))
    email_personal = db.Column(db.String(100))
    
    # Emergencia
    contacto_emergencia_nombre = db.Column(db.String(150))
    contacto_emergencia_telefono = db.Column(db.String(20))

    # --- LABORAL ---
    puesto_id = db.Column(db.Integer, db.ForeignKey('cat_puestos.id'))
    fecha_inicio_empresa = db.Column(db.Date, default=datetime.utcnow)
    calificacion_evaluacion = db.Column(db.Integer, default=5) # 1-5 Estrellas
    notas_generales = db.Column(db.Text)

    # --- SEGURIDAD ---
    email_acceso = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    pin_seguridad = db.Column(db.String(6)) # Para aprobar movimientos rápidos
    nivel_usuario = db.Column(db.Integer, default=1)
    activo = db.Column(db.Boolean, default=True)

    # --- DOCUMENTACIÓN (Rutas de archivos) ---
    foto_perfil = db.Column(db.String(255))
    img_ine_frente = db.Column(db.String(255))
    img_ine_reverso = db.Column(db.String(255))
    img_licencia_frente = db.Column(db.String(255))
    img_licencia_reverso = db.Column(db.String(255))
    fecha_validez_licencia = db.Column(db.Date)

    # Relaciones
    puesto = db.relationship('CatPuesto', backref='usuarios')

    def __repr__(self):
        return f'<Usuario {self.nombres} {self.apellido_paterno}>'