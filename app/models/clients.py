# app/models/clients.py
from app.extensions import db

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    
    # --- NEGOCIO ---
    nombre_negocio = db.Column(db.String(150), nullable=False)
    rfc = db.Column(db.String(13)) # Fiscal
    tipo_negocio = db.Column(db.String(100)) # Abarrotes, Papelería...
    img_fachada = db.Column(db.String(255))
    calificacion = db.Column(db.Integer, default=5)

    # --- ENCARGADO ---
    nombres_encargado = db.Column(db.String(100))
    apellidos_encargado = db.Column(db.String(100))
    img_ine_frente = db.Column(db.String(255))
    img_ine_reverso = db.Column(db.String(255))

    # --- DOMICILIO NEGOCIO ---
    calle = db.Column(db.String(100))
    num_exterior = db.Column(db.String(20))
    num_interior = db.Column(db.String(20))
    colonia = db.Column(db.String(100))
    ciudad = db.Column(db.String(100))
    codigo_postal = db.Column(db.String(10))
    estado = db.Column(db.String(100))
    pais = db.Column(db.String(100), default="México")

    # --- FINANCIERO ---
    limite_credito = db.Column(db.Numeric(12, 2), default=0.00)
    saldo_actual = db.Column(db.Numeric(12, 2), default=0.00) # Se actualiza vía Ledger
    
    # --- LOGÍSTICA ---
    ruta_id = db.Column(db.Integer, db.ForeignKey('rutas_reparto.id'))
    repartidor_habitual_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    vendedor_habitual_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)

    # Relaciones
    ruta = db.relationship('RutaReparto', backref='clientes')
    # Usamos string en foreign_keys para evitar import circular con Usuario si fuera necesario
    repartidor = db.relationship('Usuario', foreign_keys=[repartidor_habitual_id])
    vendedor = db.relationship('Usuario', foreign_keys=[vendedor_habitual_id])

class PrecioEspecialCliente(db.Model):
    __tablename__ = 'precios_especiales_cliente'

    id = db.Column(db.Integer, primary_key=True)
    
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    
    # FK a tu catálogo nuevo de tipos de descuento
    tipo_descuento_id = db.Column(db.Integer, db.ForeignKey('cat_tipos_descuento.id'))
    
    valor_descuento = db.Column(db.Numeric(10, 2), nullable=False) # 10%, $5.00, etc.

    cliente = db.relationship('Cliente', backref='precios_especiales')
    producto = db.relationship('Producto')
    tipo_descuento = db.relationship('CatTipoDescuento')