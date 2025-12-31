# seed_runner.py
from app import create_app
from app.extensions import db
from werkzeug.security import generate_password_hash

# --- IMPORTAR MODELOS ---
from app.models.catalogs import *
from app.models.users import Usuario
from app.models.infrastructure import Almacen, UbicacionAlmacen, RutaReparto
from app.models.products import Producto, MateriaPrima
from app.models.clients import Cliente, PrecioEspecialCliente

# --- IMPORTAR DATOS (Nombres Corregidos) ---
from db_seeds.data_catalogs import CATALOGOS
from db_seeds.data_infrastructure import ALMACENES, RUTAS
from db_seeds.data_products import PRODUCTOS, MATERIAS_PRIMAS
from db_seeds.data_users import USUARIOS
from db_seeds.data_clients import CLIENTES

app = create_app()

def run_seeds():
    with app.app_context():
        print("🌱 INICIANDO SEMBRADO DE DATOS GELMEXSYS 2.0...")
        
        # 1. CATÁLOGOS
        print("--> Sembrando Catálogos...")
        mapa_catalogos = {
            "cat_plantas": CatPlanta, "cat_areas": CatArea, "cat_ubicaciones": CatUbicacion,
            "cat_unidades_medida": CatUnidadMedida, "cat_categorias_producto": CatCategoriaProducto,
            "cat_categorias_materia_prima": CatCategoriaMateriaPrima, "cat_tipos_almacen": CatTipoAlmacen,
            "cat_tipos_movimiento_almacen": CatTipoMovimientoAlmacen, "cat_puestos": CatPuesto,
            "cat_tipos_vehiculo": CatTipoVehiculo, "cat_estados_fisicos": CatEstadoFisico,
            "cat_conceptos_finanzas": CatConceptoFinanzas, "cat_tipos_incidencia": CatTipoIncidencia,
            "cat_bancos_cajas": CatBancoCaja, "cat_tipos_descuento": CatTipoDescuento,
            "cat_tipos_pago_solicitado": CatTipoPagoSolicitado, "cat_estados_orden_venta": CatEstadoOrdenVenta,
            "cat_estados_plan_produccion": CatEstadoPlanProduccion, "cat_estados_orden_empaque": CatEstadoOrdenEmpaque,
            "cat_tipos_movimiento_finanzas": CatTipoMovimientoFinanzas, "cat_estados_deuda_empresa": CatEstadoDeudaEmpresa,
            "cat_tipos_flujo": CatTipoFlujo, "cat_origenes_flujo": CatOrigenFlujo, "cat_periodos": CatPeriodo
        }

        for tabla_key, modelo in mapa_catalogos.items():
            datos = CATALOGOS.get(tabla_key, [])
            for item in datos:
                # Búsqueda flexible (por descripción o nombre)
                criterio = {}
                if hasattr(modelo, 'descripcion'): criterio['descripcion'] = item['descripcion']
                elif hasattr(modelo, 'nombre'): criterio['nombre'] = item['nombre']
                
                if not modelo.query.filter_by(**criterio).first():
                    db.session.add(modelo(**item))
        db.session.commit()

        # 2. INFRAESTRUCTURA
        print("--> Sembrando Infraestructura...")
        for r in RUTAS:
            if not RutaReparto.query.filter_by(descripcion=r['descripcion']).first():
                db.session.add(RutaReparto(**r))
        db.session.commit()

        for alm in ALMACENES:
            if not Almacen.query.filter_by(descripcion=alm['descripcion']).first():
                tipo = CatTipoAlmacen.query.filter_by(nombre=alm['tipo']).first()
                planta = CatPlanta.query.filter_by(descripcion=alm['planta']).first()
                # Búsqueda parcial para Área
                area = CatArea.query.filter(CatArea.descripcion.ilike(f"%{alm['area']}%")).first()
                
                if tipo and planta and area:
                    nuevo = Almacen(descripcion=alm['descripcion'], tipo_id=tipo.id, planta_id=planta.id, area_id=area.id)
                    db.session.add(nuevo)
                    db.session.commit()
                    for ubi in alm['ubicaciones']:
                        db.session.add(UbicacionAlmacen(codigo=ubi['codigo'], notas=ubi['notas'], almacen_id=nuevo.id))
        db.session.commit()

        # 3. PRODUCTOS
        print("--> Sembrando Inventario Maestro...")
        for p in PRODUCTOS:
            if not Producto.query.filter_by(sku=p['sku']).first():
                cat = CatCategoriaProducto.query.filter_by(nombre=p['categoria']).first()
                uni = CatUnidadMedida.query.filter_by(nombre=p['unidad']).first()
                if cat and uni:
                    # Quitamos campos que no son columnas directas
                    data = {k: v for k, v in p.items() if k not in ['categoria', 'unidad', 'imagen']}
                    prod = Producto(**data)
                    prod.categoria_id, prod.unidad_id = cat.id, uni.id
                    prod.imagen_producto = p.get('imagen')
                    db.session.add(prod)
        
        for mp in MATERIAS_PRIMAS:
            if not MateriaPrima.query.filter_by(sku=mp['sku']).first():
                cat = CatCategoriaMateriaPrima.query.filter_by(nombre=mp['categoria']).first()
                uni = CatUnidadMedida.query.filter_by(nombre=mp['unidad']).first()
                if cat and uni:
                    data = {k: v for k, v in mp.items() if k not in ['categoria', 'unidad', 'imagen']}
                    mat = MateriaPrima(**data)
                    mat.categoria_id, mat.unidad_id = cat.id, uni.id
                    mat.imagen_materia = mp.get('imagen')
                    db.session.add(mat)
        db.session.commit()

        # 4. USUARIOS
        print("--> Sembrando Usuarios...")
        for u in USUARIOS:
            if not Usuario.query.filter_by(email_acceso=u['email']).first():
                puesto = CatPuesto.query.filter_by(nombre=u['puesto']).first()
                data = u.copy()
                del data['password_raw'], data['puesto'], data['email']
                
                user = Usuario(**data)
                user.email_acceso = u['email']
                user.password_hash = generate_password_hash(u['password_raw'])
                if puesto: user.puesto_id = puesto.id
                db.session.add(user)
        db.session.commit()

        # 5. CLIENTES
        print("--> Sembrando Clientes...")
        for c in CLIENTES:
            if not Cliente.query.filter_by(nombre_negocio=c['nombre_negocio']).first():
                ruta = RutaReparto.query.filter_by(descripcion=c['ruta_asignada']).first()
                data = c.copy()
                precios = data.pop('precios_especiales', [])
                del data['ruta_asignada']
                
                cte = Cliente(**data)
                if ruta: cte.ruta_id = ruta.id
                db.session.add(cte)
                db.session.commit()

                for pe in precios:
                    prod = Producto.query.filter_by(sku=pe['producto_sku']).first()
                    td = CatTipoDescuento.query.filter_by(descripcion=pe['tipo_descuento']).first()
                    if prod and td:
                        db.session.add(PrecioEspecialCliente(cliente_id=cte.id, producto_id=prod.id, tipo_descuento_id=td.id, valor_descuento=pe['valor']))
        db.session.commit()
        
        print("\n✅ ¡SEMBRADO COMPLETADO! La base de datos tiene vida.")

if __name__ == "__main__":
    try:
        run_seeds()
    except Exception as e:
        print(f"❌ ERROR: {e}")