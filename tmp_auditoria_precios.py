from app import create_app
from app.extensions import db
from app.models.clients import Cliente, PrecioEspecialCliente
from app.models.products import Producto

app = create_app()
with app.app_context():
    count = PrecioEspecialCliente.query.count()
    print(f"Total Precios Especiales: {count}")
    if count > 0:
        ejemplo = PrecioEspecialCliente.query.first()
        print(f"Cliente: {ejemplo.cliente.nombre_negocio}")
        print(f"Producto: {ejemplo.producto.descripcion}")
        print(f"Valor Descuento: {ejemplo.valor_descuento}")
        # Intentar ver si hay tipos de descuento
        from sqlalchemy import text
        tipos = db.session.execute(text("SELECT * FROM cat_tipos_descuento")).fetchall()
        for t in tipos:
            print(f"Tipo Descuento ID: {t[0]}, Nombre: {t[1]}")
