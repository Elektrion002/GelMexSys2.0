from app.extensions import db
from datetime import datetime

class CajaEmpresa(db.Model):
    __tablename__ = 'caja_empresa'
    
    id = db.Column(db.Integer, primary_key=True)
    saldo_actual = db.Column(db.Numeric(10, 2), default=0.00)
    ultima_actualizacion = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'<Caja ${self.saldo_actual}>'

class TransaccionFinanciera(db.Model):
    # ESTA ES LA TABLA MAESTRA DE TESORERÍA (EL HISTORIAL)
    __tablename__ = 'transacciones_financieras'

    id = db.Column(db.Integer, primary_key=True)
    
    # NUEVO: FOLIO ÚNICO DE TESORERÍA (Ej: TES-ING-251230-ABCD)
    folio = db.Column(db.String(50), unique=True, nullable=False)
    
    tipo = db.Column(db.String(20))  # 'INGRESO' o 'EGRESO'
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    concepto = db.Column(db.String(255)) 
    notas = db.Column(db.Text, nullable=True) # Para detalles extra
    fecha = db.Column(db.DateTime, default=datetime.now)
    
    # Relación con quien hizo el movimiento (Admin Finanzas)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id')) 
    usuario = db.relationship('Usuario', backref=db.backref('transacciones', lazy=True))
    
    # RASTREABILIDAD (De dónde vino esto)
    # Si viene de un pago de chofer:
    pago_origen_id = db.Column(db.Integer, db.ForeignKey('pagos.id'), nullable=True)
    pago_origen = db.relationship('Pago', backref='transaccion_tesoreria')
    
    # Si viene de un gasto operativo:
    gasto_id = db.Column(db.Integer, db.ForeignKey('gastos_operativos.id'), nullable=True)
    gasto = db.relationship('GastoOperativo', backref='transaccion_tesoreria')

class GastoOperativo(db.Model):
    __tablename__ = 'gastos_operativos'

    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50)) 
    descripcion = db.Column(db.String(255))
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    notas = db.Column(db.Text, nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.now)
    
    registrado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    registrado_por = db.relationship('Usuario', backref='gastos_registrados')
    
    proveedor_id = db.Column(db.Integer, nullable=True)