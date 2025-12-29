from app import create_app
from app.models.infrastructure import UbicacionAlmacen

app = create_app()

with app.app_context():
    print("-" * 30)
    print(f"TABLA REAL: {UbicacionAlmacen.__tablename__}")
    print("-" * 30)
    print("COLUMNAS EN EL MODELO:")
    # Esto nos dirá exactamente qué atributos tiene la clase Python
    for column in UbicacionAlmacen.__table__.columns:
        print(f" >> {column.name}")
    print("-" * 30)