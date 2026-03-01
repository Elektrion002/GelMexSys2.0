from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
import app.models.catalogs as cat_models
from app.models.infrastructure import Almacen, UbicacionAlmacen, RutaReparto, Vehiculo, ActivoFrio

catalogs_admin_bp = Blueprint('catalogs_admin', __name__, url_prefix='/admin/catalogos')

@catalogs_admin_bp.app_context_processor
def inject_utils():
    return dict(getattr=getattr)

# Mapeo de SLUG -> Clase del Modelo
MODELS_MAP = {
    'plantas': cat_models.CatPlanta,
    'areas': cat_models.CatArea,
    'tipos-almacen': cat_models.CatTipoAlmacen,
    'almacenes': Almacen,
    'ubicaciones-almacen': UbicacionAlmacen,
    'rutas-reparto': RutaReparto,
    'unidades': cat_models.CatUnidadMedida,
    'categorias-producto': cat_models.CatCategoriaProducto,
    'categorias-materia-prima': cat_models.CatCategoriaMateriaPrima,
    'puestos': cat_models.CatPuesto,
    'tipos-vehiculo': cat_models.CatTipoVehiculo,
    'modelos-vehiculo': cat_models.CatModeloVehiculo,
    'estados-fisicos': cat_models.CatEstadoFisico,
    'bancos-cajas': cat_models.CatBancoCaja,
    'conceptos-finanzas': cat_models.CatConceptoFinanzas,
    'tipos-pago': cat_models.CatTipoPagoSolicitado,
    'estados-orden-venta': cat_models.CatEstadoOrdenVenta,
    'estados-plan-produccion': cat_models.CatEstadoPlanProduccion,
    'vehiculos': Vehiculo,
    'activos-frio': ActivoFrio
}

def get_model_info(slug):
    model = MODELS_MAP.get(slug)
    if not model:
        return None, None
    # Nombre legible basado en la clase
    clean_name = model.__name__.replace('Cat', '').replace('Producto', ' de Producto')
    return model, clean_name

@catalogs_admin_bp.route('/')
@login_required
def index():
    if current_user.nivel_usuario < 4:
        flash('⛔ Acceso restringido.', 'danger')
        return redirect(url_for('home.dashboard'))
    
    # Preparamos los items para el dashboard del menú
    catalogs_list = []
    for slug, model in MODELS_MAP.items():
        catalogs_list.append({
            'slug': slug,
            'name': model.__name__.replace('Cat', ''),
            'count': model.query.count()
        })
    
    return render_template('catalogs_admin/menu.html', catalogs=catalogs_list)

@catalogs_admin_bp.route('/<string:slug>')
@login_required
def list_items(slug):
    if current_user.nivel_usuario < 4: return redirect(url_for('home.dashboard'))
    
    model, name = get_model_info(slug)
    if not model:
        flash('❌ Catálogo no encontrado.', 'danger')
        return redirect(url_for('catalogs_admin.index'))
    
    items = model.query.all()
    # Detectamos columnas interesantes
    columns = [c.name for c in model.__table__.columns if c.name not in ['id', 'activo']]
    
    return render_template('catalogs_admin/list.html', 
                           slug=slug, 
                           name=name, 
                           items=items, 
                           columns=columns)

def get_fields_config(model):
    fields = []
    from sqlalchemy import inspect
    mapper = inspect(model)
    
    for col in mapper.columns:
        if col.name in ['id', 'activo']: continue
        
        type_str = str(col.type).upper()
        field_type = 'text'
        options = []
        
        # DETECCIÓN DE LLAVES FORÁNEAS (JERARQUÍA)
        if col.foreign_keys:
            field_type = 'select'
            target_table_name = list(col.foreign_keys)[0].column.table.name
            
            # Buscar el modelo correspondiente en MODELS_MAP por su tabla
            for m_class in MODELS_MAP.values():
                if hasattr(m_class, '__tablename__') and m_class.__tablename__ == target_table_name:
                    raw_options = m_class.query.all()
                    for opt in raw_options:
                        label = getattr(opt, 'descripcion', getattr(opt, 'nombre', getattr(opt, 'codigo', f"ID: {opt.id}")))
                        options.append({'id': opt.id, 'label': label})
                    break
                    
        elif 'INT' in type_str or 'FLOAT' in type_str or 'DECIMAL' in type_str or 'NUMERIC' in type_str:
            field_type = 'number'
        elif 'TEXT' in type_str:
            field_type = 'textarea'
        elif 'BOOL' in type_str:
            field_type = 'checkbox'
            
        fields.append({
            'name': col.name,
            'label': col.name.replace('_', ' ').title(),
            'type': field_type,
            'required': not col.nullable,
            'options': options
        })
    return fields

