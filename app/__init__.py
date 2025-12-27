# app/__init__.py
from flask import Flask
from config import config
from app.extensions import db

def create_app(config_name='default'):
    # 1. Instanciar Flask
    app = Flask(__name__)

    # 2. Cargar Configuración (Dev, Prod, etc.)
    app.config.from_object(config[config_name])

    # 3. Conectar Base de Datos
    db.init_app(app)

    # 4. Cargar Modelos (Contexto de Aplicación)
    # Esto es CRÍTICO: Si no importamos los modelos aquí, SQLAlchemy no sabrá que existen
    # y no creará las tablas.
    with app.app_context():
        from app.models import catalogs
        from app.models import users
        from app.models import infrastructure
        from app.models import products
        from app.models import clients
        
        # Opcional: Crear tablas automáticamente si no existen (Solo desarrollo)
        # En producción usaremos Migraciones (Alembic)
        db.create_all()

    # 5. Registrar Blueprints (Rutas) - Lo haremos más adelante
    # from app.blueprints.home import home_bp
    # app.register_blueprint(home_bp)

    return app