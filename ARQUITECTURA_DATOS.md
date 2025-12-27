# ARQUITECTURA DE BASE DE DATOS - GELMEXSYS 2.0 (PostgreSQL)

**Motor:** PostgreSQL 15+
**ORM:** SQLAlchemy
**Estrategia:** Relacional Normalizada (3NF)

---

## 1. DICCIONARIO DE DATOS Y RELACIONES

### A. MÓDULO DE CATÁLOGOS SATÉLITE (Dinámicos)
*El cliente exigió "No Hardcoding". Estas tablas permiten al admin crear nuevos tipos sin llamar al programador.*

1.  **`cat_plantas`**
    * `id` (PK), `descripcion`, `notas`.
2.  **`cat_areas`**
    * `id` (PK), `descripcion`, `notas`.
3.  **`cat_unidades_medida`**
    * `id` (PK), `nombre` (Litro, Pieza), `abreviatura` (Lt, Pza).
4.  **`cat_categorias_producto`**
    * `id` (PK), `nombre` (Bolis Leche, Paletas Agua), `descripcion`.
5.  **`cat_categorias_materia_prima`**
    * `id` (PK), `nombre` (Lácteos, Saborizantes), `descripcion`.
6.  **`cat_tipos_almacen`**
    * `id` (PK), `nombre` (Cámara Fría, Seco, Conservador).
7.  **`cat_puestos`**
    * `id` (PK), `nombre` (Vendedor, Heladero, Repartidor), `nivel_acceso` (1-5).
8.  **`cat_tipos_vehiculo`**
    * `id` (PK), `nombre` (Sedan, Pickup, Refrigerada).
9.  **`cat_modelos_vehiculo`**
    * `id` (PK), `marca`, `modelo`, `anio`.
10. **`cat_modelos_activo`** (Para refrigeradores/congeladores)
    * `id` (PK), `marca`, `modelo`, `capacidad_litros`.
11. **`cat_estados_fisicos`**
    * `id` (PK), `descripcion` (Bueno, Malo, Óptimo, Nuevo, En Taller).

---

### B. MÓDULO DE RECURSOS HUMANOS (Usuarios)

**Tabla: `usuarios`**
*Contiene la ficha completa del empleado.*
* `id` (PK)
* **Datos Personales:**
    * `nombres`, `apellido_paterno`, `apellido_materno`.
    * `fecha_nacimiento`, `estado_civil`, `profesion`.
    * `domicilio_calle`, `domicilio_num_ext`, `domicilio_num_int`, `domicilio_colonia`, `domicilio_cp`, `domicilio_ciudad`, `domicilio_estado`, `domicilio_pais`.
    * `telefono_casa`, `telefono_celular`.
* **Datos Laborales:**
    * `puesto_id` (FK -> `cat_puestos`).
    * `fecha_inicio_empresa`.
    * `calificacion_evaluacion` (1-5 Estrellas).
    * `notas_generales`.
* **Seguridad y Acceso:**
    * `email` (Login), `password_hash`, `pin_seguridad` (6 dígitos).
    * `nivel_usuario` (Heredado de puesto o sobreescrito).
* **Emergencia:**
    * `contacto_emergencia_nombre`, `contacto_emergencia_telefono`.
* **Documentación (Rutas de Archivos en `uploads/usuarios/`):**
    * `foto_perfil` (Uso interno).
    * `img_ine_frente`, `img_ine_reverso`.
    * `img_licencia_frente`, `img_licencia_reverso`, `fecha_validez_licencia`.

---

### C. MÓDULO DE PRODUCTOS Y MATERIA PRIMA

**Tabla: `productos`**
* `id` (PK), `sku` (Único).
* `descripcion`.
* `categoria_id` (FK -> `cat_categorias_producto`).
* `unidad_id` (FK -> `cat_unidades_medida`).
* **Costos y Precios:**
    * `precio_costo_actual`.
    * `precio_venta_general` (Base).
