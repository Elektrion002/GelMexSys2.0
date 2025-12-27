# db_seeds/04_users_data.py

USUARIOS = [
    {
        # Login
        "email": "admin@gelmex.com",
        "password_raw": "Admin2025",
        "pin": "123456",
        # Identidad
        "nombres": "Mario Eduardo",
        "apellido_paterno": "Martinez",
        "apellido_materno": "Juarez",
        "puesto": "Super Administrador",
        "nivel": 5,
        "rfc": "MAJU900101XXX", # Dato real o ficticio válido
        "curp": "MAJU900101HGT...",
        # Laboral
        "fecha_inicio": "2024-01-01",
        "calificacion": 5,
        # Contacto
        "telefono_celular": "78610300599",
        "telefono_casa": "4171234567",
        # Dirección
        "calle": "Av. Hidalgo",
        "num_exterior": "123",
        "num_interior": "A",
        "colonia": "Centro",
        "cp": "38600",
        "ciudad": "Acámbaro",
        "estado": "Guanajuato",
        "pais": "México",
        # Emergencia
        "contacto_emergencia": "Maria Reyna Figueroa",
        "telefono_emergencia": "4179999999",
        # Archivos (Placeholders)
        "foto_perfil": "uploads/usuarios/admin_profile.jpg"
    }
]