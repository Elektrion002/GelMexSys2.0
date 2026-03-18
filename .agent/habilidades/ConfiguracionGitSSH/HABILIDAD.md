---
name: ConfiguracionGitSSH
description: Guía detallada paso a paso para configurar autenticación SSH con GitHub en un nuevo VPS para evitar el uso de contraseñas.
---

# HABILIDAD: Configuración de Autenticación Git por SSH en VPS

Esta habilidad documenta el procedimiento estándar y seguro para conectar un servidor de producción (VPS) con GitHub sin necesidad de ingresar contraseñas o Tokens de Acceso Personal (PAT) repetitivamente al hacer `git pull` o `git fetch`.

## El Problema

Desde 2021, GitHub eliminó el soporte para autenticarse usando la contraseña normal de la cuenta en la terminal gráfica o de comandos. Los intentos arrojarán el error:
`Support for password authentication was removed. Please use a personal access token instead.`

## Solución: Llaves SSH (Asymetric Cryptography)

En lugar de contraseñas, generamos un par de llaves (Pública y Privada). El VPS se queda con la llave privada y a GitHub le entregamos la llave pública. Cuando el VPS intenta descargar código, GitHub verifica que las llaves "encajen".

---

## Procedimiento Paso a Paso (Para un VPS nuevo)

### Paso 1: Generar el par de llaves en el VPS

Conéctate por SSH a tu VPS como el usuario que ejecutará la aplicación (usualmente `root` o un usuario de despliegue).

1. Ejecuta el siguiente comando para generar la llave RSA:

   ```bash
   ssh-keygen -t rsa -b 4096 -C "tu_correo@ejemplo.com"
   ```

   _(Reemplaza el correo por el asociado a tu cuenta de GitHub)._

2. La terminal te preguntará dónde guardar la llave:

   > `Enter file in which to save the key (/root/.ssh/id_rsa):`

   **Presiona ENTER** para aceptar la ruta por defecto.

3. Te pedirá un "passphrase" (contraseña adicional para la llave).
   Para automatización de servidores, lo ideal es dejarlo **EN BLANCO** presionando **ENTER** dos veces.

### Paso 2: Obtener la Llave Pública

Ahora necesitas leer el contenido del candado (la llave pública) para llevársela a GitHub.

1. Ejecuta:
   ```bash
   cat ~/.ssh/id_rsa.pub
   ```
2. La terminal imprimirá un texto largo que empieza con `ssh-rsa ...` y termina con tu correo.
3. Copia TODO ese texto exactamente como está (sin espacios extra al principio o final).

### Paso 3: Registrar la Llave en GitHub

1. Entra a GitHub.com desde tu navegador local e inicia sesión.
2. Ve a los **Settings** de tu perfil (clic en tu foto arriba a la derecha > Settings).
3. En el menú lateral izquierdo, haz clic en **SSH and GPG keys**.
4. Haz clic en el botón verde **New SSH key**.
5. Llena el formulario:
   - **Title:** Pon un nombre que te ayude a identificarlo (Ej. "VPS Producción GelMex").
   - **Key type:** Authentication Key.
   - **Key:** PEGA AQUÍ el texto largo que copiaste del Paso 2.
6. Haz clic en **Add SSH key**.

### Paso 4: Probar la Conexión desde el VPS

Para verificar que el VPS ya tiene acceso a GitHub sin contraseña, ejecuta esto en el VPS:

```bash
ssh -T git@github.com
```

La primera vez te saldrá un mensaje diciendo que no reconoce el host "github.com". Escribe `yes` y presiona ENTER.
Deberías recibir un mensaje de éxito como:

> `Hi [tu_usuario]! You've successfully authenticated, but GitHub does not provide shell access.`

---

## ⚠️ Paso CRÍTICO: Cambiar la URL de Git en tu Proyecto

Para que Git empiece a usar el túnel SSH y no te pida contraseña, debes decirle a la carpeta de tu proyecto en el VPS que use la dirección SSH y no la de HTTPS.

1. Ve a la carpeta de tu proyecto en el VPS:
   ```bash
   cd /var/www/TuProyecto
   ```
2. Cambia la URL remota origin ejecutando:

   ```bash
   git remote set-url origin git@github.com:TuUsuario/TuRepositorio.git
   ```

   _(Asegúrate de cambiar `TuUsuario/TuRepositorio` por los datos reales de tu repo. Nota que usa `:` en lugar de `/` después de `github.com`)._

3. ¡Listo! Intenta hacer un `git pull origin main`. Ya no te pedirá ninguna contraseña.

---

## 5. El Flujo de Trabajo Unidireccional (La Regla de Oro)

Para mantener la estabilidad en GelMexSys (y evitar conflictos al hacer despliegues), el flujo de Git es **ESTRICTAMENTE**:

**Local -> GitHub -> VPS**

### ¿Por qué NUNCA sincronizar del VPS hacia Local?

Está estrictamente prohibido editar código directamente en el servidor de producción (VPS) para "arreglos rápidos".

1. El VPS tendría código que GitHub no tiene.
2. Tu computadora local no sabría qué pasó.
3. El próximo despliegue desde Local sobreescribiría y borraría por completo tu arreglo en el servidor.

### Comandos de Ejecución Correcta

- **En tu computadora (Local):** Escribe el código, pruébalo, haz `git commit` y envíalo con `git push origin main`.
- **En el VPS (Producción):** Solo actualiza leyendo de GitHub. El comando recomendado **no** es un simple `pull`, sino un reemplazo forzado (`reset --hard`) para garantizar que Producción sea un reflejo idéntico de lo que hay en GitHub, ignorando cualquier cambio accidental en el servidor:
  ```bash
  git reset --hard origin/main
  ```
