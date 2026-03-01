# Reglas del Proyecto GelMex (Metodología 5S)

Este documento rige el comportamiento del agente para mantener la calidad, el orden y la seguridad en el sistema GelMex.

## 1. Idioma Obligatorio (Seiketsu - Estandarización)

- **TODO** debe estar en **ESPAÑOL**.
- No se permite inglés en nombres de carpetas (`.agent/reglas`, `.agent/habilidades`, `.agent/flujos`, `.agent/pruebas`), comentarios de código nuevos, mensajes de commit o documentación.

## 2. Gestión de Respaldos (.bk) (Seiso - Limpieza/Seguridad)

- **Regla Crítica**: Antes de modificar cualquier archivo existente, se DEBE crear una copia de seguridad con la extensión `.bk`.
- Ejemplo: `cp archivo.py archivo.py.bk`.
- Esto permite una reversión instantánea ("Regresar al pasado") ante cualquier error.

## 3. Jerarquía de Propagación (Shitsuke - Disciplina)

- **Flujo**: Local -> Git -> VPS.
- **Pruebas en Local**: Prohibido subir cambios sin pasar el script de pruebas en local.
- **Folder de Pruebas**: Todos los scripts de prueba, diagnóstico o auditoría deben residir en `.agent/pruebas/`. La raíz debe mantenerse limpia (Seiri).

## 4. Entorno Virtual (venv) (Seiton - Orden Técnico)

- Todas las instalaciones de librerías, ejecuciones de scripts y comandos de Python deben realizarse dentro del entorno virtual.
- Comando: `venv\Scripts\python.exe` (Windows).

## 5. Integridad de Datos e Inspección

- Prohibido modificar la base de datos sin un **Reporte de Auditoría** previo.
- Cualquier cambio en modelos debe ser auditado y autorizado formalmente por el usuario.

## 6. Metodología 5S Aplicada

- **Seiri**: Eliminar basura de la raíz.
- **Seiton**: Cada archivo en su carpeta jerárquica dentro de `.agent/`.
- **Seiso**: Código limpio, backups `.bk` preventivos.
- **Seiketsu**: Mantener el sistema en español y seguir patrones Flask.
- **Shitsuke**: Cumplir estas reglas sin excepción.
