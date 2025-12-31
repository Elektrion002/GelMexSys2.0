from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("🔧 Actualizando tabla de Órdenes de Producción...")
    try:
        # 1. Columna para lo que REALMENTE salió de la máquina
        db.session.execute(text("ALTER TABLE ordenes_produccion ADD COLUMN cantidad_producida_real FLOAT DEFAULT 0;"))
        print("✅ Columna 'cantidad_producida_real' agregada.")
    except Exception as e:
        print(f"ℹ️ Aviso: {e}")

    try:
        # 2. Columna para notas del Maestro (Excusas de por qué salió menos)
        db.session.execute(text("ALTER TABLE ordenes_produccion ADD COLUMN notas_produccion TEXT;"))
        print("✅ Columna 'notas_produccion' agregada.")
    except Exception as e:
        print(f"ℹ️ Aviso: {e}")
        
    db.session.commit()
    print("🚀 Base de datos lista para la Realidad Operativa.")