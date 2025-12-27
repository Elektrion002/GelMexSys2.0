import os

class Config:
    # Llave de seguridad (luego la cambiamos por una real en producción)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-super-secreta-desarrollo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    # Base de datos SQLite local (se crea sola en la carpeta instance)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'gelmex_dev.db')

class ProductionConfig(Config):
    DEBUG = False
    # Aquí iría la conexión a PostgreSQL real
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# Diccionario para elegir fácil
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}