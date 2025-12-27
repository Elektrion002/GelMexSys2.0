# app/models/catalogs.py
from app.extensions import db

# --- CLASES BASE PARA REUTILIZAR CÓDIGO ---
class CatalogoBase(db.Model):
    """Clase abstracta para catálogos simples (id, descripcion/nombre)"""
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    activo = db.Column(db.Boolean, default=True)

# --- INFRAESTRUCTURA ---
class CatPlanta(CatalogoBase):
    __tablename__ = 'cat_plantas'
    descripcion = db.Column(db.String(100), nullable=False)
    notas = db.Column(db.String(255))

class CatArea(CatalogoBase):
    __tablename__ = 'cat_areas'
    descripcion = db.Column(db.String(100), nullable=False)
    notas = db.Column(db.String(255))

class CatUbicacion(CatalogoBase):
    __tablename__ = 'cat_ubicaciones'
    descripcion = db.Column(db.String(100), nullable=False) # Pasillo A, Nivel 1, etc.

class CatTipoAlmacen(CatalogoBase):
    __tablename__ = 'cat_tipos_almacen'
    nombre = db.Column(db.String(50), nullable=False)

class CatTipoMovimientoAlmacen(CatalogoBase):
    __tablename__ = 'cat_tipos_movimiento_almacen'
    descripcion = db.Column(db.String(50), nullable=False, unique=True)

# --- PRODUCTOS ---
class CatUnidadMedida(CatalogoBase):
    __tablename__ = 'cat_unidades_medida'
    nombre = db.Column(db.String(50), nullable=False)
    abreviatura = db.Column(db.String(10), nullable=False)

class CatCategoriaProducto(CatalogoBase):
    __tablename__ = 'cat_categorias_producto'
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))

class CatCategoriaMateriaPrima(CatalogoBase):
    __tablename__ = 'cat_categorias_materia_prima'
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))

# --- RH Y OPERACIÓN ---
class CatPuesto(CatalogoBase):
    __tablename__ = 'cat_puestos'
    nombre = db.Column(db.String(50), nullable=False)
    nivel_acceso = db.Column(db.Integer, default=1) # 1-5

class CatTipoVehiculo(CatalogoBase):
    __tablename__ = 'cat_tipos_vehiculo'
    nombre = db.Column(db.String(50), nullable=False)

class CatModeloVehiculo(CatalogoBase):
    __tablename__ = 'cat_modelos_vehiculo'
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    anio = db.Column(db.Integer)

class CatModeloActivo(CatalogoBase):
    __tablename__ = 'cat_modelos_activo'
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    capacidad_litros = db.Column(db.Float)

class CatEstadoFisico(CatalogoBase):
    __tablename__ = 'cat_estados_fisicos'
    descripcion = db.Column(db.String(50), nullable=False)

class CatTipoIncidencia(CatalogoBase):
    __tablename__ = 'cat_tipos_incidencia'
    descripcion = db.Column(db.String(100), nullable=False)

# --- FINANZAS Y CONTROL ---
class CatBancoCaja(CatalogoBase):
    __tablename__ = 'cat_bancos_cajas'
    nombre = db.Column(db.String(100), nullable=False)

class CatConceptoFinanzas(CatalogoBase):
    __tablename__ = 'cat_conceptos_finanzas'
    tipo_flujo = db.Column(db.String(20), nullable=False) # INGRESO, EGRESO, DEUDA
    descripcion = db.Column(db.String(100), nullable=False)

class CatTipoDescuento(CatalogoBase):
    __tablename__ = 'cat_tipos_descuento'
    descripcion = db.Column(db.String(50), nullable=False) # PORCENTAJE, PRECIO_FINAL

class CatTipoPagoSolicitado(CatalogoBase):
    __tablename__ = 'cat_tipos_pago_solicitado'
    descripcion = db.Column(db.String(50), nullable=False) # CONTADO, CREDITO

class CatEstadoOrdenVenta(CatalogoBase):
    __tablename__ = 'cat_estados_orden_venta'
    descripcion = db.Column(db.String(50), nullable=False) # BORRADOR, CONFIRMADO...

class CatEstadoPlanProduccion(CatalogoBase):
    __tablename__ = 'cat_estados_plan_produccion'
    descripcion = db.Column(db.String(50), nullable=False) # PLANIFICADO, EN_PROCESO...

class CatEstadoOrdenEmpaque(CatalogoBase):
    __tablename__ = 'cat_estados_orden_empaque'
    descripcion = db.Column(db.String(50), nullable=False)

class CatTipoMovimientoFinanzas(CatalogoBase):
    __tablename__ = 'cat_tipos_movimiento_finanzas'
    descripcion = db.Column(db.String(50), nullable=False) # CARGO_VENTA...

class CatEstadoDeudaEmpresa(CatalogoBase):
    __tablename__ = 'cat_estados_deuda_empresa'
    descripcion = db.Column(db.String(50), nullable=False) # PENDIENTE...

class CatTipoFlujo(CatalogoBase):
    __tablename__ = 'cat_tipos_flujo'
    descripcion = db.Column(db.String(50), nullable=False) # ENTRADA, SALIDA

class CatOrigenFlujo(CatalogoBase):
    __tablename__ = 'cat_origenes_flujo'
    descripcion = db.Column(db.String(50), nullable=False) # CAPITAL, VENTAS...

class CatPeriodo(CatalogoBase):
    __tablename__ = 'cat_periodos'
    descripcion = db.Column(db.String(50), nullable=False) # MENSUAL, ANUAL