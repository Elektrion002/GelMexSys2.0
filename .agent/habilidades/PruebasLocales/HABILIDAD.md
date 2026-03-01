---
name: PruebasLocales
description: Verificación automatizada de GelMexSys antes del despliegue.
---

# HABILIDAD: PruebasLocales

Esta habilidad asegura que el sistema GelMex sea funcional en el entorno de desarrollo antes de enviar cualquier código a producción.

## Componentes Principales

- **Script de Pruebas**: `test_local.py` en el directorio raíz.
- **Ejecución**: `venv\Scripts\python.exe test_local.py`.

## Requisitos

- El túnel SSH a la base de datos del VPS debe estar activo en el puerto 5433 (según el archivo `.env`).
- Las variables de entorno locales en `.env` deben estar cargadas.

## Lista de Verificación (Checklist)

- [ ] Visibilidad del Catálogo (HTTP 200).
- [ ] Sincronización del Esquema DB (Consultas a tablas clave).
- [ ] Camino Crítico: Acceso -> Ver Producto -> Pedido.
