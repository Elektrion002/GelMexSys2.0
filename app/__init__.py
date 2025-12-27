from flask import Flask
from config import config

def create_app(config_name='default'):
    # Creamos la instancia de Flask
    app = Flask(__name__)

    # Cargamos la configuración (Dev o Prod)
    app.config.from_object(config[config_name])

    # Aquí luego conectaremos la Base de Datos y los Blueprints (Módulos)
    # Por ahora, solo queremos que arranque.
    
    # Ruta de prueba rápida para ver si jala
    @app.route('/')
    def index():
        return "<h1>🍦 GelMexSys 2.0</h1><p>Sistema Operativo y Listo.</p>"

    return app