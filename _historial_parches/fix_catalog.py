from app import create_app
from app.extensions import db
from app.models.catalogs import CatTipoMovimientoAlmacen

app = create_app()

with app.app_context():
    print("🔧 Agregando opción 'INVENTARIO_INICIAL' al catálogo...")
    
    # Verificamos si ya existe para no duplicar
    existe = CatTipoMovimientoAlmacen.query.filter_by(descripcion="INVENTARIO_INICIAL").first()
    
    if not existe:
        nuevo = CatTipoMovimientoAlmacen(descripcion="INVENTARIO_INICIAL")
        db.session.add(nuevo)
        db.session.commit()
        print("✅ ¡LISTO! Opción creada. Ahora aparecerá en el sistema.")
    else:
        print("ℹ️ La opción ya existía.")