---
name: DespliegueVPS
description: Guía detallada (Cómo, Por qué, Para qué) para conexión segura, túnel SSH y despliegue sincronizado con Git y VPS.
---

# HABILIDAD: Despliegue y Gestión de VPS (Sincronización Total)

Esta guía explica el proceso para mantener sincronizados el entorno Local, GitHub y el Servidor de Producción (VPS), detallando el uso de credenciales en cada paso.

---

## 1. Túnel SSH (El Tunel de Datos)

### ¿Qué es y para qué sirve?

Es un "ducto" seguro que conecta tu computadora con la base de datos del servidor sin abrir puertos peligrosos al público.

### ¿Por qué lo usamos?

La base de datos del VPS solo acepta conexiones desde "localhost" por seguridad. El túnel engaña al servidor haciéndole creer que tu computadora es local.

### ¿Cómo se hace?

1. **Comando:** `ssh -L 5433:localhost:5432 root@72.62.164.237 -N`
2. **Credenciales:** Te pedirá la **Contraseña del Servidor VPS** (`root password`).
   - _Nota:_ Sin esta contraseña, no puedes "abrir el ducto".
3. **Uso:** Mientras la terminal esté abierta, puedes usar `localhost:5433` en tu código local para ver los datos del VPS.

---

## 2. Sincronización con Git (El Respaldo Central)

### ¿Qué es y para qué sirve?

Es el control de versiones. Sirve para que el código que funciona en tu computadora se guarde de forma segura en una "nube" (GitHub) antes de mandarlo a producción.

### ¿Por qué lo usamos?

Si el VPS falla o borras algo por error, siempre puedes recuperar la última versión que subiste a GitHub.

### ¿Cómo se hace?

1. **Comando:**
   ```powershell
   git add .
   git commit -m "Explicación del cambio"
   git push origin main
   ```
2. **Credenciales:** Te pedirá tu **Usuario de GitHub** y un **Personal Access Token (PAT)** o Contraseña.
   - _Importante:_ GitHub ya no usa la contraseña normal para comandos de terminal; necesitas generar un Token desde la configuración de tu cuenta.

---

## 3. Despliegue Remoto (La Actualización en Producción)

### ¿Qué es y para qué sirve?

Es darle la instrucción al servidor de que descargue lo nuevo de GitHub y se reinicie para que el cliente vea los cambios.

### ¿Por qué lo usamos?

Para que el VPS no se quede con código viejo y para que la base de datos y la interfaz siempre coincidan.

### ¿Cómo se hace?

1. **Comando Maestro:**
   ```powershell
   ssh root@72.62.164.237 "cd /var/www/GelMexSys2.0 && git pull origin main && systemctl restart gelmex"
   ```
2. **Credenciales:** Nuevamente requiere la **Contraseña del Servidor VPS**.
   - _Pro-Tip:_ Si usas "SSH Keys", no te pedirá contraseña cada vez (más seguro y rápido).

---

## Resumen de Credenciales Necesarias

| Paso                   | Credencial Requerida  | ¿De dónde sale?         |
| :--------------------- | :-------------------- | :---------------------- |
| **Túnel / Acceso VPS** | Password de `root`    | Proveedor de VPS        |
| **Push a GitHub**      | Usuario + Token (PAT) | Configuración de GitHub |
| **Conexión DB**        | Usuario + Password DB | Archivo `.env` (oculto) |

> [!IMPORTANT]
> **SEGURIDAD:** Nunca compartas estas contraseñas por texto plano. Si las olvidas, el benchmark de despliegue fallará por falta de acceso.
