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

def audit_database():
    app = create_app()
    with app.app_context():
        print(f"\n{Colors.HEADER}{'='*60}")
        print(f" AUDITORÍA TÉCNICA GELMEXSYS - ESTADO REAL DEL SISTEMA")
        print(f"{'='*60}{Colors.ENDC}\n")

        inspector = inspect(db.engine)

        # ---------------------------------------------------------
        # 1. INSPECCIÓN DE ESTRUCTURA (LA VERDAD DE POSTGRES)
        # ---------------------------------------------------------
        print(f"{Colors.BOLD}1. INSPECCIÓN DE ESTRUCTURA (Columnas Reales){Colors.ENDC}")
        
        tablas_criticas = ['productos', 'inventario_productos', 'ordenes_venta', 'orden_venta_detalles']
        
        col_maps = {}
        for tabla in tablas_criticas:
            if inspector.has_table(tabla):
                cols = [c['name'] for c in inspector.get_columns(tabla)]
                col_maps[tabla] = cols
                print(f"   [OK] Tabla '{tabla}' detectada. Columnas clave:")
                # Filtramos solo las columnas que nos importan para el cálculo
                claves = [c for c in cols if 'stock' in c or 'cantidad' in c or 'estado' in c]
                print(f"        -> {claves}")
            else:
                print(f"{Colors.FAIL}   [ERROR] La tabla '{tabla}' NO EXISTE en la BD.{Colors.ENDC}")

        # ---------------------------------------------------------
        # 2. ANÁLISIS DE DATOS (CONTENIDO)
        # ---------------------------------------------------------
        print(f"\n{Colors.BOLD}2. ANÁLISIS DE DATOS (¿Qué hay adentro?){Colors.ENDC}")
        
        # A. Revisión de Inventario
        print("   --- INVENTARIO ---")
        try:
            # Intentamos leer con el nombre que vimos en tu consola anterior
            sql_inv = text("SELECT COUNT(*), SUM(cantidad_actual) FROM inventario_productos")
            res_inv = db.session.execute(sql_inv).fetchone()
            print(f"   Registros en Inventario: {res_inv[0]}")
            print(f"   Suma Total Stock Físico: {res_inv[1] if res_inv[1] else 0}")
        except Exception as e:
            print(f"{Colors.FAIL}   Error leyendo inventario: {e}{Colors.ENDC}")

        # B. Revisión de Preventas (El origen del problema)
        print("\n   --- PREVENTAS (ORDENES) ---")
        try:
            sql_orders = text("SELECT estado, COUNT(*) FROM ordenes_venta GROUP BY estado")
            res_orders = db.session.execute(sql_orders).fetchall()
            if not res_orders:
                print(f"{Colors.WARNING}   ⚠️ NO HAY ÓRDENES DE VENTA REGISTRADAS.{Colors.ENDC}")
            for row in res_orders:
                print(f"   Estado '{row[0]}': {row[1]} órdenes")
        except Exception as e:
            print(f"{Colors.FAIL}   Error leyendo órdenes: {e}{Colors.ENDC}")

        # ---------------------------------------------------------
        # 3. SIMULACIÓN DEL CÁLCULO MCP (PRUEBA DE LÓGICA)
        # ---------------------------------------------------------
        print(f"\n{Colors.BOLD}3. SIMULACIÓN DE CÁLCULO (Production Logic){Colors.ENDC}")
        print("   Vamos a tomar el primer producto que encontremos y calcular su necesidad manualmente:")
        
        try:
            # Tomamos un producto al azar
            sql_prod = text("SELECT id, descripcion, stock_ideal, stock_minimo FROM productos LIMIT 1")
            prod = db.session.execute(sql_prod).fetchone()
            
            if prod:
                pid, desc, ideal, minimo = prod
                print(f"   Producto Analizado: {Colors.OKBLUE}{desc}{Colors.ENDC} (ID: {pid})")
                print(f"   > Stock Ideal (Meta): {ideal}")
                print(f"   > Stock Mínimo (Referencia): {minimo}")

                # Calculamos Demanda (CONFIRMADA)
                sql_demanda = text("""
                    SELECT COALESCE(SUM(d.cantidad_pedida), 0) 
                    FROM orden_venta_detalles d 
                    JOIN ordenes_venta o ON d.orden_id = o.id 
                    WHERE d.producto_id = :pid AND o.estado = 'CONFIRMADA'
                """)
                demanda = db.session.execute(sql_demanda, {"pid": pid}).scalar()
                print(f"   > Demanda (Pedidos Nuevos): {demanda}")

                # Calculamos WIP (EN PRODUCCION)
                sql_wip = text("""
                    SELECT COALESCE(SUM(d.cantidad_pedida), 0) 
                    FROM orden_venta_detalles d 
                    JOIN ordenes_venta o ON d.orden_id = o.id 
                    WHERE d.producto_id = :pid AND o.estado = 'PRODUCCION'
                """)
                wip = db.session.execute(sql_wip, {"pid": pid}).scalar()
                print(f"   > WIP (Ya en cocina): {wip}")

                # Calculamos Existencia Real
                sql_existencia = text("SELECT COALESCE(SUM(cantidad_actual), 0) FROM inventario_productos WHERE producto_id = :pid")
                existencia = db.session.execute(sql_existencia, {"pid": pid}).scalar()
                print(f"   > Existencia Real (DB): {existencia}")

                # --- EL DIAGNÓSTICO ---
                print(f"\n   {Colors.BOLD}--- RESULTADO DEL CÁLCULO ---{Colors.ENDC}")
                
                # FÓRMULA: (Demanda + Ideal) - (Existencia + WIP)
                necesidad = (demanda + ideal) - (existencia + wip)
                final = max(0, necesidad)
                
                print(f"   Fórmula: ({demanda} + {ideal}) - ({existencia} + {wip}) = {necesidad}")
                print(f"   {Colors.OKGREEN}A FABRICAR SUGERIDO: {final}{Colors.ENDC}")
                
                if final == 0 and demanda > 0:
                    print(f"   {Colors.OKBLUE}DIAGNÓSTICO: El sistema detecta que la demanda ya está cubierta.{Colors.ENDC}")
                elif final > 0:
                    print(f"   {Colors.WARNING}DIAGNÓSTICO: Falta producto para llegar al ideal.{Colors.ENDC}")
            else:
                print("   No hay productos en la base de datos.")

        except Exception as e:
            print(f"{Colors.FAIL}Error en la simulación: {str(e)}{Colors.ENDC}")

if __name__ == "__main__":
    audit_database()