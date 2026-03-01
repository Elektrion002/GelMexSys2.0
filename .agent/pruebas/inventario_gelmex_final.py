import os
import sys
import csv
import re
from sqlalchemy import inspect, text

# Localización para encontrar 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.extensions import db

def generar_inventario():
    app = create_app('development')
    resultado_dir = os.path.join(os.path.dirname(__file__), 'resultados')
    if not os.path.exists(resultado_dir):
        os.makedirs(resultado_dir)

    with app.app_context():
        # --- 1. AUDITORÍA DE TABLAS Y ESQUEMA ---
        inspector = inspect(db.engine)
        tablas = inspector.get_table_names()
        
        archivo_tablas = os.path.join(resultado_dir, 'inventario_tablas_gelmex.csv')
        with open(archivo_tablas, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['TABLA', 'COLUMNA', 'TIPO', 'NULO', 'DEFAULT', 'MUESTRA_DATOS (Top 1)'])
            
            for tabla in tablas:
                # Obtener muestra real
                muestra = ""
                try:
                    res = db.session.execute(text(f"SELECT * FROM {tabla} LIMIT 1")).fetchone()
                    if res:
                        # Convertir a string limitado para CSV
                        muestra = str(dict(res._mapping))[:200]
                    else:
                        muestra = "TABLA VACÍA"
                except Exception:
                    muestra = "ERROR AL LEER"
                
                columnas = inspector.get_columns(tabla)
                for col in columnas:
                    writer.writerow([tabla, col['name'], col['type'], col['nullable'], col['default'], muestra])
        
        print(f"✅ CSV de Tablas generado: {archivo_tablas}")

        # --- 2. AUDITORÍA DE CRUD EN CÓDIGO ---
        directorio_app = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../app'))
        archivo_crud = os.path.join(resultado_dir, 'mapeo_crud_gelmex.csv')
        
        # Patrones CRUD comunes en Flask-SQLAlchemy
        patrones = [
            (r'db\.session\.add\(', 'CREATE (INSERT)'),
            (r'db\.session\.delete\(', 'DELETE'),
            (r'db\.session\.commit\(', 'COMMIT'),
            (r'\.query\.get\(', 'READ (GET)'),
            (r'\.query\.filter\(', 'READ (FILTER)'),
            (r'\.query\.all\(', 'READ (ALL)'),
            (r'\.query\.first\(', 'READ (FIRST)'),
            (r'db\.session\.execute\(', 'SQL DIRECTO')
        ]

        with open(archivo_crud, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ARCHIVO', 'LINEA', 'TIPO_OPERACION', 'CONTENIDO_CODIGO'])
            
            for root, dirs, files in os.walk(directorio_app):
                for file in files:
                    if file.endswith('.py') and not file.endswith('.bk'):
                        ruta_completa = os.path.join(root, file)
                        ruta_relativa = os.path.relpath(ruta_completa, directorio_app)
                        
                        with open(ruta_completa, 'r', encoding='utf-8', errors='ignore') as p:
                            for i, line in enumerate(p, 1):
                                line_clean = line.strip()
                                for pattern, op_name in patrones:
                                    if re.search(pattern, line_clean):
                                        writer.writerow([ruta_relativa, i, op_name, line_clean])

        print(f"✅ CSV de Mapeo CRUD generado: {archivo_crud}")

if __name__ == "__main__":
    generar_inventario()
