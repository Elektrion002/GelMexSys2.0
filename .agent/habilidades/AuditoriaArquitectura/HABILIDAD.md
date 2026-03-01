---
name: AuditoriaArquitectura
description: Escaneo profundo de base de datos y mapeo de CRUD en el código.
---

# HABILIDAD: AuditoriaArquitectura

Esta habilidad permite obtener la "verdad absoluta" del sistema mediante la inspección directa de la base de datos y el análisis estático del código.

## Objetivos

1. **Inspección de DB**: Obtener nombres de tablas, columnas, tipos de datos y restricciones (FK, PK).
2. **Muestreo**: Extraer las primeras 3 filas de cada tabla para entender el contexto de la información.
3. **Mapeo CRUD**: Localizar en el código fuente todas las interacciones con la base de datos (Insert, Select, Update, Delete).
4. **Documentación**: Consolidar los hallazgos en un formato estructurado (CSV o Markdown).

## Procedimiento

1. Ejecutar el script centralizado en `.agent/pruebas/auditoria_db_crud.py`.
2. Las salidas deben guardarse en `.agent/pruebas/resultados/`.
3. Mantener el orden 5S: limpiar archivos temporales tras la generación del reporte final.

## Reglas Críticas

- **Prohibido Suponer**: Si no está en el reporte de la base de datos, no existe.
- **Respetar venv**: Ejecutar siempre con `venv\Scripts\python.exe`.
- **Integridad**: No modificar datos durante el muestreo (Solo lectura).
