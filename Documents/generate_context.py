import os
import datetime

# --- CONFIGURACIÓN DE LA HERRAMIENTA ---
OUTPUT_FILE = "PROJECT_CONTEXT.txt"

# Carpetas a ignorar (Agregué 'migrations' y 'pytest_cache')
IGNORE_DIRS = {
    'venv', '.git', '__pycache__', 'instance', 'uploads', 'img', 
    '.idea', '.vscode', 'migrations', '.pytest_cache', 'node_modules'
}

# Extensiones a ignorar (Archivos binarios o imágenes)
IGNORE_EXTENSIONS = {
    '.pyc', '.sqlite3', '.db', '.png', '.jpg', '.jpeg', 
    '.gif', '.ico', '.svg', '.eot', '.ttf', '.woff', '.woff2'
}

# Archivos específicos a ignorar (Para no saturar)
IGNORE_FILES = {OUTPUT_FILE, "generate_context.py", "package-lock.json"}

# Extensiones permitidas (Texto y Código)
INCLUDE_EXTENSIONS = {'.py', '.html', '.css', '.js', '.txt', '.md', '.json', '.env.example', '.sql'}

# Límite de tamaño por archivo (500KB) para evitar bloqueos
MAX_FILE_SIZE_KB = 500 

def is_ignored(path, is_dir=False):
    name = os.path.basename(path)
    if is_dir:
        return name in IGNORE_DIRS
    
    ext = os.path.splitext(name)[1]
    return (ext in IGNORE_EXTENSIONS) or (name.startswith('.')) or (name in IGNORE_FILES)

def get_tree_structure(startpath):
    """Genera una representación visual del árbol de directorios."""
    tree_str = "ESTRUCTURA DE DIRECTORIOS:\n"
    for root, dirs, files in os.walk(startpath):
        # Filtrar directorios en marcha
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), is_dir=True)]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree_str += '{}[{}/]\n'.format(indent, os.path.basename(root))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if not is_ignored(os.path.join(root, f)):
                tree_str += '{}{}\n'.format(subindent, f)
    return tree_str

def generate_context():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[ INFO ] Generando reporte de contexto en: {OUTPUT_FILE}...")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        # 1. Cabecera MCP
        outfile.write("="*60 + "\n")
        outfile.write(f" GELMEXSYS 2.0 - REPORTE DE CONTEXTO TÉCNICO (PostgreSQL)\n")
        outfile.write(f" FECHA: {timestamp}\n")
        outfile.write("="*60 + "\n\n")

        # 2. Árbol Visual
        outfile.write("-" * 30 + "\n")
        outfile.write(get_tree_structure("."))
        outfile.write("-" * 30 + "\n\n")

        # 3. Contenido de Archivos
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), is_dir=True)]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                if is_ignored(file_path):
                    continue
                
                ext = os.path.splitext(file)[1]
                # Inclusión estricta: Solo lo que definimos o archivos clave
                if ext not in INCLUDE_EXTENSIONS and file not in ['requirements.txt', '.gitignore', 'Procfile']:
                    continue

                # REGLA DE PESO: Si el archivo es muy grande, lo saltamos
                try:
                    size_kb = os.path.getsize(file_path) / 1024
                    if size_kb > MAX_FILE_SIZE_KB:
                        outfile.write(f"\n{'='*25} FILE: {file_path} (SKIPPED - TOO LARGE) {'='*25}\n")
                        outfile.write(f"[INFO] El archivo pesa {size_kb:.2f}KB y excede el límite de {MAX_FILE_SIZE_KB}KB.\n")
                        continue
                except:
                    pass

                outfile.write(f"\n{'='*25} FILE: {file_path} {'='*25}\n")
                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(content + "\n")
                except Exception as e:
                    outfile.write(f"[ERROR LEYENDO ARCHIVO]: {str(e)}\n")

    print(f"[ OK ] Reporte generado exitosamente.")

if __name__ == "__main__":
    generate_context()