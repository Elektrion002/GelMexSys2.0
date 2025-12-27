# db_seeds/03_products_data.py

PRODUCTOS = [
    {
        "sku": "BOL-LIM-STD",
        "descripcion": "Boli de Limón (Tamaño Estándar)",
        "categoria": "Bolis Base Agua",
        "unidad": "Pieza",
        # Precios
        "precio_costo": 2.50,
        "precio_venta": 6.00,
        # Inventario
        "stock_min": 100,
        "stock_max": 2000,
        "stock_ideal": 1000,
        # Físico
        "peso_gr": 150,
        "caducidad_dias": 30,
        "imagen": "uploads/productos/bol_limon.jpg" 
    },
    {
        "sku": "PAL-FRE-CRM",
        "descripcion": "Paleta de Fresa con Crema",
        "categoria": "Paletas Base Crema",
        "unidad": "Pieza",
        "precio_costo": 4.00,
        "precio_venta": 12.00,
        "stock_min": 50,
        "stock_max": 1000,
        "stock_ideal": 500,
        "peso_gr": 120,
        "caducidad_dias": 45,
        "imagen": "uploads/productos/pal_fresa.jpg"
    }
]

MATERIAS_PRIMAS = [
    {
        "sku": "AZU-BUL-50",
        "descripcion": "Bulto de Azúcar Estándar 50kg",
        "categoria": "Azúcares y Endulzantes", # <--- CORREGIDO: Debe coincidir con archivo 01
        "unidad": "Kilogramo", 
        "precio_costo": 22.50,
        "precio_venta": 28.00, 
        "stock_min": 100,
        "stock_max": 1000,
        "stock_ideal": 500,
        "peso_gr": 1000,
        "caducidad_dias": 365,
        "imagen": "uploads/materias/azucar.jpg"
    }
]