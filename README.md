 HOJA DE MÉTODO: DESPLIEGUE DE ENTORNO (GMX-OP-01)

| **PROYECTO**      | **ID OPERACIÓN**  | **REVISIÓN** | **RESPONSABLE**        |
| :---              | :---              | :---         | :---                   |
| GelMexSys 2.0 ERP | OP-001-SETUP      | 1.1 (Fix)    | Ing. Mario E. Martínez |

 1. OBJETIVO DE LA OPERACIÓN
Estandarizar el procedimiento de "Rearme Inicial" y configuración del entorno de desarrollo, asegurando la vinculación explícita a la versión correcta de Python (3.12) y la gestión de dependencias sin conflictos.

 2. ESPECIFICACIONES DE ENTRADA (SNAPSHOT)
El sistema ha sido validado bajo los siguientes parámetros críticos. **No proceder si no se cumplen.**

| Parámetro     | Valor Especificado    | Criterio de Aceptación      |
| :-------------| :-------------------- | :-------------------------- |
| **S.O.**      | Windows 10/11 (x64)   | Sistema Host Operativo      |
| **Git Core**  | **v2.52.0.windows.1** | Hash de versión coincidente |
| **Python**    | **C:\Python312**      | Ruta Absoluta del Binario   |
| **Framework** | Flask (Modular)       | Instalación limpia          |


 3. SECUENCIA DE OPERACIONES
 OP 10: Instalación de Herramientas Base
