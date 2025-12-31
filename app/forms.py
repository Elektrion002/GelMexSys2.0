# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, FileField, SubmitField, IntegerField, TextAreaField, PasswordField, DateField
from wtforms.validators import DataRequired, NumberRange, Length, Optional, Email
from flask_wtf.file import FileAllowed

# ==========================================
#  1. FORMULARIO SIMPLE (LEGACY / OPERATIVO)
# ==========================================
class ProductoForm(FlaskForm):
    sku = StringField('SKU / Código', validators=[DataRequired(), Length(max=50)])
    descripcion = StringField('Nombre del Producto', validators=[DataRequired(), Length(max=200)])
    categoria_id = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    unidad_id = SelectField('Unidad de Medida', coerce=int, validators=[DataRequired()])
    precio_costo = DecimalField('Costo Producción ($)', places=2, validators=[NumberRange(min=0)])
    precio_venta = DecimalField('Precio Venta ($)', places=2, validators=[DataRequired(), NumberRange(min=0)])
    stock_minimo = IntegerField('Stock Mínimo (Alerta)', validators=[NumberRange(min=0)], default=10)
    imagen = FileField('Foto del Producto', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imágenes JPG o PNG')])
    submit = SubmitField('Guardar Producto')

# ==========================================
#  2. FORMULARIO DE CLIENTES (CRM)
# ==========================================
class ClienteForm(FlaskForm):
    nombre_negocio = StringField('Nombre del Negocio', validators=[DataRequired(), Length(max=150)])
    rfc = StringField('RFC', validators=[Optional(), Length(max=13)])
    tipo_negocio = StringField('Giro / Tipo', validators=[Optional()])
    nombres_encargado = StringField('Nombre Encargado', validators=[DataRequired()])
    apellidos_encargado = StringField('Apellidos Encargado', validators=[Optional()])
    telefono = StringField('Teléfono Fijo', validators=[Optional()])
    celular = StringField('Celular (WhatsApp)', validators=[Optional()])
    email = StringField('Correo Electrónico', validators=[Optional(), Email(message="Email inválido")])
    calle = StringField('Calle', validators=[DataRequired()])
    num_exterior = StringField('Número Ext.', validators=[DataRequired()])
    colonia = StringField('Colonia', validators=[DataRequired()])
    codigo_postal = StringField('C.P.', validators=[Optional()])
    ciudad = StringField('Ciudad', validators=[DataRequired()])
    estado = StringField('Estado', default='Guanajuato')
    ruta_id = SelectField('Ruta de Reparto', coerce=int, validators=[DataRequired()])
    vendedor_id = SelectField('Vendedor Asignado', coerce=int, validators=[Optional()])
    repartidor_id = SelectField('Repartidor Habitual', coerce=int, validators=[Optional()])
    limite_credito = DecimalField('Límite de Crédito ($)', places=2, default=0.00)
    img_fachada = FileField('Fachada Negocio', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    img_ine_frente = FileField('INE Frente', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    img_ine_reverso = FileField('INE Reverso', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Guardar Cliente')

# ==========================================
#  3. FORMULARIO DE USUARIOS (RH)
# ==========================================
class UsuarioForm(FlaskForm):
    email_acceso = StringField('Correo Institucional (Login)', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[Optional()]) 
    puesto_id = SelectField('Puesto / Rol', coerce=int, validators=[DataRequired()])
    nivel_usuario = SelectField('Nivel de Acceso Sistema', coerce=int, choices=[
        (1, 'Nivel 1 - Operativo Básico (Chofer/Auxiliar)'),
        (2, 'Nivel 2 - Operativo Ventas (Vendedor/Heladero)'),
        (3, 'Nivel 3 - Supervisor (Almacén/Prod)'),
        (4, 'Nivel 4 - Gerencial (Finanzas/Admin)'),
        (5, 'Nivel 5 - Super Admin (Dueño)')
    ], validators=[DataRequired()])
    pin_seguridad = StringField('PIN App Móvil (6 dígitos)', validators=[Optional(), Length(min=4, max=6)])
    nombres = StringField('Nombre(s)', validators=[DataRequired()])
    apellido_paterno = StringField('Apellido Paterno', validators=[DataRequired()])
    apellido_materno = StringField('Apellido Materno', validators=[Optional()])
    fecha_nacimiento = DateField('Fecha Nacimiento', validators=[Optional()])
    estado_civil = SelectField('Estado Civil', choices=[
        ('SOLTERO', 'Soltero/a'), ('CASADO', 'Casado/a'), ('UNION_LIBRE', 'Unión Libre'), ('DIVORCIADO', 'Divorciado/a'), ('VIUDO', 'Viudo/a')
    ], validators=[Optional()])
    profesion = StringField('Profesión / Oficio', validators=[Optional()])
    curp = StringField('CURP', validators=[Optional(), Length(max=18)])
    rfc = StringField('RFC (Personal)', validators=[Optional(), Length(max=13)])
    calle = StringField('Calle', validators=[Optional()])
    num_exterior = StringField('No. Ext', validators=[Optional()])
    num_interior = StringField('No. Int', validators=[Optional()])
    colonia = StringField('Colonia', validators=[Optional()])
    codigo_postal = StringField('C.P.', validators=[Optional()])
    ciudad = StringField('Ciudad', validators=[Optional()])
    estado = StringField('Estado', default='Guanajuato')
    pais = StringField('País', default='México')
    telefono_celular = StringField('Celular Personal', validators=[DataRequired()])
    telefono_casa = StringField('Teléfono Casa', validators=[Optional()])
    email_personal = StringField('Email Personal', validators=[Optional(), Email()])
    contacto_emergencia_nombre = StringField('Nombre Contacto Emergencia', validators=[Optional()])
    contacto_emergencia_telefono = StringField('Teléfono Emergencia', validators=[Optional()])
    fecha_inicio_empresa = DateField('Fecha Ingreso', validators=[Optional()])
    calificacion_evaluacion = SelectField('Evaluación Desempeño', coerce=int, choices=[
        (5, '⭐⭐⭐⭐⭐ Excelente'), (4, '⭐⭐⭐⭐ Bueno'), (3, '⭐⭐⭐ Regular'), (2, '⭐⭐ Malo'), (1, '⭐ Pésimo')
    ], default=5)
    notas_generales = TextAreaField('Notas Generales / Observaciones', validators=[Optional()])
    foto_perfil = FileField('Foto Perfil (Rostro)', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    img_ine_frente = FileField('INE Frente', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    img_ine_reverso = FileField('INE Reverso', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    img_licencia_frente = FileField('Licencia Frente', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    img_licencia_reverso = FileField('Licencia Reverso', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    fecha_validez_licencia = DateField('Vigencia Licencia', validators=[Optional()])
    submit = SubmitField('Guardar Empleado')

# ==========================================
#  4. FORMULARIO MAESTRO DE PRODUCTOS (ADMIN)
# ==========================================
class ProductoAdminForm(FlaskForm):
    # TAB 1: IDENTIDAD
    sku = StringField('SKU / Código Único', validators=[DataRequired(), Length(max=50)])
    descripcion = StringField('Descripción Comercial', validators=[DataRequired(), Length(max=200)])
    categoria_id = SelectField('Categoría / Familia', coerce=int, validators=[DataRequired()])
    imagen_producto = FileField('Foto Marketing', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    activo = SelectField('Estado Catálogo', coerce=int, choices=[(1, 'ACTIVO (Venta y Producción)'), (0, 'DESCONTINUADO (Solo lectura)')], default=1)

    # TAB 2: FINANZAS
    unidad_id = SelectField('Unidad de Medida Base', coerce=int, validators=[DataRequired()])
    precio_costo_actual = DecimalField('Costo Producción ($)', places=2, validators=[NumberRange(min=0)])
    precio_venta_general = DecimalField('Precio Venta Público ($)', places=2, validators=[DataRequired(), NumberRange(min=0)])
    
    # TAB 3: POLÍTICA DE STOCK (PLANEACIÓN)
    stock_minimo = IntegerField('Mínimo (Punto de Reorden)', validators=[NumberRange(min=0)], default=100)
    stock_maximo = IntegerField('Máximo (Capacidad)', validators=[NumberRange(min=0)], default=1000)
    stock_ideal = IntegerField('Stock Ideal (Meta Producción)', validators=[NumberRange(min=0)], default=500)

    # TAB 4: FICHA TÉCNICA (LOGÍSTICA)
    peso_gramos = DecimalField('Peso Unitario (gr)', places=2, default=0)
    caducidad_dias = IntegerField('Vida Útil (Días)', default=0)

    submit = SubmitField('Guardar Configuración Maestra')