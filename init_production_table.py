from app import create_app, db
# Importamos el modelo para que SQLAlchemy sepa que existe
from app.models.production import OrdenProduccion 

app = create_app()

with app.app_context():
    print("🔧 Verificando tablas faltantes...")
    # Esto crea SOLO las tablas que no existen (ordenes_produccion)
    db.create_all()
    print("✅ Tabla 'ordenes_produccion' creada exitosamente en PostgreSQL.")