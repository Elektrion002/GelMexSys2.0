# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, FileField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length
from flask_wtf.file import FileAllowed

class ProductoForm(FlaskForm):
    sku = StringField('SKU / Código', validators=[DataRequired(), Length(max=50)])
    descripcion = StringField('Nombre del Producto', validators=[DataRequired(), Length(max=200)])
    
    # Los SelectField (Combos) se llenan dinámicamente en el controlador
    categoria_id = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    unidad_id = SelectField('Unidad de Medida', coerce=int, validators=[DataRequired()])
    
    precio_costo = DecimalField('Costo Producción ($)', places=2, validators=[NumberRange(min=0)])
    precio_venta = DecimalField('Precio Venta ($)', places=2, validators=[DataRequired(), NumberRange(min=0)])
    
    stock_minimo = IntegerField('Stock Mínimo (Alerta)', validators=[NumberRange(min=0)], default=10)
    
    imagen = FileField('Foto del Producto', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imágenes JPG o PNG')
    ])
    
    submit = SubmitField('Guardar Producto')