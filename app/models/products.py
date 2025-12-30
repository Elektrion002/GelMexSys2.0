# app/models/products.py
from app.extensions import db

class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    
    # Clasificación
    categoria_id = db.Column(db.Integer, db.ForeignKey('cat_categorias_producto.id'))
    unidad_id = db.Column(db.Integer, db.ForeignKey('cat_unidades_medida.id'))

    # Dinero
    precio_costo_actual = db.Column(db.Numeric(10, 2), default=0.00)
    precio_venta_general = db.Column(db.Numeric(10, 2), default=0.00) # Base

    # Físico
    peso_gramos = db.Column(db.Float, default=0.0)
    caducidad_dias = db.Column(db.Integer, default=0)
    imagen_producto = db.Column(db.String(255))

    # Semáforos de Inventario
    stock_minimo = db.Column(db.Float, default=0.0)
    stock_maximo = db.Column(db.Float, default=0.0)
    stock_ideal = db.Column(db.Float, default=0.0)

    # --- CONTROL DE VIDA (Sincronización) ---
    # Esto le permite a Python ver la columna que YA EXISTE en tu BD
    activo = db.Column(db.Boolean, default=True)

    # Relaciones
    categoria = db.relationship('CatCategoriaProducto')
    unidad = db.relationship('CatUnidadMedida')

class MateriaPrima(db.Model):
    __tablename__ = 'materia_prima'

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    
    categoria_id = db.Column(db.Integer, db.ForeignKey('cat_categorias_materia_prima.id'))
    unidad_id = db.Column(db.Integer, db.ForeignKey('cat_unidades_medida.id'))

    # Dinero
    precio_costo_promedio = db.Column(db.Numeric(10, 2), default=0.00)
    precio_venta_general = db.Column(db.Numeric(10, 2), default=0.00) 

    # Físico
    peso_gramos = db.Column(db.Float, default=0.0)
    caducidad_dias = db.Column(db.Integer, default=0)
    imagen_materia = db.Column(db.String(255))
    
    # Inventario Ideal
    stock_minimo = db.Column(db.Float, default=0.0)
    stock_maximo = db.Column(db.Float, default=0.0)
    stock_ideal = db.Column(db.Float, default=0.0)

    # Agregado por seguridad para futuros filtros
    activo = db.Column(db.Boolean, default=True)

    categoria = db.relationship('CatCategoriaMateriaPrima')
    unidad = db.relationship('CatUnidadMedida')