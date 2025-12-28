# app/__init__.py
from flask import Flask
from config import config
from app.extensions import db
from flask_login import LoginManager # <--- 1. Importar

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    # --- CONFIGURACIÓN DE LOGIN (NUEVO) ---
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # A dónde ir si no estás logueado
    login_manager.login_message = "Debes iniciar sesión para acceder a este sistema."
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    # Función para cargar usuario desde la Cookie
    from app.models.users import Usuario
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    # --------------------------------------

    with app.app_context():
        from app.models import catalogs, users, infrastructure, products, clients, stock, orders 
        db.create_all()

    # --- REGISTRO DE BLUEPRINTS ---
    from app.blueprints.api_test import api_bp
    app.register_blueprint(api_bp)

    from app.blueprints.home import home_bp
    app.register_blueprint(home_bp)

    from app.blueprints.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.blueprints.inventory import inventory_bp
    app.register_blueprint(inventory_bp)

    from app.blueprints.sales import sales_bp
    app.register_blueprint(sales_bp)

    from app.blueprints.production import production_bp
    app.register_blueprint(production_bp)
 
    
    return app