@catalogs_admin_bp.route('/<string:slug>/nuevo', methods=['GET', 'POST'])
@login_required
def create(slug):
    if current_user.nivel_usuario < 4: return redirect(url_for('home.dashboard'))
    
    model, name = get_model_info(slug)
    if not model: return redirect(url_for('catalogs_admin.index'))
    
    if request.method == 'POST':
        item = model()
        for field in request.form:
            if hasattr(item, field):
                val = request.form.get(field)
                # Conversión de tipos básica
                col_type = str(getattr(model, field).property.columns[0].type).upper()
                if 'BOOL' in col_type:
                    val = True if val in ['1', 'true', 'on'] else False
                elif 'INT' in col_type:
                    val = int(val) if val else None
                elif 'FLOAT' in col_type or 'DECIMAL' in col_type or 'NUMERIC' in col_type:
                    val = float(val) if val else 0.0
                
                setattr(item, field, val)
        
        db.session.add(item)
        db.session.commit()
        flash(f'✅ Registro añadido a {name}.', 'success')
        # Redirigir al explorador si venimos de ahí
        if 'planta_id' in request.args or 'almacen_id' in request.args:
            return redirect(url_for('catalogs_admin.explorer'))
        return redirect(url_for('catalogs_admin.list_items', slug=slug))
    
    fields = get_fields_config(model)
    # Valores por defecto desde URL (para jerarquía)
    defaults = request.args.to_dict()
    
    return render_template('catalogs_admin/form.html', slug=slug, name=name, fields=fields, item=None, defaults=defaults)

@catalogs_admin_bp.route('/<string:slug>/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(slug, id):
    if current_user.nivel_usuario < 4: return redirect(url_for('home.dashboard'))
    
    model, name = get_model_info(slug)
    item = model.query.get_or_404(id)
    
    if request.method == 'POST':
        for field in request.form:
            if hasattr(item, field):
                val = request.form.get(field)
                col_type = str(getattr(model, field).property.columns[0].type).upper()
                if 'BOOL' in col_type:
                    val = True if val in ['1', 'true', 'on'] else False
                elif 'INT' in col_type:
                    val = int(val) if val else None
                elif 'FLOAT' in col_type or 'DECIMAL' in col_type or 'NUMERIC' in col_type:
                    val = float(val) if val else 0.0
                
                setattr(item, field, val)
        
        db.session.commit()
        flash(f'✅ Registro de {name} actualizado.', 'success')
        # Determinar retorno
        referrer = request.referrer or ''
        if '/explorador' in referrer:
            return redirect(url_for('catalogs_admin.explorer'))
        return redirect(url_for('catalogs_admin.list_items', slug=slug))
    
    fields = get_fields_config(model)
    return render_template('catalogs_admin/form.html', slug=slug, name=name, fields=fields, item=item)

@catalogs_admin_bp.route('/explorador')
@login_required
def explorer():
    if current_user.nivel_usuario < 4: return redirect(url_for('home.dashboard'))
    
    plantas = cat_models.CatPlanta.query.all()
    areas = cat_models.CatArea.query.all()
    # Para los modales de creación
    tipos_almacen = cat_models.CatTipoAlmacen.query.all()
    cat_ubicaciones = cat_models.CatUbicacion.query.all()
    
    return render_template('catalogs_admin/infrastructure_tree.html', 
                           plantas=plantas, 
                           areas=areas,
                           tipos_almacen=tipos_almacen,
                           cat_ubicaciones=cat_ubicaciones)
