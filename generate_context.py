import os
import datetime

# --- CONFIGURACIÓN DE LA HERRAMIENTA ---
OUTPUT_FILE = "PROJECT_CONTEXT.txt"
IGNORE_DIRS = {'venv', '.git', '__pycache__', 'instance', 'uploads', 'img', '.idea', '.vscode'}
IGNORE_EXTENSIONS = {'.pyc', '.sqlite3', '.db', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg'}
INCLUDE_EXTENSIONS = {'.py', '.html', '.css', '.js', '.txt', '.md', '.json', '.env.example'}

def is_ignored(path, is_dir=False):
    name = os.path.basename(path)
    if is_dir:
        return name in IGNORE_DIRS
    ext = os.path.splitext(name)[1]
    return ext in IGNORE_EXTENSIONS or name.startswith('.')

def get_tree_structure(startpath):
    """Genera una representación visual del árbol de directorios."""
    tree_str = "ESTRUCTURA DE DIRECTORIOS:\n"
    for root, dirs, files in os.walk(startpath):
        # Filtrar directorios en marcha (igual que en la lectura)
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), is_dir=True)]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree_str += '{}[{}/]\n'.format(indent, os.path.basename(root))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if not is_ignored(os.path.join(root, f)):
                 # Verificar extensiones permitidas o archivos especiales
                ext = os.path.splitext(f)[1]
                if ext in INCLUDE_EXTENSIONS or f == '.gitignore' or f == 'requirements.txt':
                    tree_str += '{}{}\n'.format(subindent, f)
    return tree_str

def generate_context():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[ INFO ] Generando reporte de contexto en: {OUTPUT_FILE}...")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        # 1. Escribir Cabecera con Datos de Auditoría
        outfile.write("="*60 + "\n")
        outfile.write(f" GELMEXSYS 2.0 - REPORTE DE CONTEXTO TÉCNICO\n")
        outfile.write(f" FECHA DE GENERACIÓN: {timestamp}\n")
        outfile.write("="*60 + "\n\n")

        # 2. Escribir el Árbol de Directorios (NUEVO)
        outfile.write("-" * 30 + "\n")
        outfile.write(get_tree_structure("."))
        outfile.write("-" * 30 + "\n\n")

        # 3. Recorrer directorios y volcar contenido
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), is_dir=True)]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                if is_ignored(file_path) or file == OUTPUT_FILE or file == "generate_context.py":
                    continue
                
                ext = os.path.splitext(file)[1]
                # Aseguramos que .gitignore y requirements.txt siempre entren
                if ext not in INCLUDE_EXTENSIONS and file != '.gitignore' and file != 'requirements.txt':
                    continue

                outfile.write(f"\n{'='*25} FILE: {file_path} {'='*25}\n")
                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(content + "\n")
                except Exception as e:
                    outfile.write(f"[ERROR LEYENDO ARCHIVO]: {str(e)}\n")

    print(f"[ OK ] Reporte generado exitosamente.")
    print(f"[ TIP ] Copia el contenido de '{OUTPUT_FILE}' y pégalo en el chat.")

if __name__ == "__main__":
    generate_context()