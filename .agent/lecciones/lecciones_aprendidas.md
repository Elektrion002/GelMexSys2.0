# Lecciones Aprendidas - Proyecto GelMex

Este documento registra los errores cometidos ("malos pasos") y la solución definitiva para que no vuelvan a ocurrir.

## 1. El Error de la "Suposición de Arquitectura"

- **Mal paso**: Intentar implementar el Portal de Clientes basándose solo en los modelos del código Python (`models/clients.py`), asumiendo que la base de datos física estaba sincronizada.
- **Consecuencia**: Error 500 en la aplicación al buscar la columna `access_code` que no existía en PostgreSQL.
- **Lección**: NUNCA suponer la estructura de la base de datos. Antes de cualquier cambio en modelos o lógica de datos, se debe ejecutar la **Habilidad: AuditoriaArquitectura**.

## 2. El Error del "Desorden en la Raíz" (5S - Seiri)

- **Mal paso**: Dejar scripts de prueba (`test_local.py`, `api_test.py`) en la raíz del proyecto.
- **Consecuencia**: Confusión visual, riesgo de ejecución accidental y violación de la metodología 5S.
- **Lección**: La raíz debe contener solo lo estrictamente necesario para el arranque (`run.py`, `.env`). Todo lo demás debe ir a sus respectivas carpetas en `.agent/`.

## 3. El Error del Idioma (Cero Inglés)

- **Mal paso**: Usar términos en inglés en rutas de archivos, comentarios o documentación.
- **Consecuencia**: Conflictos de comunicación con el usuario y ruptura de la estandarización del proyecto.
- **Lección**: El sistema es 100% en español. Si se detecta inglés, se debe traducir de inmediato.

## 4. El Error de la "Modificación Directa" (Sin .bk)

- **Mal paso**: Editar archivos críticos del sistema sin tener una vía de escape rápida.
- **Consecuencia**: Riesgo de dejar el sistema inoperativo por un error de sintaxis o lógica.
- **Lección**: Aplicar siempre la **Regla de Respaldos .bk** antes de usar cualquier herramienta de edición.

---

**Objetivo Final**: Error Mínimo mediante Disciplina (Shitsuke).
