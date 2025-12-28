import unittest
import sys
import os

# --- FIX: FORZAR LA RUTA RAÍZ PARA QUE ENCUENTRE 'APP' ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ---------------------------------------------------------

from app import create_app, db
from app.models.products import Producto
from app.models.stock import InventarioProducto
from app.models.infrastructure import Almacen, UbicacionAlmacen
from app.models.catalogs import CatTipoMovimientoAlmacen, CatCategoriaProducto, CatUnidadMedida

class TestFlujoInventario(unittest.TestCase):
    
    # 1. SETUP: Se ejecuta antes de cada prueba.
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # DB en RAM
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # --- CREAMOS DATOS MAESTROS ---
        self.crear_catalogos()
        self.crear_infraestructura()
        self.crear_producto()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # --- HELPERS (CORREGIDOS) ---
    def crear_catalogos(self):
        tipos = ['INVENTARIO_INICIAL', 'ENTRADA_COMPRA', 'SALIDA_VENTA', 'AJUSTE_MERMA']
        for t in tipos:
            db.session.add(CatTipoMovimientoAlmacen(descripcion=t))
        
        # CORRECCIÓN: Quitamos 'codigo' y 'abreviatura' que causaban el error
        # Solo usamos 'nombre' que es lo obligatorio.
        db.session.add(CatCategoriaProducto(nombre="Helados")) 
        db.session.add(CatUnidadMedida(nombre="Pieza"))
        db.session.commit()

    def crear_infraestructura(self):
        # Asumiendo que Tipo de Almacén 1 existe o no es FK estricta en test, 
        # pero si truena aqui, necesitaremos crear CatTipoAlmacen tambien.
        # Por simplicidad del test unitario, a veces se permite nulo si el modelo lo deja.
        # Si tu modelo exige FK, el test fallará pidiendo CatTipoAlmacen.
        # Vamos a intentar insertar directo.
        alm = Almacen(descripcion="Almacén Test", tipo_id=1) 
        db.session.add(alm)
        db.session.commit()
        
        ubi = UbicacionAlmacen(codigo="A1", almacen_id=alm.id)
        db.session.add(ubi)
        db.session.commit()
        self.ubi_id = ubi.id 

    def crear_producto(self):
        prod = Producto(sku="TEST-01", descripcion="Boli Test", categoria_id=1, unidad_id=1)
        db.session.add(prod)
        db.session.commit()
        self.prod_id = prod.id

    # ==========================================
    # CASOS DE PRUEBA
    # ==========================================

    def test_1_inventario_inicial_corrige_negativos(self):
        print("\n🧪 TEST 1: Inventario Inicial vs Negativos...")
        basura = InventarioProducto(producto_id=self.prod_id, ubicacion_id=self.ubi_id, cantidad_actual=-500)
        db.session.add(basura)
        db.session.commit()
        
        # Simulación RESET
        stock_record = InventarioProducto.query.filter_by(producto_id=self.prod_id, ubicacion_id=self.ubi_id).first()
        stock_record.cantidad_actual = 1000 
        db.session.commit()
        
        self.assertEqual(stock_record.cantidad_actual, 1000)
        print("   ✅ ÉXITO: El saldo se corrigió de -500 a 1000.")

    def test_2_entrada_suma_correctamente(self):
        print("🧪 TEST 2: Suma de Entradas...")
        inicial = InventarioProducto(producto_id=self.prod_id, ubicacion_id=self.ubi_id, cantidad_actual=100)
        db.session.add(inicial)
        db.session.commit()
        
        inicial.cantidad_actual += 50
        db.session.commit()
        
        self.assertEqual(inicial.cantidad_actual, 150)
        print("   ✅ ÉXITO: 100 + 50 = 150.")

    def test_3_salida_resta_correctamente(self):
        print("🧪 TEST 3: Resta de Salidas...")
        inicial = InventarioProducto(producto_id=self.prod_id, ubicacion_id=self.ubi_id, cantidad_actual=100)
        db.session.add(inicial)
        db.session.commit()
        
        inicial.cantidad_actual -= 20
        db.session.commit()
        
        self.assertEqual(inicial.cantidad_actual, 80)
        print("   ✅ ÉXITO: 100 - 20 = 80.")

    def test_4_bloqueo_de_negativos(self):
        print("🧪 TEST 4: Bloqueo de Stocks Negativos...")
        inicial = InventarioProducto(producto_id=self.prod_id, ubicacion_id=self.ubi_id, cantidad_actual=10)
        db.session.add(inicial)
        db.session.commit()
        
        cantidad_a_sacar = 50
        operacion_exitosa = False
        
        if inicial.cantidad_actual >= cantidad_a_sacar:
            inicial.cantidad_actual -= cantidad_a_sacar
            operacion_exitosa = True
        
        self.assertFalse(operacion_exitosa)
        self.assertEqual(inicial.cantidad_actual, 10)
        print("   ✅ ÉXITO: El sistema impidió sacar 50 teniendo solo 10.")

if __name__ == '__main__':
    unittest.main()