* **Físico:**
    * `peso_gramos`, `caducidad_dias`.
    * `imagen_producto` (300x300 jpg, ruta).

**Tabla: `materia_prima`**
* `id` (PK), `sku`, `descripcion`.
* `categoria_id` (FK -> `cat_categorias_materia_prima`).
* `unidad_id` (FK -> `cat_unidades_medida`).
* `precio_costo_promedio`.
* `precio_venta_general` (Base).
* `peso_gramos`, `caducidad_dias`.
* `imagen_materia` (300x300 jpg, ruta).

---

### D. MÓDULO DE INFRAESTRUCTURA E INVENTARIOS

**Tabla: `almacenes`**
* `id` (PK), `descripcion`.
* `tipo_id` (FK -> `cat_tipos_almacen`).
* `planta_id` (FK -> `cat_plantas`).
* `area_id` (FK -> `cat_areas`).
* `imagen_almacen` (300x300 jpg).

**Tabla: `ubicaciones_almacen`**
* `id` (PK), `codigo` (Ej: CFPA001B004).
* `almacen_id` (FK -> `almacenes`).
* `notas`.

**Tabla: `inventario_lotes` (El corazón del stock)**
* `id` (PK).
* **Qué es:**
    * `producto_id` (FK, Nullable).
    * `materia_prima_id` (FK, Nullable).
* **Dónde está:**
    * `ubicacion_id` (FK -> `ubicaciones_almacen`).
* **Cuánto hay:**
    * `cantidad_actual`.
    * `fecha_produccion` (Lote).
    * `fecha_ingreso_almacen`.
    * `stock_minimo`.
    * `stock_maximo`.
    * `stock_ideal`.
* **Semáforos (Definidos por producto, pero guardados aquí para snapshot o referenciados):**
    * (Lógica: Se compara `cantidad_actual` vs `Producto.stock_minimo` o `cantidad_actual` vs `Producto.stock_maximo`).

---

### E. MÓDULO DE LOGÍSTICA Y ACTIVOS

**Tabla: `vehiculos`**
* `id` (PK), `placas`.
* `serie_vehiculo`.
* `tipo_id` (FK -> `cat_tipos_vehiculo`).
* `modelo_id` (FK -> `cat_modelos_vehiculo`).
* `estado_llantas_id` (FK -> `cat_estados_fisicos`).
* `estado_general_id` (FK -> `cat_estados_fisicos`).
* `kilometraje_ultimo_servicio`.
* `asignado` (Boolean).
* **Fechas Críticas:**
    * `fecha_ultimo_servicio`, `fecha_proximo_servicio`.
    * `fecha_vencimiento_seguro`, `fecha_vencimiento_verificacion`.
* **Evidencia (600x400 jpg):**
    * `img_vehiculo`, `img_motor`, `img_odometro`.

**Tabla: `activos_frio` (Congeladores)**
* `id` (PK), `serie`, `descripcion`.
* `modelo_id` (FK -> `cat_modelos_activo`).
* `estado_id` (FK -> `cat_estados_fisicos`).
* `asignado` (Boolean).
* `img_activo` (300x300 jpg).
* `fecha_ultimo_mtto`, `fecha_proximo_mtto`.

**Tabla: `rutas_reparto`**
* `id` (PK), `descripcion`.
* `img_mapa` (600x400 jpg).
* `notas`.

---

### F. MÓDULO DE VENTAS Y CLIENTES (Complejidad Alta)

**Tabla: `clientes`**
* `id` (PK).
* **Negocio:**
    * `nombre_negocio`, `tipo_negocio`.
    * `img_fachada` (300x300 jpg).
    * `calificacion` (1-5).
* **Encargado:**
    * `nombres_encargado`, `apellido_p_encargado`, `apellido_m_encargado`.
    * `img_ine_frente`, `img_ine_reverso`.
    * `domicilio_completo` (Desglosado igual que usuarios).
