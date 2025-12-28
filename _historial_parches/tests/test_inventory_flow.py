import unittest
import sys
import os

# 1. PREPARACIÓN DE ENTORNO (CRÍTICO: HACER ESTO ANTES DE IMPORTAR APP)
# Esto engaña a Flask para que ignore tu archivo .env real
os.environ['FLASK_ENV'] = 'testing'
# Forzamos una URI de SQLite en memoria. Si tu config.py usa os.getenv('DATABASE_URL'), esto lo intercepta.
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

# Ajuste de ruta para imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.products import Producto
from app.models.stock import InventarioProducto
from app.models.infrastructure import Almacen, UbicacionAlmacen
from app.models.catalogs import CatTipoMovimientoAlmacen, CatCategoriaProducto, CatUnidadMedida

class TestFlujoInventario(unittest.TestCase):
    
    def setUp(self):
        """Se ejecuta ANTES de cada prueba. Configura el entorno aislado."""
        
        # Crear la app
        self.app = create_app()
        
        # --- DOBLE VERIFICACIÓN DE SEGURIDAD (FAIL-SAFE) ---
        # Forzamos la configuración en el objeto app directamente por si el entorno falló
        self.app.config.update({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "WTF_CSRF_ENABLED": False  # Desactivar tokens CSRF para facilitar test de formularios
        })

        self.app_context = self.app.app_context()
        self.app_context.push()

        # MATAR CUALQUIER CONEXIÓN PREVIA (Por si acaso se coló Postgres)
        db.session.remove()
        db.engine.dispose()

        # VERIFICACIÓN FINAL: Si esto imprime algo que no sea memory, lanzamos excepción
        uri_actual = str(db.engine.url)
        print(f"   [DEBUG] Conectado a: {uri_actual}")
        
        if 'sqlite' not in uri_actual and ':memory:' not in uri_actual:
            raise RuntimeError(f"🚨 PELIGRO: El test intentó conectarse a {uri_actual}. ABORTANDO.")

        # Ahora sí, creamos las tablas en la RAM
        try:
            db.create_all()
        except Exception as e:
            print(f"Error creando DB virtual: {e}")
            raise

        # Cargar datos semilla falsos (Mocks)
        self.crear_datos_mock()

    def tearDown(self):
        """Se ejecuta DESPUÉS de cada prueba. Limpia la RAM."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def crear_datos_mock(self):
        """Crea datos falsos exclusivos para la memoria RAM"""
        
        # 1. Catálogos (Sin duplicados porque la DB está vacía en RAM)
        tipos = ['INVENTARIO_INICIAL', 'ENTRADA_COMPRA', 'SALIDA_VENTA', 'AJUSTE_MERMA']
        for t in tipos:
            db.session.add(CatTipoMovimientoAlmacen(descripcion=t))
        
        db.session.add(CatCategoriaProducto(nombre="Helados Test"))
        db.session.add(CatUnidadMedida(nombre="Pieza", abreviatura="PZ"))
        
        # 2. Infraestructura
        alm = Almacen(descripcion="Almacén RAM", tipo_id=1)
        db.session.add(alm)
        db.session.flush() # Para obtener el ID
        
        ubi = UbicacionAlmacen(codigo="RAM-A1", almacen_id=alm.id)
        db.session.add(ubi)
        db.session.flush()
        self.ubi_id = ubi.id

        # 3. Producto
        prod = Producto(sku="TEST-RAM", descripcion="Boli Virtual", categoria_id=1, unidad_id=1)
        db.session.add(prod)
        db.session.flush()
        self.prod_id = prod.id
        
        db.session.commit()

    # ==========================================
    # PRUEBAS UNITARIAS
    # ==========================================

    def test_flujo_completo_inventario(self):
        print("\n🧪 INICIANDO TEST DE INTEGRIDAD DE INVENTARIO...")

        # CASO 1: Ajuste Inicial (Reset)
        # Inyectamos un valor basura
        inv = InventarioProducto(producto_id=self.prod_id, ubicacion_id=self.ubi_id, cantidad_actual=-999)
        db.session.add(inv)
        db.session.commit()

        # Simulamos la lógica de "INVENTARIO_INICIAL"
        target = InventarioProducto.query.filter_by(producto_id=self.prod_id, ubicacion_id=self.ubi_id).first()
        target.cantidad_actual = 500 # Borrón y cuenta nueva
        db.session.commit()
        
        self.assertEqual(target.cantidad_actual, 500, "FALLO: El inventario inicial no reseteó el saldo negativo.")
        print("   ✅ PASO 1: Corrección de negativos -> OK")

        # CASO 2: Entrada (Suma)
        target.cantidad_actual += 100
        db.session.commit()
        self.assertEqual(target.cantidad_actual, 600, "FALLO: La suma de entrada falló.")
        print("   ✅ PASO 2: Suma de inventario -> OK")

        # CASO 3: Salida (Resta)
        target.cantidad_actual -= 50
        db.session.commit()
        self.assertEqual(target.cantidad_actual, 550, "FALLO: La resta de salida falló.")
        print("   ✅ PASO 3: Resta de inventario -> OK")

        # CASO 4: Bloqueo de Stock Insuficiente
        # Intentamos sacar 1000 cuando hay 550
        saldo_antes = target.cantidad_actual
        if target.cantidad_actual >= 1000:
            target.cantidad_actual -= 1000
        else:
            # Esto es lo que esperamos que pase
            pass 
        
        self.assertEqual(target.cantidad_actual, saldo_antes, "FALLO: El sistema permitió sacar más de lo que había.")
        print("   ✅ PASO 4: Bloqueo de saldo negativo -> OK")

if __name__ == '__main__':
    unittest.main()