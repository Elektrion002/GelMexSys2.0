# db_seeds/data_users.py

USUARIOS = [
    {
        # --- LOGIN ---
        "email": "admin@gelmex.com",
        "password_raw": "Admin2025",
        
        # --- SEGURIDAD ---
        "pin_seguridad": "123456",
        "nivel_usuario": 5,
        "activo": True,

        # --- IDENTIDAD ---
        "nombres": "Mario Eduardo",
        "apellido_paterno": "Martinez",
        "apellido_materno": "Juarez",
        "puesto": "Super Administrador",
        "rfc": "MAJU900101XXX",
        "curp": "MAJU900101HGT...",
        
        # --- LABORAL ---
        "fecha_inicio_empresa": "2024-01-01",
        "calificacion_evaluacion": 5,
        
        # --- CONTACTO ---
        "telefono_celular": "78610300599",
        "telefono_casa": "4171234567",
        
        # --- DIRECCIÓN (AQUÍ ESTABA EL ERROR) ---
        "calle": "Av. Hidalgo",
        "num_exterior": "123",
        "num_interior": "A",
        "colonia": "Centro",
        "codigo_postal": "38600",   # <--- CORREGIDO (Antes decía 'cp')
        "ciudad": "Acámbaro",
        "estado": "Guanajuato",
        "pais": "México",
        
        # --- EMERGENCIA ---
        "contacto_emergencia_nombre": "Maria Reyna Figueroa",
        "contacto_emergencia_telefono": "4179999999",
        
        # --- ARCHIVOS ---
        "foto_perfil": "uploads/usuarios/admin_profile.jpg"
    }
]