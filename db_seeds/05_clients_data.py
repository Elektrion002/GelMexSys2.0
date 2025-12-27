# db_seeds/05_clients_data.py

CLIENTES = [
    {
        # Datos Negocio
        "nombre_negocio": "Abarrotes Don Pepe",
        "rfc": "XAXX010101000", # RFC Genérico o Real
        "tipo_negocio": "Tienda de Abarrotes",
        "calificacion": 5,
        "img_fachada": "uploads/clientes/donpepe_fachada.jpg",
        
        # Datos Encargado
        "nombres_encargado": "Jose",
        "apellidos_encargado": "Perez Lopez",
        
        # Dirección Negocio
        "calle": "Calle Morelos",
        "num_exterior": "45",
        "num_interior": "",
        "colonia": "San Isidro",
        "cp": "38600",
        "ciudad": "Acámbaro",
        "estado": "Guanajuato",
        
        # Finanzas
        "limite_credito": 5000.00,
        "saldo_actual": 0.00, # Inicia en cero
        
        # Logística
        "ruta_asignada": "Ruta 1: Acambaro", # Debe coincidir con archivo de infraestructura
        
        # Precios Especiales (Lista de diccionarios)
        "precios_especiales": [
            {
                "producto_sku": "BOL-LIM-STD",
                "tipo_descuento": "PRECIO_FINAL", # Usa el string del catálogo
                "valor": 4.50 # Precio normal 6.00, a él se lo damos a 4.50
            },
            {
                "producto_sku": "PAL-FRE-CRM",
                "tipo_descuento": "PORCENTAJE",
                "valor": 10.00 # 10% de descuento
            }
        ]
    }
]