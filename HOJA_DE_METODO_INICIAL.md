markdown
# HOJA DE MÉTODO: DESPLIEGUE DE ENTORNO (GMX-OP-01)

| **PROYECTO**      | **ID OPERACIÓN**  | **REVISIÓN** | **RESPONSABLE**        |
|                   |                   |              |                        |
| GelMexSys 2.0 ERP | OP-001-SETUP      | 1.0 (Alpha)  | Ing. Mario E. Martínez |


## 1. OBJETIVO DE LA OPERACIÓN
Estandarizar el procedimiento de "Rearme Inicial" y configuración del entorno de desarrollo para garantizar la reproducibilidad del software en cualquier estación de trabajo (Bare Metal).


## 2. ESPECIFICACIONES DE ENTRADA (SNAPSHOT)
El sistema ha sido validado bajo los siguientes parámetros críticos. **No proceder si no se cumplen.**

| Parámetro     | Valor Especificado    | Criterio de Aceptación      |
| :-------------| :-------------------- | :-------------------------- |
| **S.O.**      | Windows 10/11 (x64)   | Sistema Host Operativo      |
| **Git Core**  | **v2.52.0.windows.1** | Hash de versión coincidente |
| **Python**    | v3.10 o superior      | Intérprete base             |
| **Framework** | Flask (Modular)       | Instalación limpia          |


## 3. SECUENCIA DE OPERACIONES

### OP 10: Instalación de Herramientas Base
**Descripción:** Preparación del entorno host.

1. Descargar instalador certificado desde [git-scm.com](https://git-scm.com/).
2. Ejecutar instalación estándar (Default Settings).
3. **Punto de Control (Inspección):** Ejecutar comando de validación.
   powershell
   git --version
   # SALIDA ESPERADA: git version 2.52.0.windows.1


### OP 20: Configuración de Identidad (Gafete Digital)

**Descripción:** Asignación de trazabilidad al usuario.

1. Ejecutar en terminal:
powershell
git config --global user.name "edwared"
git config --global user.email "elektrion@gmail.com"


### OP 30: Inicialización del Repositorio

**Descripción:** Activación del control de cambios en el directorio de trabajo.

1. Iniciar rastreo:
powershell
git init


2. **Seguridad:** Crear archivo de bloqueo `.gitignore` con los siguientes filtros:
text
venv/
__pycache__/
*.pyc
instance/
.env
*.db
app/static/uploads/



3. **Línea Base:** Generar el primer punto de restauración.
powershell
git add .
git commit -m "Inicio: Estructura base y entorno virtual según HOJA DE METODO OP-001"


### OP 40: Aprovisionamiento del Entorno Virtual

**Descripción:** Creación del contenedor aislado de librerías (VENV).

1. Generar entorno:
powershell
python -m venv venv



2. **Activación (Punto Crítico):**
powershell
.\venv\Scripts\activate



*Verificación Visual: Debe aparecer `(venv)` en verde al inicio de la terminal.*
3. Inyección de Dependencias:
powershell
pip install -r requirements.txt



## 4. DIAGRAMA DE ARQUITECTURA RESULTANTE

Al finalizar la operación, la estructura del directorio debe coincidir con este patrón:

text
GelMexSys2.0/
├── HOJA_DE_METODO_INICIAL.md  <-- Documento Maestro
├── app/
│   ├── blueprints/            # Lógica (Controladores)
│   ├── models/                # Datos (ORM)
│   ├── static/                # Assets
│   ├── templates/             # Vistas
│   └── __init__.py            # App Factory
├── instance/                  # BD Local
├── run.py                     # Entry Point
└── requirements.txt           # BOM (Bill of Materials) de Librerías

