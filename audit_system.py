import os
from app import create_app
from app.extensions import db
from sqlalchemy import text, inspect

# Configuración de colores para la consola
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def check_table_health(inspector, table_name, required_cols=None):
    """Verifica si la tabla existe y tiene columnas críticas."""
    if not inspector.has_table(table_name):
        print(f"   {Colors.FAIL}[CRÍTICO] La tabla '{table_name}' NO EXISTE.{Colors.ENDC}")
        return False
    
    if required_cols:
        cols = [c['name'] for c in inspector.get_columns(table_name)]
        missing = [rc for rc in required_cols if rc not in cols]
        if missing:
            print(f"   {Colors.FAIL}[ERROR] Tabla '{table_name}' incompleta. Faltan columnas: {missing}{Colors.ENDC}")
            return False
        else:
            print(f"   [OK] Tabla '{table_name}' estructuralmente correcta.")
            # Imprimir columnas clave encontradas para validación visual
            found_keys = [c for c in cols if c in required_cols]
            print(f"        -> Columnas validadas: {found_keys}")
    
    return True

def count_records(table_name):
    """Cuenta registros reales usando SQL directo."""
    try:
        sql = text(f"SELECT COUNT(*) FROM {table_name}")
        count = db.session.execute(sql).scalar()
        color = Colors.OKGREEN if count > 0 else Colors.WARNING
        print(f"   {color}Registros en '{table_name}': {count}{Colors.ENDC}")
        return count
    except Exception as e:
        print(f"   {Colors.FAIL}Error leyendo '{table_name}': {e}{Colors.ENDC}")
        return 0

def audit_database():
    app = create_app()
    with app.app_context():
        print(f"\n{Colors.HEADER}{'='*70}")
        print(f" AUDITORÍA MCP (MODEL CONTEXT PROTOCOL) - GELMEXSYS 2.0")
        print(f"{'='*70}{Colors.ENDC}\n")

        inspector = inspect(db.engine)

        # ---------------------------------------------------------
        # FASE 1: INFRAESTRUCTURA DE ALMACÉN (El terreno del Almacenista)
        # ---------------------------------------------------------
        print(f"{Colors.BOLD}FASE 1: PREPARACIÓN DE ALMACENES (Infraestructura){Colors.ENDC}")
        
        # Validar si existen almacenes y, más importante, UBICACIONES (Pasillos/Racks)
        # Sin ubicaciones, el almacenista no puede "ubicar" el producto.
        if check_table_health(inspector, 'almacenes') and check_table_health(inspector, 'ubicaciones_almacen', ['codigo', 'almacen_id']):
            cnt_alm = count_records('almacenes')
            cnt_ubi = count_records('ubicaciones_almacen')
            
            if cnt_alm > 0 and cnt_ubi == 0:
                print(f"   {Colors.FAIL}>>> ALERTA DE PROCESO: Tienes almacenes pero NO tienes ubicaciones.{Colors.ENDC}")
                print("       El Almacenista no podrá guardar nada porque no hay 'Pasillos' definidos.")

        # ---------------------------------------------------------
        # FASE 2: MODELO DE INVENTARIO (La divergencia detectada)
        # ---------------------------------------------------------
        print(f"\n{Colors.BOLD}FASE 2: MODELO DE INVENTARIO (Validación de Nombres){Colors.ENDC}")
        
        # Aquí validamos si postgres tiene 'cantidad_actual' o 'cantidad_fisica'
        inv_cols = [c['name'] for c in inspector.get_columns('inventario_productos')] if inspector.has_table('inventario_productos') else []
        
        print(f"   Columnas en DB Real: {inv_cols}")
        if 'cantidad_actual' in inv_cols:
            print(f"   {Colors.OKGREEN}✓ PostgreSQL usa 'cantidad_actual'. (Asegúrate que stock.py coincida){Colors.ENDC}")
        elif 'cantidad_fisica' in inv_cols:
            print(f"   {Colors.OKGREEN}✓ PostgreSQL usa 'cantidad_fisica'. (Asegúrate que stock.py coincida){Colors.ENDC}")
        else:
            print(f"   {Colors.FAIL}❌ NO SE ENCONTRÓ COLUMNA DE CANTIDAD. El sistema tronará.{Colors.ENDC}")

        # Revisamos si hay Kárdex para auditoría
        check_table_health(inspector, 'historial_movimientos', ['tipo_movimiento', 'cantidad', 'usuario_id', 'referencia'])

        # ---------------------------------------------------------
        # FASE 3: LOGÍSTICA (El terreno del Repartidor)
        # ---------------------------------------------------------
        print(f"\n{Colors.BOLD}FASE 3: LOGÍSTICA Y RUTAS (Preparación para Entrega){Colors.ENDC}")
        
        # El proceso dice que el repartidor sube cajas según su ruta. ¿Hay rutas?
        check_table_health(inspector, 'rutas_reparto', ['descripcion'])
        count_records('rutas_reparto')
        
        check_table_health(inspector, 'vehiculos', ['placas', 'asignado'])
        count_records('vehiculos')

        # ---------------------------------------------------------
        # FASE 4: SIMULACIÓN DE FLUJO DE DATOS (Data Flow)
        # ---------------------------------------------------------
        print(f"\n{Colors.BOLD}FASE 4: DIAGNÓSTICO DE FLUJO{Colors.ENDC}")
        
        # Revisamos estados de órdenes para ver si el "Programador" tiene chamba
        try:
            sql = text("SELECT estado, COUNT(*) FROM ordenes_venta GROUP BY estado")
            res = db.session.execute(sql).fetchall()
            if res:
                print("   Estado de las Órdenes:")
                for r in res:
                    print(f"   - {r[0]}: {r[1]}")
            else:
                print(f"   {Colors.WARNING}No hay órdenes activas.{Colors.ENDC}")
        except:
            pass

        print(f"\n{Colors.HEADER}CONCLUSIÓN DEL PROTOCOLO:{Colors.ENDC}")
        print("Si FASE 1 tiene Almacenes pero 0 Ubicaciones -> Bloqueante para Módulo Almacén.")
        print("Si FASE 2 muestra nombres distintos a tu código Python -> Error 500 seguro.")
        print("Si FASE 3 tiene 0 Rutas -> El módulo de Ventas no podrá asignar clientes correctamente.")

if __name__ == "__main__":
    audit_database()