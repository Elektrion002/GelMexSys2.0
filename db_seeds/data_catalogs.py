# db_seeds/01_catalogs_data.py

CATALOGOS = {
    # --- INFRAESTRUCTURA ---
    "cat_plantas": [
        {"descripcion": "Planta Matriz Hgo", "notas": "Producción Principal"},        
    ],
    "cat_areas": [
        {"descripcion": "Producción", "notas": "Zona Congelacion"},        
        {"descripcion": "Logística y Carga", "notas": "Andenes"},
        {"descripcion": "Administración", "notas": "Oficinas"}
    ],
    "cat_ubicaciones": [ # NUEVO: Faltaba este
        {"descripcion": "Pasillo A"},
        {"descripcion": "Pasillo B"},
        {"descripcion": "Nivel 1 (Piso)"},
        {"descripcion": "Nivel 2 (Rack)"},
        {"descripcion": "Zona de Carga"}
    ],

    # --- PRODUCTOS ---
    "cat_unidades_medida": [
        {"nombre": "Pieza", "abreviatura": "Pza"},
        {"nombre": "Litro", "abreviatura": "Lt"},
        {"nombre": "Kilogramo", "abreviatura": "Kg"},
        {"nombre": "Caja", "abreviatura": "Cja"},
        {"nombre": "Gramo", "abreviatura": "gr"}
    ],
    "cat_categorias_producto": [
        {"nombre": "Bolis Base Leche", "descripcion": "Base láctea congelada"},
        {"nombre": "Bolis Base Agua", "descripcion": "Base Agua congelada"},
        {"nombre": "Paletas Base Crema", "descripcion": "Paleta Base láctea"},
        {"nombre": "Paletas Base Agua", "descripcion": "Paleta Base Agua"},
        {"nombre": "Helado Base Leche", "descripcion": "Litros de helado Base leche"}, 
        {"nombre": "Helado Base Agua", "descripcion": "Litros de helado Base Agua"}
    ],
    "cat_categorias_materia_prima": [
        {"nombre": "Lácteos", "descripcion": "Leche, Crema, Suero"},
        {"nombre": "Azúcares y Endulzantes", "descripcion": ""}, # OJO: Este es el nombre correcto
        {"nombre": "Saborizantes y Esencias", "descripcion": ""},
        {"nombre": "Empaque Primario", "descripcion": "Bolsitas, Palitos"},
        {"nombre": "Empaque Secundario", "descripcion": "Cajas cartón, Cinta"}
    ],

    # --- ALMACÉN ---
    "cat_tipos_almacen": [
        {"nombre": "Cámara Fría (Congelación)"},
        {"nombre": "Almacén Seco"},
        {"nombre": "Cámara Refrigerada (Conservación)"},
        {"nombre": "Almacén de Refacciones"}
    ],
    "cat_tipos_movimiento_almacen": [ # NUEVO: Requerido por Kárdex
        {"descripcion": "ENTRADA_PRODUCCION"},
        {"descripcion": "REUBICACION_INTERNA"},
        {"descripcion": "SALIDA_EMPAQUE"},
        {"descripcion": "AJUSTE_INVENTARIO"},
        {"descripcion": "BAJA_MERMA"}
    ],

    # --- RH Y OPERACIÓN ---
    "cat_puestos": [
        {"nombre": "Super Administrador", "nivel_acceso": 5},
        {"nombre": "Gerente de Planta", "nivel_acceso": 4},
        {"nombre": "Finanzas / Contador", "nivel_acceso": 4},
        {"nombre": "Programador Producción", "nivel_acceso": 3},
        {"nombre": "Almacenista", "nivel_acceso": 3},
        {"nombre": "Vendedor / Preventista", "nivel_acceso": 2},
        {"nombre": "Maestro Heladero", "nivel_acceso": 2},
        {"nombre": "Repartidor / Chofer", "nivel_acceso": 1}
    ],
    "cat_tipos_vehiculo": [
        {"nombre": "Unidad Refrigerada (Termo)"},
        {"nombre": "Motocicleta"},
        {"nombre": "Automóvil Sedán"}
    ],
    "cat_estados_fisicos": [
        {"descripcion": "Nuevo"},
        {"descripcion": "Bueno / Operativo"},
        {"descripcion": "Regular / Requiere Atención"},
        {"descripcion": "Malo / En Reparación"},
        {"descripcion": "Baja Definitiva"}
    ],

    # --- FINANZAS Y CONTROL ---
    "cat_conceptos_finanzas": [
        {"tipo_flujo": "INGRESO", "descripcion": "Venta Contado Ruta"},
        {"tipo_flujo": "INGRESO", "descripcion": "Cobranza Crédito (Abono)"},
        {"tipo_flujo": "INGRESO", "descripcion": "Aportación de Capital"},
        {"tipo_flujo": "EGRESO", "descripcion": "Pago a Proveedor MP"},
        {"tipo_flujo": "EGRESO", "descripcion": "Pago Nómina"},
        {"tipo_flujo": "EGRESO", "descripcion": "Pago Servicios (Luz/Agua)"},
        {"tipo_flujo": "EGRESO", "descripcion": "Mantenimiento Vehicular"},
        {"tipo_flujo": "DEUDA", "descripcion": "Compra Crédito MP"}
    ],
    "cat_tipos_incidencia": [
        {"descripcion": "Producto Derretido"},
        {"descripcion": "Producto Dañado/Aplastado"},
        {"descripcion": "Robo / Extravío"},
        {"descripcion": "Consumo Interno Autorizado"},
        {"descripcion": "Merma de Producción"},
        {"descripcion": "Error de Conteo"}
    ],
    "cat_bancos_cajas": [
        {"nombre": "Caja Chica Planta"},
        {"nombre": "Caja Fuerte Principal"},
        {"nombre": "Cuenta Fiscal BBVA"},
        {"nombre": "Cuenta Nómina Santander"}
    ],
    
    # --- NUEVOS AGREGADOS DE ARQUITECTURA MAESTRA ---
    "cat_tipos_descuento": [
        {"descripcion": "PORCENTAJE"},
        {"descripcion": "MONTO_FIJO"},
        {"descripcion": "PRECIO_FINAL"}
    ],
    "cat_tipos_pago_solicitado": [
        {"descripcion": "CONTADO"},
        {"descripcion": "CREDITO"}
    ],
    "cat_estados_orden_venta": [
        {"descripcion": "BORRADOR"},
        {"descripcion": "CONFIRMADO"},
        {"descripcion": "EN_PRODUCCION"},
        {"descripcion": "EMPACADO"},
        {"descripcion": "EN_RUTA"},
        {"descripcion": "ENTREGADO"},
        {"descripcion": "CANCELADO"}
    ],
    "cat_estados_plan_produccion": [
        {"descripcion": "PLANIFICADO"},
        {"descripcion": "EN_PROCESO"},
        {"descripcion": "CERRADO"}
    ],
    "cat_estados_orden_empaque": [
        {"descripcion": "EN_PROCESO"},
        {"descripcion": "LISTO_PARA_RUTA"}
    ],
    "cat_tipos_movimiento_finanzas": [
        {"descripcion": "CARGO_VENTA"},
        {"descripcion": "ABONO_EFECTIVO"},
        {"descripcion": "ABONO_TRANSFERENCIA"},
        {"descripcion": "NOTA_CREDITO"}
    ],
    "cat_estados_deuda_empresa": [
        {"descripcion": "PENDIENTE"},
        {"descripcion": "PAGADO"},
        {"descripcion": "VENCIDO"}
    ],
    "cat_tipos_flujo": [
        {"descripcion": "ENTRADA"},
        {"descripcion": "SALIDA"}
    ],
    "cat_origenes_flujo": [
        {"descripcion": "CAPITAL"},
        {"descripcion": "VENTAS"},
        {"descripcion": "PRESTAMO"}
    ],
    "cat_periodos": [
        {"descripcion": "MENSUAL"},
        {"descripcion": "ANUAL"}
    ]
}