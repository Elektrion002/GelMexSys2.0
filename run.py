# run.py
from dotenv import load_dotenv
load_dotenv()
import os
from app import create_app

config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)

if __name__ == '__main__':
    print(f"--> Arrancando GelMexSys en modo: {config_name}")
    print("--> ACCESO EXTERNO HABILITADO: Usa tu IP para entrar desde el cel.")
    
    # AGREGAMOS host='0.0.0.0'
    app.run(host='0.0.0.0', port=5000)