* **Financiero:**
    * `Vendedor_habitual_id` (FK -> `usuarios`, Nullable).
    * `limite_credito` (Cuánto le fía GelMex).
    * `saldo_actual` (Deuda actual).
* **Logística:**
    * `ruta_id` (FK -> `rutas_reparto`).
    * `repartidor_habitual_id` (FK -> `usuarios`, Nullable).

**Tabla: `asignacion_activos_cliente`**
* `cliente_id` (FK).
* `activo_frio_id` (FK).
* `fecha_asignacion`.

**Tabla: `precios_especiales_cliente` (Regla de Negocio Crítica)**
* *Esta tabla permite que cada cliente tenga un precio diferente.*
* `id` (PK).
* `cliente_id` (FK).
* `producto_id` (FK).
* `tipo_descuento`: ('PORCENTAJE', 'MONTO_FIJO', 'PRECIO_FINAL').
* `valor_descuento`: (Ej. 10, 5.00, 15.50).
* *Lógica:* Al vender, el sistema busca aquí primero. Si no encuentra, usa `Producto.precio_venta_general`.

---

## 2. LÓGICA DE PROCEDIMIENTOS Y VISTAS

### A. Vistas (Views) para Reportes Rápidos
Estas vistas se crearán en la BD para facilitar el trabajo de los Dashboards.

1.  **`view_inventario_global`**:
    * Suma el stock de todas las ubicaciones agrupado por SKU.
    * Muestra: SKU, Descripción, Total Plantas, Total Rutas, Total General.

2.  **`view_estado_credito`**:
    * Lista clientes con `saldo_actual > 0`.
    * Calcula `credito_disponible` = `limite_credito` - `saldo_actual`.
    * Alerta si `saldo_actual` >= `limite_credito`.

### B. Lógica de Transacciones (Procedimientos "Lógicos")
No usaremos Stored Procedures de SQL (PL/pgSQL) para la lógica de negocio, usaremos **Servicios en Python** (capa intermedia) para mantener el control de versiones, pero la lógica será transaccional (Atomicity).

1.  **Procedimiento `CrearPedido`:**
    * Input: Cliente, Lista de Items.
    * Validación 1: ¿El cliente tiene crédito suficiente? (Si es venta a crédito).
    * Cálculo: Iterar items -> Buscar si existe `precios_especiales_cliente` -> Calcular Subtotal.
    * Output: Orden en estado "BORRADOR" o "CONFIRMADO".

2.  **Procedimiento `ConfirmarProduccion` (Maestro Heladero):**
    * Input: Orden de Producción, Cantidad Real Producida.
    * Acción:
        * Restar Materia Prima (según receta - *Futuro*).
        * Sumar Stock a "Ubicación Temporal Producción".
        * Crear registro en `inventario_lotes`.

3.  **Procedimiento `CierreRuta` (Finanzas):**
    * Input: ID Ruta, Efectivo Entregado, Notas de Crédito Firmadas.
    * Acción:
        * Actualizar `saldo_actual` de cada cliente (Resta abonos, suma nuevos pedidos a crédito).
        * Conciliar Stock del camión (Lo que salió vs lo que volvió vs lo vendido).

---

## 3. ESTRATEGIA DE SEMILLAS (DB SEEDS)

Para el archivo `db_seeds.py`, seguiremos este orden estricto de llenado para evitar errores de Llaves Foráneas (FK):

1.  **Nivel 0 (Catálogos Duros):** Unidades de medida, Tipos de Almacén, Estados Físicos.
2.  **Nivel 1 (Infraestructura):** Plantas, Áreas, Rutas base.
3.  **Nivel 2 (Categorías):** Categorías de Productos y Materia Prima, Puestos.
4.  **Nivel 3 (Recursos):** Productos Base, Almacenes físicos, Vehículos demo.
5.  **Nivel 4 (Usuarios):** Crear al "Super Admin" (Dios) y un Vendedor demo.