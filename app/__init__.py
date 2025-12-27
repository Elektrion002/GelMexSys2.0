# app/__init__.py
from flask import Flask
from config import config
from app.extensions import db

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    with app.app_context():
        # Importamos modelos para que SQLAlchemy sepa de ellos
        from app.models import catalogs, users, infrastructure, products, clients
        
        # OJO: Ya no necesitamos db.create_all() siempre, porque ya existen.
        # Pero no estorba dejarlo por seguridad en desarrollo.
        db.create_all()

    # --- AQUÍ REGISTRAMOS EL NUEVO BLUEPRINT ---
    from app.blueprints.api_test import api_bp
    app.register_blueprint(api_bp)
    
    return app