**Descripción:** Preparación del entorno host.
1. Descargar instalador certificado desde [git-scm.com](https://git-scm.com/).
2. Ejecutar instalación estándar (Default Settings).
3. **Punto de Control (Inspección):** Ejecutar comando de validación.
   powershell
   git --version
    SALIDA ESPERADA: git version 2.52.0.windows.1

 OP 20: Configuración de Identidad (Gafete Digital)
**Descripción:** Asignación de trazabilidad al usuario.
1. Ejecutar en terminal:
powershell
git config --global user.name "edwared"
git config --global user.email "elektrion@gmail.com"

 OP 30: Inicialización del Repositorio

**Descripción:** Activación del control de cambios en el directorio de trabajo.

1. Iniciar rastreo:
powershell
git init


2. **Seguridad:** Crear archivo de bloqueo `.gitignore` con los siguientes filtros:
```text
venv/
__pycache__/
*.pyc
instance/
.env
*.db
app/static/uploads/

3. **Línea Base:** Generar el primer punto de restauración.
```powershell
git add .
git commit -m "Inicio: Estructura base y entorno virtual según HOJA DE METODO OP-001"

OP 40: Aprovisionamiento y Vinculación de Entorno

**Descripción:** Creación del contenedor aislado (VENV) forzando la ruta del ejecutable para evitar ambigüedad en Windows y carga de materiales.

1. **Creación con Ruta Absoluta:**
Usar el operador de llamada `&` de PowerShell para invocar el ejecutable específico y evitar errores de sintaxis.
powershell
& "C:\Python312\python.exe" -m venv venv

2. **Activación (Punto Crítico):**
powershell
.\venv\Scripts\activate

*Verificación Visual: Debe aparecer `(venv)` en verde al inicio de la terminal.*
3. **Validación de Origen (Quality Gate):**
Asegurar que el sistema no está usando el Python de C:.
powershell
Get-Command python
 CRITERIO DE ACEPTACIÓN: Source debe ser ".../GelMexSys2.0/venv/Scripts/python.exe"

4. **Definición de Lista de Materiales (BOM):**
Editar archivo `requirements.txt` con el siguiente contenido exacto para evitar conflictos de versiones:

Flask==3.0.0
python-dotenv==1.0.0
SQLAlchemy>=2.0.16
Flask-SQLAlchemy>=3.1.1


5. **Inyección de Dependencias:**
powershell
pip install -r requirements.txt




 4. DIAGRAMA DE ARQUITECTURA RESULTANTE

Al finalizar la operación y ejecutar el script de estructura, el directorio debe coincidir con este patrón:

GelMexSys2.0/
├── HOJA_DE_METODO_INICIAL.md  <-- Documento Maestro Actualizado
├── app/
│   ├── blueprints/             Lógica (Controladores)
│   ├── models/                 Datos (ORM)
│   ├── static/                 Assets
│   ├── templates/              Vistas
│   └── __init__.py             App Factory
├── instance/                   BD Local
├── run.py                      Entry Point
└── requirements.txt            BOM Certificado


 GUÍA TÉCNICA: DESPLIEGUE DE MOTOR DE BASE DE DATOS (GMX-DB-01)

 PASO 1: Descarga e Instalación

1. Ve al sitio oficial: [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Dale clic en **"Download the installer"**.
3. Elige la versión **16.x** (es la más estable ahorita) para Windows x86-64.
4. Ejecuta el instalador.

**Durante la instalación (OJO AQUÍ):**

* **Componentes:** Asegúrate de que estén marcados:
* [x] PostgreSQL Server
* [x] pgAdmin 4 (Este es el panel visual para administrar, indispensable).
* [x] Command Line Tools


* **Directorio:** Déjalo por defecto.
* **Contraseña (CRÍTICO):** Te va a pedir una contraseña para el "Superusuario (postgres)".
* ⚠️ **Escríbela:** Ponle `admin` o `123456` por ahora para desarrollo local. **No la olvides**, porque sin ella no podemos conectar Python.


* **Puerto:** Déjalo en `5432` (Estándar).
* **Locale:** Déjalo por defecto (Default locale).

Dale "Siguiente" a todo hasta que termine.

---

 PASO 2: Crear la Base de Datos "gelmex_db"

Ya instalado, no vamos a usar consola negra, vamos a usar lo visual.

1. Presiona la tecla `Windows` y busca **pgAdmin 4**. Ábrelo (es el icono del elefante).
2. Te va a pedir la contraseña que acabas de crear. Pónsela.
3. A la izquierda verás `Servers` -> `PostgreSQL 16`. Dale doble clic para conectar.
4. Dale **clic derecho** sobre "Databases" -> **Create** -> **Database...**
5. En el nombre ponle: **`gelmex_db`** (Todo minúsculas).
6. Dale **Save**.

¡Listo! Ya tienes el contenedor vacío esperando los datos.

---

 PASO 3: Conectar Flask a PostgreSQL

Ahora hay que decirle a tu código: "Oye, deja de usar SQLite y conéctate al Postgres que acabamos de instalar".

1. Abre tu archivo **`config.py`** en VS Code.
2. Busca la clase `DevelopmentConfig`.
3. Modifica la línea `SQLALCHEMY_DATABASE_URI`.

Debe quedar así (cambia `TU_CONTRASEÑA` por la que pusiste en el instalador):

```python
class DevelopmentConfig(Config):
    DEBUG = True
     Conexión a PostgreSQL Local
     Formato: postgresql://usuario:password@localhost:puerto/nombre_db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'postgresql://postgres:TU_CONTRASEÑA@localhost:5432/gelmex_db'

```

*Nota: Si tu contraseña es `admin`, la línea queda: `'postgresql://postgres:admin@localhost:5432/gelmex_db'*`

---

 PASO 4: Instalar el Driver

Para que Python hable con Postgres, necesita un traductor. Ejecuta esto en tu terminal (con el `(venv)` activo):

```powershell
pip install psycopg2-binary

```

---

 PASO 5: Generar las Tablas (La Prueba de Fuego)

Ahora sí, ya con el motor instalado, la base creada y el código conectado, vamos a crear las tablas.

Ejecuta tu archivo de arranque:

```powershell
python run.py

```

1. Si dice `Running on http://127.0.0.1:5000`, **EXITAZO**.
2. Para confirmar, ve a **pgAdmin 4**, ve a `gelmex_db` -> `Schemas` -> `public` -> `Tables`. Dale clic derecho y "Refresh".
3. Deberías ver ahí toda la lista: `almacenes`, `clientes`, `productos`, `usuarios`... ¡Todas las tablas vacías creadas por SQLAlchemy!

OP 50: Aseguramiento de Versión (Git Commit)

**Descripción:** Consolidación de la Arquitectura de Datos, Modelos ORM y conexión a motor de base de datos.

**1. Verificar el Estado (Reconocimiento)**
Primero, vamos a ver todo lo que Git detectó que cambiamos (Modelos, Config, Seeds, etc.). Ejecuta en tu terminal:

```powershell
git status

```

*Deberías ver en rojo (o verde si ya agregaste algo) archivos como `app/models/`, `db_seeds/`, `config.py`, `setup_db.py`, etc.*

**2. Preparar el Paquete (Staging)**
Vamos a subir todo al área de preparación.

```powershell
git add .

```

**3. Ejecutar el Commit (Guardado)**

```powershell
git commit -m "Feat: Implementacion Arquitectura de Datos PostgreSQL y Modelos ORM

- Configuracion de conexion a PostgreSQL en config.py (GMX-DB-01).
- Creacion de Modelos Maestros: Catalogos, Usuarios, Productos, Clientes, Infraestructura.
- Integracion de script de sembrado de datos (seed_runner.py) y diccionarios de datos.
- Instalacion de driver psycopg2-binary.
- Validacion de creacion de tablas en pgAdmin 4."

```
OP 60: Integración de Motor de Datos (Post-Deployment)

**Descripción:** Vinculación del entorno de aplicación con el servidor de datos persistente.

1. **Instalación de Driver:**
```powershell
pip install psycopg2-binary


2. **Configuración de Enlace:**
Editar `config.py` para apuntar a `postgresql://postgres:***@localhost:5432/gelmex_db`.
3. **Despliegue de Esquema:**
Ejecutar script de diagnóstico y construcción:
```powershell
python setup_db.py

```


*Criterio de Aceptación: Mensaje "✅ ¡ÉXITO! TABLAS CREADAS CORRECTAMENTE." y visualización de 34 tablas en pgAdmin.*

---

