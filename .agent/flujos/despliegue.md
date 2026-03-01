---
description: Flujo de Despliegue verificado (Local -> Git -> VPS)
---

# FLUJO: Despliegue GelMex

Sigue estos pasos para asegurar un despliegue seguro en GelMexSys.

1. **Verificación Local (Seiso - Inspección)**
   // turbo
   `venv\Scripts\python.exe test_local.py`

2. **Commit y Push (Shitsuke - Disciplina)**
   `git add .`
   `git commit -m "Descripción clara en español"`
   `git push origin main`

3. **Actualización VPS (Seiketsu - Estandarización)**
   `ssh -t root@72.62.164.237 "cd /var/www/GelMexSys2.0 && git reset --hard origin/main && systemctl restart gelmex"`

4. **Monitoreo Final**
   Verifica los logs en el VPS: `journalctl -u gelmex -f`
