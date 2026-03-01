---
description: Procedimiento para una ejecución segura de cambios (Caminata de Ejecución)
---

# FLUJO: CaminataDeEjecucionSegura

Este es el proceso estándar que seguiré cuando me pidas realizar cambios importantes. Puedes activarlo diciendo: "/ejecuta-cambio" o "Sigue el flujo de ejecución segura".

## Pasos del Proceso:

1. **Auditoría Previa**: Si el cambio involucra la base de datos, ejecuto `AuditoriaArquitectura`.
2. **Backups (.bk)**: Creo copias de seguridad de todos los archivos que voy a tocar.
3. **Draft de Implementación**: Presento el plan de qué se va a modificar.
4. **Modificación venv**: Realizo los cambios usando exclusivamente el entorno virtual.
5. **Prueba Local**: Ejecuto `.agent/pruebas/test_local.py` para verificar que nada se rompió.
6. **Limpieza 5S**: Elimino cualquier archivo temporal generado durante el proceso.
7. **Notificación**: Entrego un walkthrough del resultado.

// turbo-all
