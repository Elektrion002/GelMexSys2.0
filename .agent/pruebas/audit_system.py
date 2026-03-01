from app import create_app
from app.extensions import db
from sqlalchemy import inspect

app = create_app()

def audit_schema():
    with app.app_context():
        inspector = inspect(db.engine)
        print("=== AUDITORÍA DE ESTRUCTURA ACTUAL ===\n")

        # 1. REVISAR ORDENES DE VENTA
        print("--- TABLA: ordenes_venta ---")
        columns = inspector.get_columns('ordenes_venta')
        for col in columns:
            print(f"- {col['name']} ({col['type']})")
        
        # 2. REVISAR DETALLES (Vital para ver si tenemos cantidad_entregada)
        print("\n--- TABLA: orden_venta_detalles ---")
        columns = inspector.get_columns('orden_venta_detalles')
        for col in columns:
            print(f"- {col['name']} ({col['type']})")

        # 3. REVISAR CLIENTES (Vital para saldos y créditos)
        print("\n--- TABLA: clientes ---")
        columns = inspector.get_columns('clientes')
        for col in columns:
            print(f"- {col['name']} ({col['type']})")

        # 4. CHECAR SI YA EXISTE PAGOS (Para no duplicar)
        if inspector.has_table('pagos'):
            print("\n--- TABLA: pagos (YA EXISTE) ---")
            columns = inspector.get_columns('pagos')
            for col in columns:
                print(f"- {col['name']} ({col['type']})")
        else:
            print("\n--- TABLA: pagos (NO EXISTE AÚN) ---")

if __name__ == '__main__':
    audit_schema()