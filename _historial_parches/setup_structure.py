import os
import pathlib

# --- CONFIGURACIÓN DEL BLUEPRINT (ESPECIFICACIÓN DE ARQUITECTURA) ---
# Definimos la estructura exacta aprobada en la Hoja de Método
PROJECT_STRUCTURE = {
    "directories": [
        "app",
        "app/blueprints",   # Controladores
        "app/models",       # Base de Datos
        "app/static",       # Assets Públicos
        "app/static/css",
        "app/static/js",
        "app/static/img",
        "app/templates",    # Vistas HTML
        "instance"          # DB Local (Protegida)
    ],
    "files": [
        "app/__init__.py",              # Inicializador del Core
        "app/blueprints/__init__.py",   # Inicializador de Paquete
        "app/models/__init__.py",       # Inicializador de Paquete
        "run.py",                       # Entry Point
        "config.py",                    # Variables de Entorno
        "requirements.txt"              # Lista de materiales (BOM)
    ]
}

def create_structure():
    print(f"[ INFO ] Iniciando despliegue de arquitectura GelMexSys 2.0...")
    
    # 1. Crear Directorios
    for directory in PROJECT_STRUCTURE["directories"]:
        path = pathlib.Path(directory)
        if not path.exists():
            os.makedirs(path)
            print(f"[ OK ] Directorio creado: {directory}/")
        else:
            print(f"[ SKIP ] El directorio ya existe: {directory}/")

    # 2. Crear Archivos Vacíos (Touch)
    for file in PROJECT_STRUCTURE["files"]:
        path = pathlib.Path(file)
        if not path.exists():
            # Crear archivo vacío
            with open(path, 'w') as f:
                pass 
            print(f"[ OK ] Archivo base generado: {file}")
        else:
            print(f"[ SKIP ] El archivo ya existe: {file}")

    print("-" * 40)
    print(f"[ FIN ] Despliegue de estructura completado con éxito.")

if __name__ == "__main__":
    create_structure()