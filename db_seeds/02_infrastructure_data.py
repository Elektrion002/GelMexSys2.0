# db_seeds/02_infrastructure_data.py

ALMACENES = [
    {
        "descripcion": "Cámara Fría Principal (Producto Terminado)",
        "tipo": "Cámara Fría (Congelación)",
        "planta": "Planta Matriz Hgo",
        "area": "Logística y Carga",
        "ubicaciones": [
            # Generaremos códigos automáticos o manuales
            {"codigo": "CF1-PAS1-NV1", "notas": "Pasillo 1 Nivel 1"},
            {"codigo": "CF1-PAS1-NV2", "notas": "Pasillo 1 Nivel 2"},
            {"codigo": "CF1-PISO", "notas": "Almacenaje a piso"}
        ]
    },
    {
        "descripcion": "Almacén Materia Prima Seca",
        "tipo": "Almacén Seco",
        "planta": "Planta Matriz Hgo",
        "area": "Producción Helados",
        "ubicaciones": [
            {"codigo": "SEC-ANAQUEL-A", "notas": "Sacos Azúcar"},
            {"codigo": "SEC-ANAQUEL-B", "notas": "Saborizantes"}
        ]
    }
]

RUTAS = [
    {"descripcion": "Ruta 1: Acambaro", "notas": "Lunes, Miércoles, Viernes"},
    {"descripcion": "Ruta 2: Queretaro", "notas": "Martes y Jueves"},
    {"descripcion": "Ruta 3: Zinapecuaro", "notas": "Sábados"}
]
