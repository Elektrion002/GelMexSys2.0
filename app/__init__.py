from flask import Flask
from config import config
from app.extensions import db
from flask_login import LoginManager 

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    # --- CONFIGURACIÓN DE LOGIN ---
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
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
        # IMPORTANTE: Agregamos 'finance' para que detecte los modelos financieros
        from app.models import catalogs, users, infrastructure, products, clients, stock, orders, payments, finance
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

    from app.blueprints.reception import reception_bp
    app.register_blueprint(reception_bp)

    from app.blueprints.sales import sales_bp
    app.register_blueprint(sales_bp)

    from app.blueprints.production import production_bp
    app.register_blueprint(production_bp)

    from app.blueprints.shipping import shipping_bp
    app.register_blueprint(shipping_bp)
    
    from app.blueprints.logistics import logistics_bp
    app.register_blueprint(logistics_bp)

    # Módulo de Finanzas
    from app.blueprints.finance import finance_bp
    app.register_blueprint(finance_bp)

    from app.blueprints.clients import clients_bp
    app.register_blueprint(clients_bp)

    from app.blueprints.users import users_bp
    app.register_blueprint(users_bp)

    from app.blueprints.product_admin import product_admin_bp
    app.register_blueprint(product_admin_bp)

    from app.blueprints.catalogs_admin import catalogs_admin_bp
    app.register_blueprint(catalogs_admin_bp)

    return app