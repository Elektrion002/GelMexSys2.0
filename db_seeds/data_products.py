# db_seeds/data_products.py

PRODUCTOS = [
    {
        "sku": "BOL-LIM-STD",
        "descripcion": "Boli de Limón (Tamaño Estándar)",
        "categoria": "Bolis Base Agua",
        "unidad": "Pieza",
        # CORRECCIÓN DE NOMBRES PARA COINCIDIR CON BD
        "precio_costo_actual": 2.50,      # Antes: precio_costo
        "precio_venta_general": 6.00,     # Antes: precio_venta
        "stock_minimo": 100,              # Antes: stock_min
        "stock_maximo": 2000,             # Antes: stock_max
        "stock_ideal": 1000,
        "peso_gramos": 150,               # Antes: peso_gr
        "caducidad_dias": 30,
        "imagen": "uploads/productos/bol_limon.jpg" # El runner maneja 'imagen' manualmente, este déjalo así
    },
    {
        "sku": "PAL-FRE-CRM",
        "descripcion": "Paleta de Fresa con Crema",
        "categoria": "Paletas Base Crema",
        "unidad": "Pieza",
        "precio_costo_actual": 4.00,
        "precio_venta_general": 12.00,
        "stock_minimo": 50,
        "stock_maximo": 1000,
        "stock_ideal": 500,
        "peso_gramos": 120,
        "caducidad_dias": 45,
        "imagen": "uploads/productos/pal_fresa.jpg"
    }
]

MATERIAS_PRIMAS = [
    {
        "sku": "AZU-BUL-50",
        "descripcion": "Bulto de Azúcar Estándar 50kg",
        "categoria": "Azúcares y Endulzantes",
        "unidad": "Kilogramo", 
        # CORRECCIÓN: Materia Prima usa 'precio_costo_promedio'
        "precio_costo_promedio": 22.50,   # Antes: precio_costo
        "precio_venta_general": 28.00,
        "stock_minimo": 100,
        "stock_maximo": 1000,
        "stock_ideal": 500,
        "peso_gramos": 1000,
        "caducidad_dias": 365,
        "imagen": "uploads/materias/azucar.jpg"
    }
]