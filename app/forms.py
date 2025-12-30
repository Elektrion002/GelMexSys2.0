# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, FileField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length, Optional, Email
from flask_wtf.file import FileAllowed

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

# --- NUEVO FORMULARIO DE CLIENTES ---
class ClienteForm(FlaskForm):
    # Pestaña 1: Identidad y Contacto
    nombre_negocio = StringField('Nombre del Negocio', validators=[DataRequired(), Length(max=150)])
    rfc = StringField('RFC', validators=[Optional(), Length(max=13)])
    tipo_negocio = StringField('Giro / Tipo', validators=[Optional()])
    
    nombres_encargado = StringField('Nombre Encargado', validators=[DataRequired()])
    apellidos_encargado = StringField('Apellidos Encargado', validators=[Optional()])
    
    telefono = StringField('Teléfono Fijo', validators=[Optional()])
    celular = StringField('Celular (WhatsApp)', validators=[Optional()])
    email = StringField('Correo Electrónico', validators=[Optional(), Email(message="Email inválido")])

    # Pestaña 2: Dirección
    calle = StringField('Calle', validators=[DataRequired()])
    num_exterior = StringField('Número Ext.', validators=[DataRequired()])
    colonia = StringField('Colonia', validators=[DataRequired()])
    codigo_postal = StringField('C.P.', validators=[Optional()])
    ciudad = StringField('Ciudad', validators=[DataRequired()])
    estado = StringField('Estado', default='Guanajuato')

    # Pestaña 3: Operación
    ruta_id = SelectField('Ruta de Reparto', coerce=int, validators=[DataRequired()])
    vendedor_id = SelectField('Vendedor Asignado', coerce=int, validators=[Optional()])
    repartidor_id = SelectField('Repartidor Habitual', coerce=int, validators=[Optional()])

    # Pestaña 4: Finanzas
    limite_credito = DecimalField('Límite de Crédito ($)', places=2, default=0.00)
    
    # Pestaña 5: Documentos
    img_fachada = FileField('Fachada Negocio', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    img_ine_frente = FileField('INE Frente', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    img_ine_reverso = FileField('INE Reverso', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    submit = SubmitField('Guardar Cliente')