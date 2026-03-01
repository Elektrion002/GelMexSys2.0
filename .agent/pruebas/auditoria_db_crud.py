import os
import sys
import csv
import json
from sqlalchemy import inspect, text

# Ajuste de ruta para encontrar 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.extensions import db

def auditoria_completa():
    app = create_app('development')
    
    with app.app_context():
        inspector = inspect(db.engine)
        tablas = inspector.get_table_names()
        
        resultado_dir = os.path.join(os.path.dirname(__file__), 'resultados')
        if not os.path.exists(resultado_dir):
            os.makedirs(resultado_dir)
            
        repo_path = os.path.join(resultado_dir, 'reporte_arquitectura.md')
        
        with open(repo_path, 'w', encoding='utf-8') as f:
            f.write("# Reporte de Auditoría de Arquitectura GelMex\n\n")
            
            for tabla in tablas:
                f.write(f"## Tabla: `{tabla}`\n")
                
                # Obtener columnas
                columnas = inspector.get_columns(tabla)
                f.write("### Esquema\n")
                f.write("| Columna | Tipo | Nulo | Default |\n")
                f.write("| --- | --- | --- | --- |\n")
                for col in columnas:
                    f.write(f"| {col['name']} | {col['type']} | {col['nullable']} | {col['default']} |\n")
                
                # Obtener Muestra
                f.write("\n### Muestra de Datos (Top 3)\n")
                try:
                    query = text(f"SELECT * FROM {tabla} LIMIT 3")
                    result = db.session.execute(query)
                    rows = result.fetchall()
                    
                    if rows:
                        keys = result.keys()
                        f.write("| " + " | ".join(keys) + " |\n")
                        f.write("| " + " | ".join(["---"] * len(keys)) + " |\n")
                        for row in rows:
                            # Sanitizar datos para markdown (evitar pipes)
                            row_str = [str(v).replace('|', '\\|') if v is not None else 'NULL' for v in row]
                            f.write("| " + " | ".join(row_str) + " |\n")
                    else:
                        f.write("*Tabla vacía*\n")
                except Exception as e:
                    f.write(f"❌ Error al leer datos: {str(e)}\n")
                
                f.write("\n---\n\n")
        
        print(f"✅ Auditoría de DB completada. Reporte en: {repo_path}")

if __name__ == "__main__":
    auditoria_completa()
