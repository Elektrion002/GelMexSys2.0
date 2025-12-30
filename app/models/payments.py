from app.extensions import db
from datetime import datetime

class Pago(db.Model):
    __tablename__ = 'pagos'

    id = db.Column(db.Integer, primary_key=True)
    folio_recibo = db.Column(db.String(50), unique=True, nullable=False)
    
    # FKs OBLIGATORIAS
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    orden_id = db.Column(db.Integer, db.ForeignKey('ordenes_venta.id'), nullable=False)
    tipo_movimiento_id = db.Column(db.Integer, db.ForeignKey('cat_tipos_movimiento_finanzas.id'), nullable=False)
    
    # RESPONSABLES
    cobrado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    auditado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True) # Puede ser Null al inicio
    
    # DINERO
    monto_pago = db.Column(db.Numeric(12, 2), nullable=False)
    dinero_recibido = db.Column(db.Numeric(12, 2))
    cambio_devuelto = db.Column(db.Numeric(12, 2))
    
    referencia = db.Column(db.String(100))
    estado = db.Column(db.String(20), default='POR_AUDITAR')
    
    fecha_registro = db.Column(db.DateTime, default=datetime.now)
    fecha_auditoria = db.Column(db.DateTime)
    notas = db.Column(db.Text)

    # RELACIONES
    cliente = db.relationship('Cliente', backref='historial_pagos')
    orden = db.relationship('OrdenVenta', backref='pagos_registrados')
    
    # Relación al catálogo (para saber si fue Efectivo o Transferencia)
    # Asumimos que el modelo CatTipoMovimientoFinanzas ya existe en tus catálogos.
    # Si te da error de import, asegúrate de importarlo aquí o definirlo.
    
    # RELACIONES CON USUARIOS
    cobrador = db.relationship('Usuario', foreign_keys=[cobrado_por_id], backref='cobros_realizados')
    auditor = db.relationship('Usuario', foreign_keys=[auditado_por_id], backref='cobros_auditados')