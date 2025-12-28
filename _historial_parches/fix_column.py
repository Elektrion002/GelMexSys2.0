from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("🔧 Reparando tabla 'inventario_productos'...")
    try:
        # Comando SQL directo para agregar la columna que falta
        sql = text("ALTER TABLE inventario_productos ADD COLUMN cantidad_reservada FLOAT DEFAULT 0.0;")
        db.session.execute(sql)
        db.session.commit()
        print("✅ ¡ÉXITO! Columna 'cantidad_reservada' agregada correctamente.")
    except Exception as e:
        print(f"⚠️ Aviso (puede que ya exista): {e}")