# Reporte de Auditoría de Arquitectura GelMex

## Tabla: `caja_empresa`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('caja_empresa_id_seq'::regclass) |
| saldo_actual | NUMERIC(10, 2) | True | None |
| ultima_actualizacion | TIMESTAMP | True | None |

### Muestra de Datos (Top 3)
| id | saldo_actual | ultima_actualizacion |
| --- | --- | --- |
| 1 | 193683.99 | 2026-03-01 15:49:01.809031 |

---

## Tabla: `cat_tipos_flujo`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| descripcion | VARCHAR(50) | False | None |
| id | INTEGER | False | nextval('cat_tipos_flujo_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| descripcion | id | activo |
| --- | --- | --- |
| ENTRADA | 1 | True |
| SALIDA | 2 | True |

---

## Tabla: `clientes`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('clientes_id_seq'::regclass) |
| nombre_negocio | VARCHAR(150) | False | None |
| rfc | VARCHAR(13) | True | None |
| tipo_negocio | VARCHAR(100) | True | None |
| img_fachada | VARCHAR(255) | True | None |
| calificacion | INTEGER | True | None |
| nombres_encargado | VARCHAR(100) | True | None |
| apellidos_encargado | VARCHAR(100) | True | None |
| img_ine_frente | VARCHAR(255) | True | None |
| img_ine_reverso | VARCHAR(255) | True | None |
| calle | VARCHAR(100) | True | None |
| num_exterior | VARCHAR(20) | True | None |
| num_interior | VARCHAR(20) | True | None |
| colonia | VARCHAR(100) | True | None |
| ciudad | VARCHAR(100) | True | None |
| codigo_postal | VARCHAR(10) | True | None |
| estado | VARCHAR(100) | True | None |
| pais | VARCHAR(100) | True | None |
| limite_credito | NUMERIC(12, 2) | True | None |
| saldo_actual | NUMERIC(12, 2) | True | None |
| ruta_id | INTEGER | True | None |
| repartidor_habitual_id | INTEGER | True | None |
| vendedor_habitual_id | INTEGER | True | None |
| activo | BOOLEAN | True | true |
| telefono | VARCHAR(20) | True | None |
| celular | VARCHAR(20) | True | None |
| email | VARCHAR(150) | True | None |

### Muestra de Datos (Top 3)
| id | nombre_negocio | rfc | tipo_negocio | img_fachada | calificacion | nombres_encargado | apellidos_encargado | img_ine_frente | img_ine_reverso | calle | num_exterior | num_interior | colonia | ciudad | codigo_postal | estado | pais | limite_credito | saldo_actual | ruta_id | repartidor_habitual_id | vendedor_habitual_id | activo | telefono | celular | email |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | PRIMARIA SAN PEDRO TARIMBARO | SIN RFC | ESCUELA PRIMARIA | NULL | 5 | BETI | BETI | NULL | NULL | MELCHOR OCAMPO | 13 | NULL | TARIMBARO | TARIMBARO | 789900 | Guanajuato | México | 10000.00 | 0.00 | 1 | 4 | 2 | True | 7121279798 | 7121479798 |  |
| 5 | PRIMARIA SAN PEDRO TARIMBARO | SIN RFC | ESCUELA PRIMARIA | NULL | 5 | BETI | BETI | NULL | NULL | MELCHOR OCAMPO | 13 | NULL | TARIMBARO | TARIMBARO | 789900 | Guanajuato | México | 10000.00 | 0.00 | 1 | 4 | 2 | False | 7121279798 | 7121479798 |  |
| 7 | SEC TECNICA 58 |  | ESCUELA SECUNDARIA | NULL | 5 | REINA | REINA | NULL | NULL | BENITO JUAREZ | 11 | NULL | SENGUIO | SENGUIO | SIN | Guanajuato | México | 0.00 | 0.00 | 1 | 4 | 2 | True | 7297614670 | 7297614670 |  |

---

## Tabla: `materia_prima`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('materia_prima_id_seq'::regclass) |
| sku | VARCHAR(50) | False | None |
| descripcion | VARCHAR(200) | False | None |
| categoria_id | INTEGER | True | None |
| unidad_id | INTEGER | True | None |
| precio_costo_promedio | NUMERIC(10, 2) | True | None |
| precio_venta_general | NUMERIC(10, 2) | True | None |
| peso_gramos | DOUBLE PRECISION | True | None |
| caducidad_dias | INTEGER | True | None |
| imagen_materia | VARCHAR(255) | True | None |
| stock_minimo | DOUBLE PRECISION | True | None |
| stock_maximo | DOUBLE PRECISION | True | None |
| stock_ideal | DOUBLE PRECISION | True | None |

### Muestra de Datos (Top 3)
| id | sku | descripcion | categoria_id | unidad_id | precio_costo_promedio | precio_venta_general | peso_gramos | caducidad_dias | imagen_materia | stock_minimo | stock_maximo | stock_ideal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | AZU-BUL-50 | Bulto de Az├║car Est├índar 50kg | 2 | 3 | 22.50 | 28.00 | 1000.0 | 365 | uploads/materias/azucar.jpg | 100.0 | 1000.0 | 500.0 |

---

## Tabla: `productos`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('productos_id_seq'::regclass) |
| sku | VARCHAR(50) | False | None |
| descripcion | VARCHAR(200) | False | None |
| categoria_id | INTEGER | True | None |
| unidad_id | INTEGER | True | None |
| precio_costo_actual | NUMERIC(10, 2) | True | None |
| precio_venta_general | NUMERIC(10, 2) | True | None |
| peso_gramos | DOUBLE PRECISION | True | None |
| caducidad_dias | INTEGER | True | None |
| imagen_producto | VARCHAR(255) | True | None |
| stock_minimo | DOUBLE PRECISION | True | None |
| stock_maximo | DOUBLE PRECISION | True | None |
| stock_ideal | DOUBLE PRECISION | True | None |
| activo | BOOLEAN | True | true |

### Muestra de Datos (Top 3)
| id | sku | descripcion | categoria_id | unidad_id | precio_costo_actual | precio_venta_general | peso_gramos | caducidad_dias | imagen_producto | stock_minimo | stock_maximo | stock_ideal | activo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | PAL-FRE-CRM | Paleta de Fresa con Crema | 3 | 1 | 4.00 | 12.00 | 120.0 | 45 | NULL | 50.0 | 1000.0 | 500.0 | True |
| 25 | PAL-MED-FER | PALETA FERRERO | 3 | 1 | 2.86 | 13.00 | 0.75 | 90 | uploads/productos/PAL-MED-FER_d1c77515-a4ca-49c8-8b92-7b5442412364.JPG | 500.0 | 1450.0 | 1300.0 | True |
| 1 | BOL-LIM-STD | Boli de Limon (Tamaño Estandar) | 2 | 1 | 2.50 | 6.00 | 150.0 | 30 | NULL | 100.0 | 2000.0 | 1000.0 | True |

---

## Tabla: `vehiculos`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('vehiculos_id_seq'::regclass) |
| placas | VARCHAR(20) | True | None |
| serie_vehiculo | VARCHAR(50) | True | None |
| tipo_id | INTEGER | True | None |
| modelo_id | INTEGER | True | None |
| asignado | BOOLEAN | True | None |
| kilometraje_ultimo_servicio | DOUBLE PRECISION | True | None |

### Muestra de Datos (Top 3)
*Tabla vacía*

---

## Tabla: `cat_bancos_cajas`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| nombre | VARCHAR(100) | False | None |
| id | INTEGER | False | nextval('cat_bancos_cajas_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| nombre | id | activo |
| --- | --- | --- |
| Caja Chica Planta | 1 | True |
| Caja Fuerte Principal | 2 | True |
| Cuenta Fiscal BBVA | 3 | True |

---

## Tabla: `cat_conceptos_finanzas`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| tipo_flujo | VARCHAR(20) | False | None |
| descripcion | VARCHAR(100) | False | None |
| id | INTEGER | False | nextval('cat_conceptos_finanzas_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| tipo_flujo | descripcion | id | activo |
| --- | --- | --- | --- |
| INGRESO | Venta Contado Ruta | 1 | True |
| EGRESO | Pago a Proveedor MP | 4 | True |
| EGRESO | Pago Servicios (Luz/Agua) | 6 | True |

---

## Tabla: `cat_estados_deuda_empresa`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| descripcion | VARCHAR(50) | False | None |
| id | INTEGER | False | nextval('cat_estados_deuda_empresa_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| descripcion | id | activo |
| --- | --- | --- |
| PENDIENTE | 1 | True |
| PAGADO | 2 | True |
| VENCIDO | 3 | True |

---

## Tabla: `cat_estados_orden_empaque`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| descripcion | VARCHAR(50) | False | None |
| id | INTEGER | False | nextval('cat_estados_orden_empaque_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| descripcion | id | activo |
| --- | --- | --- |
| EN_PROCESO | 1 | True |
| LISTO_PARA_RUTA | 2 | True |

---

## Tabla: `cat_estados_orden_venta`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| descripcion | VARCHAR(50) | False | None |
| id | INTEGER | False | nextval('cat_estados_orden_venta_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| descripcion | id | activo |
| --- | --- | --- |
| BORRADOR | 1 | True |
| CONFIRMADO | 2 | True |
| EN_PRODUCCION | 3 | True |

---

## Tabla: `cat_estados_plan_produccion`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| descripcion | VARCHAR(50) | False | None |
| id | INTEGER | False | nextval('cat_estados_plan_produccion_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| descripcion | id | activo |
| --- | --- | --- |
| PLANIFICADO | 1 | True |
| EN_PROCESO | 2 | True |
| CERRADO | 3 | True |

---

## Tabla: `cat_origenes_flujo`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| descripcion | VARCHAR(50) | False | None |
| id | INTEGER | False | nextval('cat_origenes_flujo_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| descripcion | id | activo |
| --- | --- | --- |
| CAPITAL | 1 | True |
| VENTAS | 2 | True |
| PRESTAMO | 3 | True |

---

## Tabla: `cat_periodos`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| descripcion | VARCHAR(50) | False | None |
| id | INTEGER | False | nextval('cat_periodos_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| descripcion | id | activo |
| --- | --- | --- |
| MENSUAL | 1 | True |
| ANUAL | 2 | True |

---

## Tabla: `cat_modelos_activo`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| marca | VARCHAR(50) | False | None |
| modelo | VARCHAR(50) | False | None |
| capacidad_litros | DOUBLE PRECISION | True | None |
| id | INTEGER | False | nextval('cat_modelos_activo_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
*Tabla vacía*

---

## Tabla: `cat_areas`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| descripcion | VARCHAR(100) | False | None |
| notas | VARCHAR(255) | True | None |
| id | INTEGER | False | nextval('cat_areas_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| descripcion | notas | id | activo |
| --- | --- | --- | --- |
| Administración | Oficinas | 3 | True |
| Logística y Carga | Andenes | 2 | True |
| Producción | Zona Congelacion | 1 | True |

---

## Tabla: `almacenes`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('almacenes_id_seq'::regclass) |
| descripcion | VARCHAR(100) | False | None |
| imagen_almacen | VARCHAR(255) | True | None |
| tipo_id | INTEGER | True | None |
| planta_id | INTEGER | True | None |
| area_id | INTEGER | True | None |

### Muestra de Datos (Top 3)
| id | descripcion | imagen_almacen | tipo_id | planta_id | area_id |
| --- | --- | --- | --- | --- | --- |
| 1 | Cámara Fría Principal (Producto Terminado) | NULL | 1 | 1 | 2 |

---

## Tabla: `cat_plantas`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| descripcion | VARCHAR(100) | False | None |
| notas | VARCHAR(255) | True | None |
| id | INTEGER | False | nextval('cat_plantas_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| descripcion | notas | id | activo |
| --- | --- | --- | --- |
| Planta Matriz Hgo | Producción Principal | 1 | True |

---

## Tabla: `cat_tipos_almacen`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| nombre | VARCHAR(50) | False | None |
| id | INTEGER | False | nextval('cat_tipos_almacen_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| nombre | id | activo |
| --- | --- | --- |
| Almacén de Refacciones | 4 | True |
| Cámara Refrigerada (Conservación) | 3 | True |
| Almacén Seco | 2 | True |

---

## Tabla: `cat_categorias_materia_prima`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| nombre | VARCHAR(100) | False | None |
| descripcion | VARCHAR(255) | True | None |
| id | INTEGER | False | nextval('cat_categorias_materia_prima_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| nombre | descripcion | id | activo |
| --- | --- | --- | --- |
| Empaque Primario | Bolsitas, Palitos | 3 | True |
| Empaque Secundario | Cajas carton, Cinta | 4 | True |
| Azucares y Endulzantes |  | 2 | True |

---

## Tabla: `cat_tipos_descuento`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| descripcion | VARCHAR(50) | False | None |
| id | INTEGER | False | nextval('cat_tipos_descuento_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| descripcion | id | activo |
| --- | --- | --- |
| PORCENTAJE | 1 | True |
| MONTO_FIJO | 2 | True |
| PRECIO_FINAL | 3 | True |

---

## Tabla: `cat_categorias_producto`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| nombre | VARCHAR(100) | False | None |
| descripcion | VARCHAR(255) | True | None |
| id | INTEGER | False | nextval('cat_categorias_producto_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| nombre | descripcion | id | activo |
| --- | --- | --- | --- |
| Bolis Base Agua | Base Agua congelada | 2 | True |
| Paletas Base Agua | Paleta Base Agua | 4 | True |
| Helado Base Leche | Litros de helado Base leche | 5 | True |

---

## Tabla: `cat_puestos`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| nombre | VARCHAR(50) | False | None |
| nivel_acceso | INTEGER | True | None |
| id | INTEGER | False | nextval('cat_puestos_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| nombre | nivel_acceso | id | activo |
| --- | --- | --- | --- |
| Super Administrador | 5 | 1 | True |
| Gerente de Planta | 4 | 2 | True |
| Almacenista | 3 | 5 | True |

---

## Tabla: `cat_modelos_vehiculo`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| marca | VARCHAR(50) | False | None |
| modelo | VARCHAR(50) | False | None |
| anio | INTEGER | True | None |
| id | INTEGER | False | nextval('cat_modelos_vehiculo_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
*Tabla vacía*

---

## Tabla: `cat_tipos_incidencia`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| descripcion | VARCHAR(100) | False | None |
| id | INTEGER | False | nextval('cat_tipos_incidencia_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| descripcion | id | activo |
| --- | --- | --- |
| Producto Derretido | 1 | True |
| Consumo Interno Autorizado | 4 | True |
| Error de Conteo | 6 | True |

---

## Tabla: `cat_tipos_movimiento_almacen`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| descripcion | VARCHAR(50) | False | None |
| id | INTEGER | False | nextval('cat_tipos_movimiento_almacen_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| descripcion | id | activo |
| --- | --- | --- |
| ENTRADA_PRODUCCION | 1 | True |
| REUBICACION_INTERNA | 2 | True |
| SALIDA_EMPAQUE | 3 | True |

---

## Tabla: `cat_tipos_pago_solicitado`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| descripcion | VARCHAR(50) | False | None |
| id | INTEGER | False | nextval('cat_tipos_pago_solicitado_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| descripcion | id | activo |
| --- | --- | --- |
| CONTADO | 1 | True |
| CREDITO | 2 | True |

---

## Tabla: `cat_tipos_movimiento_finanzas`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| descripcion | VARCHAR(50) | False | None |
| id | INTEGER | False | nextval('cat_tipos_movimiento_finanzas_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| descripcion | id | activo |
| --- | --- | --- |
| CARGO_VENTA | 1 | True |
| ABONO_EFECTIVO | 2 | True |
| ABONO_TRANSFERENCIA | 3 | True |

---

## Tabla: `cat_unidades_medida`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| nombre | VARCHAR(50) | False | None |
| abreviatura | VARCHAR(10) | False | None |
| id | INTEGER | False | nextval('cat_unidades_medida_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| nombre | abreviatura | id | activo |
| --- | --- | --- | --- |
| Pieza | Pza | 1 | True |
| Litro | Lt | 2 | True |
| Kilogramo | Kg | 3 | True |

---

## Tabla: `cat_tipos_vehiculo`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| nombre | VARCHAR(50) | False | None |
| id | INTEGER | False | nextval('cat_tipos_vehiculo_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| nombre | id | activo |
| --- | --- | --- |
| Unidad Refrigerada (Termo) | 1 | True |
| Motocicleta | 2 | True |
| Automóvil Sedan | 3 | True |

---

## Tabla: `movimientos_temporales`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('movimientos_temporales_id_seq'::regclass) |
| orden_venta_id | INTEGER | False | None |
| producto_id | INTEGER | True | None |
| ubicacion_origen_id | INTEGER | True | None |
| cantidad | DOUBLE PRECISION | False | None |
| estado | VARCHAR(20) | True | None |

### Muestra de Datos (Top 3)
*Tabla vacía*

---

## Tabla: `precios_especiales_cliente`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('precios_especiales_cliente_id_seq'::regclass) |
| cliente_id | INTEGER | True | None |
| producto_id | INTEGER | True | None |
| tipo_descuento_id | INTEGER | True | None |
| valor_descuento | NUMERIC(10, 2) | False | None |

### Muestra de Datos (Top 3)
| id | cliente_id | producto_id | tipo_descuento_id | valor_descuento |
| --- | --- | --- | --- | --- |
| 2 | 1 | 2 | 1 | 10.00 |
| 3 | 1 | 1 | 2 | 5.50 |
| 4 | 1 | 3 | 2 | 135.50 |

---

## Tabla: `orden_paquetes`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('orden_paquetes_id_seq'::regclass) |
| orden_id | INTEGER | False | None |
| codigo_etiqueta | VARCHAR(50) | True | None |
| numero_caja | INTEGER | True | None |
| total_cajas_orden | INTEGER | True | None |
| descripcion_contenido | VARCHAR(255) | True | None |
| peso_kg | DOUBLE PRECISION | True | 0.0 |
| creado_por_id | INTEGER | True | None |
| fecha_creacion | TIMESTAMP | True | now() |

### Muestra de Datos (Top 3)
| id | orden_id | codigo_etiqueta | numero_caja | total_cajas_orden | descripcion_contenido | peso_kg | creado_por_id | fecha_creacion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | #251227195737_Ruta 1_B1/3 | 1 | 3 | mantener congelado este envi├│ porfas | 0.0 | 1 | 2025-12-29 11:54:16.016251 |
| 2 | 1 | #251227195737_Ruta 1_B2/3 | 2 | 3 | mantener congelado este envi├│ porfas | 0.0 | 1 | 2025-12-29 11:54:16.016251 |
| 3 | 1 | #251227195737_Ruta 1_B3/3 | 3 | 3 | mantener congelado este envi├│ porfas | 0.0 | 1 | 2025-12-29 11:54:16.016251 |

---

## Tabla: `ordenes_venta`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('ordenes_venta_id_seq'::regclass) |
| folio | VARCHAR(20) | False | None |
| cliente_id | INTEGER | False | None |
| vendedor_id | INTEGER | False | None |
| fecha_registro | TIMESTAMP | True | None |
| fecha_promesa_entrega | DATE | False | None |
| estado | VARCHAR(25) | True | None |
| metodo_pago_esperado | VARCHAR(20) | True | None |
| total_venta | DOUBLE PRECISION | True | None |
| notas_vendedor | TEXT | True | None |
| saldo_pendiente | NUMERIC(12, 2) | True | 0.00 |

### Muestra de Datos (Top 3)
| id | folio | cliente_id | vendedor_id | fecha_registro | fecha_promesa_entrega | estado | metodo_pago_esperado | total_venta | notas_vendedor | saldo_pendiente |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | PV-251228125126 | 1 | 1 | 2025-12-28 18:51:26.261454 | 2025-12-28 | ENTREGADA | Credito | 3320.0 | NULL | 1020.00 |
| 2 | PV-251228094136 | 1 | 1 | 2025-12-28 15:41:36.058850 | 2025-12-28 | PRODUCCION | Credito | 800.0 | NULL | 800.00 |
| 3 | PV-251228095013 | 1 | 1 | 2025-12-28 15:50:13.760318 | 2025-12-28 | PRODUCCION | Credito | 3000.0 | NULL | 3000.00 |

---

## Tabla: `pagos`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('pagos_id_seq'::regclass) |
| folio_recibo | VARCHAR(50) | False | None |
| cliente_id | INTEGER | False | None |
| orden_id | INTEGER | False | None |
| tipo_movimiento_id | INTEGER | False | None |
| cobrado_por_id | INTEGER | False | None |
| auditado_por_id | INTEGER | True | None |
| monto_pago | NUMERIC(12, 2) | False | None |
| dinero_recibido | NUMERIC(12, 2) | True | None |
| cambio_devuelto | NUMERIC(12, 2) | True | None |
| referencia | VARCHAR(100) | True | None |
| estado | VARCHAR(20) | True | 'POR_AUDITAR'::character varying |
| fecha_registro | TIMESTAMP | True | now() |
| fecha_auditoria | TIMESTAMP | True | None |
| notas | TEXT | True | None |

### Muestra de Datos (Top 3)
| id | folio_recibo | cliente_id | orden_id | tipo_movimiento_id | cobrado_por_id | auditado_por_id | monto_pago | dinero_recibido | cambio_devuelto | referencia | estado | fecha_registro | fecha_auditoria | notas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 7 | PAG-251229-TT5F | 1 | 6 | 2 | 1 | 1 | 300.00 | 300.00 | 0.00 | NULL | AUDITADO | 2025-12-29 21:19:56.366842 | 2025-12-30 07:46:28.014710 | COBRANZA: abono 300 a esta orden don pepe bien buena onda lo amo |
| 5 | PAG-251229-6 | 1 | 6 | 2 | 1 | 1 | 2000.00 | 2000.00 | 0.00 | NULL | AUDITADO | 2025-12-29 21:07:06.285101 | 2025-12-30 07:46:30.543855 | COBRANZA: pago $2000.00 de esta orden pendiente don Jos├® muy buena onda he |
| 3 | PAG-251229-5 | 1 | 5 | 2 | 1 | 1 | 2590.00 | 5000.00 | 2410.00 | NULL | AUDITADO | 2025-12-29 15:48:53.522409 | 2025-12-30 07:46:31.493321 | pago el pedido con efectivo |

---

## Tabla: `gastos_operativos`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('gastos_operativos_id_seq'::regclass) |
| categoria | VARCHAR(50) | True | None |
| descripcion | VARCHAR(255) | True | None |
| monto | NUMERIC(10, 2) | False | None |
| fecha_registro | TIMESTAMP | True | None |
| registrado_por_id | INTEGER | True | None |
| proveedor_id | INTEGER | True | None |
| notas | TEXT | True | None |

### Muestra de Datos (Top 3)
| id | categoria | descripcion | monto | fecha_registro | registrado_por_id | proveedor_id | notas |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Pago a Proveedor MP | pago de servicios 104039 | 1000.00 | 2025-12-30 08:46:31.670935 | 1 | NULL | se pag├│ por el servicio de programaci├│n Edwared |

---

## Tabla: `historial_movimientos`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('historial_movimientos_id_seq'::regclass) |
| producto_id | INTEGER | True | None |
| ubicacion_id | INTEGER | True | None |
| tipo_movimiento | VARCHAR(50) | True | None |
| cantidad | DOUBLE PRECISION | False | None |
| usuario_id | INTEGER | True | None |
| fecha | TIMESTAMP | True | None |
| referencia | VARCHAR(100) | True | None |
| notas | TEXT | True | None |

### Muestra de Datos (Top 3)
| id | producto_id | ubicacion_id | tipo_movimiento | cantidad | usuario_id | fecha | referencia | notas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | AJUSTE_INVENTARIO | 1200.0 | 1 | 2025-12-28 10:59:14.901971 | NULL | inventario inicial \| Ubic: CF1-PAS1-NV1 \| 0 -> -1200.0 |
| 2 | 1 | 1 | INVENTARIO_INICIAL | 1200.0 | 1 | 2025-12-28 11:06:52.096218 | NULL | inventario inicial \| Saldo: -1200.0 -> 1200.0 |
| 3 | 2 | 1 | INVENTARIO_INICIAL | 1000.0 | 1 | 2025-12-28 11:37:53.923896 | NULL | inventario incial \| Saldo: 0 -> 1000.0 |

---

## Tabla: `orden_venta_detalles`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('orden_venta_detalles_id_seq'::regclass) |
| orden_id | INTEGER | False | None |
| producto_id | INTEGER | False | None |
| cantidad_pedida | DOUBLE PRECISION | False | None |
| cantidad_surtida | DOUBLE PRECISION | True | None |
| cantidad_entregada | DOUBLE PRECISION | True | None |
| precio_unitario | DOUBLE PRECISION | False | None |
| subtotal | DOUBLE PRECISION | False | None |

### Muestra de Datos (Top 3)
| id | orden_id | producto_id | cantidad_pedida | cantidad_surtida | cantidad_entregada | precio_unitario | subtotal |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 2 | 2 | 5.0 | 0.0 | 0.0 | 10.0 | 50.0 |
| 4 | 2 | 3 | 5.0 | 0.0 | 0.0 | 150.0 | 750.0 |
| 5 | 3 | 3 | 20.0 | 0.0 | 0.0 | 150.0 | 3000.0 |

---

## Tabla: `ordenes_produccion`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('ordenes_produccion_id_seq'::regclass) |
| folio | VARCHAR(50) | False | None |
| producto_id | INTEGER | False | None |
| receta_id | INTEGER | True | None |
| cantidad | DOUBLE PRECISION | False | None |
| usuario_solicita_id | INTEGER | False | None |
| fecha_solicitud | TIMESTAMP | True | None |
| fecha_inicio | TIMESTAMP | True | None |
| fecha_termino | TIMESTAMP | True | None |
| estatus | VARCHAR(20) | True | None |
| prioridad | VARCHAR(20) | True | None |
| cantidad_producida_real | DOUBLE PRECISION | True | 0 |
| notas_produccion | TEXT | True | None |
| cantidad_recibida_almacen | DOUBLE PRECISION | True | 0 |

### Muestra de Datos (Top 3)
| id | folio | producto_id | receta_id | cantidad | usuario_solicita_id | fecha_solicitud | fecha_inicio | fecha_termino | estatus | prioridad | cantidad_producida_real | notas_produccion | cantidad_recibida_almacen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ORD-20251228-1 | 2 | NULL | 620.0 | 1 | 2025-12-28 13:03:06.503540 | 2025-12-28 13:53:45.280458 | 2025-12-28 16:21:40.258665 | TERMINADA | NORMAL | 1000.0 | el lote sali├│ bien perro y el producto sabe incre├¡ble soy la mera verdura | 1000.0 |
| 3 | ORD-20251228-3 | 2 | NULL | 20.0 | 1 | 2025-12-28 14:00:17.704779 | 2025-12-28 14:04:26.666551 | 2025-12-28 16:29:49.670513 | TERMINADA | NORMAL | 20.0 | todo ok con esta perra orden | 20.0 |
| 5 | ORD-251228-1-DE85 | 1 | NULL | 600.0 | 1 | 2025-12-28 14:04:14.639073 | 2025-12-28 14:04:49.269311 | 2025-12-28 16:45:39.976522 | TERMINADA | NORMAL | 1000.0 | todo bien chingon ademas sabe perron yame comi dos bolis | 1000.0 |

---

## Tabla: `rutas_reparto`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('rutas_reparto_id_seq'::regclass) |
| descripcion | VARCHAR(100) | False | None |
| img_mapa | VARCHAR(255) | True | None |
| notas | TEXT | True | None |

### Muestra de Datos (Top 3)
| id | descripcion | img_mapa | notas |
| --- | --- | --- | --- |
| 2 | Ruta 2: Queretaro | NULL | Martes y Jueves |
| 3 | Ruta 3: Zinapecuaro | NULL | Sabados |
| 1 | Ruta 1: Acambaro | None | Lunes |

---

## Tabla: `ubicaciones_almacen`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('ubicaciones_almacen_id_seq'::regclass) |
| codigo | VARCHAR(50) | False | None |
| notas | VARCHAR(255) | True | None |
| almacen_id | INTEGER | True | None |
| cat_ubicacion_id | INTEGER | True | None |

### Muestra de Datos (Top 3)
| id | codigo | notas | almacen_id | cat_ubicacion_id |
| --- | --- | --- | --- | --- |
| 4 | TORRE-04 | TORRE ALM 04 | 1 | NULL |
| 5 | TORRE-05 | TORRE ALM 05 | 1 | NULL |
| 6 | TORRE-06 | TORRE ALM 06 | 1 | NULL |

---

## Tabla: `transacciones_financieras`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('transacciones_financieras_id_seq'::regclass) |
| tipo | VARCHAR(20) | True | None |
| monto | NUMERIC(10, 2) | False | None |
| concepto | VARCHAR(255) | True | None |
| fecha | TIMESTAMP | True | None |
| usuario_id | INTEGER | True | None |
| pago_origen_id | INTEGER | True | None |
| gasto_id | INTEGER | True | None |
| folio | VARCHAR(50) | False | None |
| notas | TEXT | True | None |

### Muestra de Datos (Top 3)
| id | tipo | monto | concepto | fecha | usuario_id | pago_origen_id | gasto_id | folio | notas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INGRESO | 300.00 | Corte Caja - Pago Chofer PAG-251229-TT5F | 2025-12-30 07:46:28.021973 | 1 | 7 | NULL | TES-ING-251230-K9LC | Orden: PV-251228125126. Cliente: Abarrotes Don Pepe |
| 2 | INGRESO | 2000.00 | Corte Caja - Pago Chofer PAG-251229-6 | 2025-12-30 07:46:30.548460 | 1 | 5 | NULL | TES-ING-251230-QSLQ | Orden: PV-251228125126. Cliente: Abarrotes Don Pepe |
| 3 | INGRESO | 2590.00 | Corte Caja - Pago Chofer PAG-251229-5 | 2025-12-30 07:46:31.496365 | 1 | 3 | NULL | TES-ING-251230-TDRR | Orden: PV-251228121120. Cliente: Abarrotes Don Pepe |

---

## Tabla: `cat_estados_fisicos`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| descripcion | VARCHAR(50) | False | None |
| id | INTEGER | False | nextval('cat_estados_fisicos_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| descripcion | id | activo |
| --- | --- | --- |
| Nuevo | 1 | True |
| Bueno / Operativo | 2 | True |
| Baja Definitiva | 5 | True |

---

## Tabla: `activos_frio`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('activos_frio_id_seq'::regclass) |
| serie | VARCHAR(50) | True | None |
| descripcion | VARCHAR(100) | True | None |
| modelo_id | INTEGER | True | None |
| estado_id | INTEGER | True | None |
| asignado | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
*Tabla vacía*

---

## Tabla: `inventario_productos`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('inventario_productos_id_seq'::regclass) |
| producto_id | INTEGER | True | None |
| materia_prima_id | INTEGER | True | None |
| ubicacion_id | INTEGER | False | None |
| cantidad_actual | DOUBLE PRECISION | False | None |
| fecha_produccion | DATE | True | None |
| fecha_ingreso_almacen | TIMESTAMP | True | None |
| stock_minimo | DOUBLE PRECISION | True | None |
| stock_maximo | DOUBLE PRECISION | True | None |
| stock_ideal | DOUBLE PRECISION | True | None |
| cantidad_reservada | DOUBLE PRECISION | True | 0.0 |

### Muestra de Datos (Top 3)
| id | producto_id | materia_prima_id | ubicacion_id | cantidad_actual | fecha_produccion | fecha_ingreso_almacen | stock_minimo | stock_maximo | stock_ideal | cantidad_reservada |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | 3 | NULL | 3 | 1000.0 | NULL | 2026-01-21 02:34:27.529543 | 0.0 | 0.0 | 0.0 | 0.0 |
| 9 | 3 | NULL | 2 | 990.0 | NULL | 2026-01-21 02:34:13.512772 | 0.0 | 0.0 | 0.0 | 0.0 |
| 11 | 1 | NULL | 3 | 76.0 | NULL | 2026-01-28 16:47:53.170696 | 0.0 | 0.0 | 0.0 | 0.0 |

---

## Tabla: `cat_ubicaciones`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| descripcion | VARCHAR(100) | False | None |
| id | INTEGER | False | nextval('cat_ubicaciones_id_seq'::regclass) |
| activo | BOOLEAN | True | None |

### Muestra de Datos (Top 3)
| descripcion | id | activo |
| --- | --- | --- |
| Nivel 1 (Piso) | 3 | True |
| Nivel 2 (Rack) | 4 | True |
| Zona de Carga | 5 | True |

---

## Tabla: `usuarios`
### Esquema
| Columna | Tipo | Nulo | Default |
| --- | --- | --- | --- |
| id | INTEGER | False | nextval('usuarios_id_seq'::regclass) |
| nombres | VARCHAR(100) | False | None |
| apellido_paterno | VARCHAR(100) | False | None |
| apellido_materno | VARCHAR(100) | True | None |
| fecha_nacimiento | DATE | True | None |
| estado_civil | VARCHAR(50) | True | None |
| profesion | VARCHAR(100) | True | None |
| curp | VARCHAR(18) | True | None |
| rfc | VARCHAR(13) | True | None |
| calle | VARCHAR(100) | True | None |
| num_exterior | VARCHAR(20) | True | None |
| num_interior | VARCHAR(20) | True | None |
| colonia | VARCHAR(100) | True | None |
| ciudad | VARCHAR(100) | True | None |
| codigo_postal | VARCHAR(10) | True | None |
| estado | VARCHAR(100) | True | None |
| pais | VARCHAR(100) | True | None |
| telefono_casa | VARCHAR(20) | True | None |
| telefono_celular | VARCHAR(20) | True | None |
| email_personal | VARCHAR(100) | True | None |
| contacto_emergencia_nombre | VARCHAR(150) | True | None |
| contacto_emergencia_telefono | VARCHAR(20) | True | None |
| puesto_id | INTEGER | True | None |
| fecha_inicio_empresa | DATE | True | None |
| calificacion_evaluacion | INTEGER | True | None |
| notas_generales | TEXT | True | None |
| email_acceso | VARCHAR(100) | False | None |
| password_hash | VARCHAR(255) | False | None |
| pin_seguridad | VARCHAR(6) | True | None |
| nivel_usuario | INTEGER | True | None |
| activo | BOOLEAN | True | None |
| foto_perfil | VARCHAR(255) | True | None |
| img_ine_frente | VARCHAR(255) | True | None |
| img_ine_reverso | VARCHAR(255) | True | None |
| img_licencia_frente | VARCHAR(255) | True | None |
| img_licencia_reverso | VARCHAR(255) | True | None |
| fecha_validez_licencia | DATE | True | None |

### Muestra de Datos (Top 3)
| id | nombres | apellido_paterno | apellido_materno | fecha_nacimiento | estado_civil | profesion | curp | rfc | calle | num_exterior | num_interior | colonia | ciudad | codigo_postal | estado | pais | telefono_casa | telefono_celular | email_personal | contacto_emergencia_nombre | contacto_emergencia_telefono | puesto_id | fecha_inicio_empresa | calificacion_evaluacion | notas_generales | email_acceso | password_hash | pin_seguridad | nivel_usuario | activo | foto_perfil | img_ine_frente | img_ine_reverso | img_licencia_frente | img_licencia_reverso | fecha_validez_licencia |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Mario Eduardo | Martinez | Juarez | 1986-06-09 | CASADO | Ing. Mecatronico | MAJU900101HGT... | MAJU900101XXX | Av. Hidalgo | 123 | A | Centro | Ac├ímbaro | 38600 | Guanajuato | M├®xico | 4171234567 | 78610300599 | NULL | Maria Reyna Figueroa | 4179999999 | 1 | 2024-01-01 | 5 | NULL | admin@gelmex.com | scrypt:32768:8:1$RuhMxCBRduXLLdJN$dfa56600a6165c487cda79191ae028daaf80b052e0c29cc55b9dc2fceb62df166d38c19b8114f3e7d3e5cf317b6903ed2eb35b2a6eae7bc82801dbd07c2fab11 | 123456 | 5 | True | NULL | NULL | NULL | NULL | NULL | NULL |
| 4 | Emmanuel  | Martinez  | moreno  | 2001-12-07 | CASADO | Lic. Admon | JORO1223333RRR1212 | JORRO122333RR | Cuauht├®moc | 1563 |  | miradores | CD HIDALGO | 61130 | MICHOACAN | M├®xico | 7861548974 | 7861082356 | J.rodriguez@outloock.com | Leticia | 7861225655 | 8 | 1990-08-18 | 5 | primer almacenista muy serio | repartidor01@gelmex.com | scrypt:32768:8:1$aWVCoEf2SStF1ToI$39dbe2fc8d55b6c84dc54d68a2344bda388f9f2e394465ff3810c85e8057af8ff03142c032804e3a3e24a0029b04842cc411f848cf51e289419c4abdc5abe6b5 | 654321 | 2 | True | NULL | NULL | NULL | NULL | NULL | NULL |
| 3 | Brayan  | Martinez  | Moreno | 1999-12-16 | DIVORCIADO | lic marketing | BELO452221 | BELO452221125 | carmen serdan  | 29 |  | LA libertad | CD HIDALGO | 61190 | MICHOACAN | M├®xico | 7861544023 | 78614145 |  | Carolina Herrera | 7861152256 | 5 | 2026-01-28 | 5 | es muy bien repartidor creo que lo ama el vendedor | repartidor@gelmex.com | scrypt:32768:8:1$dummyhash | 123456 | 1 | True | NULL | NULL | NULL | NULL | NULL | NULL |

---

