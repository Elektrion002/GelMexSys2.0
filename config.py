import os

class Config:
    # Llave de seguridad (luego la cambiamos por una real en producción)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-super-secreta-desarrollo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    # Conexión a PostgreSQL Local
    # Formato: postgresql://usuario:password@localhost:puerto/nombre_db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'postgresql://postgres:admin12345@localhost:5432/gelmex_db'

class ProductionConfig(Config):
    DEBUG = False
    # Aquí iría la conexión a PostgreSQL real
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# Diccionario para elegir fácil
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}
