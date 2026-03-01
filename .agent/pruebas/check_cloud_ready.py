import os

def check_ready():
    print("\n=== REVISIÓN DE SALUD PARA LA NUBE ===")
    
    # 1. Verificar carpetas de carga
    uploads = ['app/static/uploads/usuarios', 'app/static/uploads/productos', 'app/static/uploads/clientes']
    for path in uploads:
        if os.path.exists(path):
            print(f"✅ Carpeta encontrada: {path}")
        else:
            print(f"❌ FALTA CARPETA: {path}")

    # 2. Verificar requirements
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            content = f.read()
            if 'gunicorn' in content.lower():
                print("✅ Gunicorn (Servidor Pro) está en requirements.")
            else:
                print("❌ FALTA: Agrega 'gunicorn' a requirements.txt")
            
            if 'psycopg2' in content.lower():
                print("✅ Driver de PostgreSQL encontrado.")
            else:
                print("❌ FALTA: Agrega 'psycopg2-binary' a requirements.txt")
    else:
        print("❌ CRÍTICO: No existe requirements.txt")

    # 3. Verificar Procfile
    if os.path.exists('Procfile'):
        with open('Procfile', 'r') as f:
            if 'gunicorn' in f.read():
                print("✅ Procfile configurado correctamente.")
            else:
                print("❌ Procfile existe pero el contenido es incorrecto.")
    else:
        print("❌ FALTA: Archivo Procfile")

    # 4. Verificar punto de entrada
    if os.path.exists('run.py'):
        print("✅ Archivo run.py (Entry Point) encontrado.")
    else:
        print("❌ FALTA: Archivo run.py")

if __name__ == "__main__":
    check_ready()