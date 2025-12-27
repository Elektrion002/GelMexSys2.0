# db_seeds/data_clients.py

CLIENTES = [
    {
        # Datos Negocio
        "nombre_negocio": "Abarrotes Don Pepe",
        "rfc": "XAXX010101000",
        "tipo_negocio": "Tienda de Abarrotes",
        "calificacion": 5,
        "img_fachada": "uploads/clientes/donpepe_fachada.jpg",
        
        # Datos Encargado
        "nombres_encargado": "Jose",
        "apellidos_encargado": "Perez Lopez",
        
        # Dirección Negocio (AQUÍ TAMBIÉN CORREGIMOS)
        "calle": "Calle Morelos",
        "num_exterior": "45",
        "num_interior": "",
        "colonia": "San Isidro",
        "codigo_postal": "38600",  # <--- CORREGIDO (Antes decía 'cp')
        "ciudad": "Acámbaro",
        "estado": "Guanajuato",
        "pais": "México", # Agregué país por si acaso el modelo lo requiere, no estorba
        
        # Finanzas
        "limite_credito": 5000.00,
        "saldo_actual": 0.00,
        
        # Logística
        "ruta_asignada": "Ruta 1: Acambaro",
        
        # Precios Especiales
        "precios_especiales": [
            {
                "producto_sku": "BOL-LIM-STD",
                "tipo_descuento": "PRECIO_FINAL",
                "valor": 4.50
            },
            {
                "producto_sku": "PAL-FRE-CRM",
                "tipo_descuento": "PORCENTAJE",
                "valor": 10.00
            }
        ]
    }
]