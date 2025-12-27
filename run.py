import os
from app import create_app

# Leemos en qué modo estamos (por defecto Desarrollo)
config_name = os.getenv('FLASK_CONFIG') or 'default'

# Creamos la app
app = create_app(config_name)

if __name__ == '__main__':
    print(f"--> Arrancando GelMexSys en modo: {config_name}")
    app.run()