# setup_db.py
import sys
import os

# Agregamos el directorio actual al path para evitar errores de módulos
sys.path.append(os.getcwd())

from app import create_app
from app.extensions import db

def init_database():
    print("--> Inicializando aplicación Flask...")
    # 1. Instanciamos la app AQUÍ ADENTRO para evitar el error de variable
    app = create_app()

    with app.app_context():
        print("🔧 INICIANDO CONSTRUCCIÓN DE BASE DE DATOS...")
        print(f"--> Destino: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        try:
            # 2. Importar Modelos (Esto fuerza a SQLAlchemy a reconocer las tablas)
            print("--> Leyendo planos (Modelos)...")
            # Importamos dentro del contexto para asegurar que db esté listo
            from app.models import catalogs
            from app.models import users
            from app.models import infrastructure
            from app.models import products
            from app.models import clients
            print("    [OK] Modelos cargados en memoria.")

            # 3. Crear Tablas
            print("--> Ejecutando CREATE TABLE en PostgreSQL...")
            db.create_all()
            
            print("-" * 40)
            print("✅ ¡ÉXITO! TABLAS CREADAS CORRECTAMENTE.")
            print("-" * 40)
            print("Instrucciones:")
            print("1. Ve a pgAdmin 4.")
            print("2. Dale clic derecho a 'Tables' -> Refresh.")
            print("3. Si ves la lista de tablas, ejecuta 'python seed_runner.py' para llenar los datos.")
            
        except Exception as e:
            print("\n❌ ERROR CRÍTICO AL CONECTAR CON LA BD:")
            print(f"{e}")
            print("\nPOSIBLES CAUSAS:")
            print("1. La contraseña en config.py está mal.")
            print("2. El servidor de PostgreSQL no está corriendo.")
            print("3. La base de datos 'gelmex_db' no existe (Créala en pgAdmin).")

if __name__ == "__main__":
    init_database()