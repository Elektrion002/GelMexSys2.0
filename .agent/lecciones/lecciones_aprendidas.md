# Lecciones Aprendidas: GelMexSys 2.0

## 1. Metodología 5S en Código

- **Error**: Mezclar JavaScript (`onerror`, `onclick`) directamente en los atributos HTML.
- **Consecuencia**: Errores de sintaxis detectados por el linter y código difícil de mantener.
- **Lección**: **Nunca** usar JS inline. Toda lógica debe residir en archivos `.js` externos. Los eventos se manejan mediante funciones globales o escuchadores de eventos.

## 2. Atestación de Base de Datos

- **Error**: Suponer que la base de datos física coincide con el modelo de Python.
- **Consecuencia**: Error 500 (`ProgrammingError`) por falta de columnas como `access_code`.
- **Lección**: Siempre realizar una auditoría de esquema (`ALTER TABLE`) antes de implementar nuevas funcionalidades que dependan del modelo.

## 3. Aislamiento de Entornos

- **Error**: Heredar de un template administrativo (`base.html`) para un portal público.
- **Consecuencia**: Fuga de datos/funcionalidad y errores cuando el usuario no está autenticado como administrador.
- **Lección**: Crear templates base dedicados (`base_portal.html`) para vistas de cliente para asegurar el aislamiento total (Aesthetic & Security).

## 4. Gestión de Multimedia

- **Error**: Depender de que el usuario cargue imágenes perfectas o que las rutas sean infalibles.
- **Consecuencia**: Iconos de imagen rota que dañan la imagen premium de la marca.
- **Lección**: Implementar siempre un sistema de **Fallback** (imagen por defecto) centralizado en JS.

---

_Este documento es parte del estándar GelMex de mejora continua._
