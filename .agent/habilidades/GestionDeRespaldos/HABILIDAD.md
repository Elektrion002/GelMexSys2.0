---
name: GestionDeRespaldos
description: Procedimiento para crear copias .bk antes de modificar archivos.
---

# HABILIDAD: Gestión de Respaldos (.bk)

Esta habilidad asegura que siempre tengamos una vía de retorno segura al modificar el código de GelMex.

## Procedimiento

1. Identificar el archivo a modificar (ej. `app/blueprints/catalogos_admin.py`).
2. Crear la copia de seguridad: `copy app\blueprints\catalogos_admin.py app\blueprints\catalogos_admin.py.bk`.
3. Proceder con la edición del archivo original.
4. En caso de error crítico, restaurar: `move app\blueprints\catalogos_admin.py.bk app\blueprints\catalogos_admin.py`.

## Cuándo Usar

- Siempre, antes de usar herramientas como `replace_file_content` o `multi_replace_file_content` en archivos del sistema.
