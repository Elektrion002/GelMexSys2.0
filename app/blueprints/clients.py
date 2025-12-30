import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.extensions import db
from sqlalchemy import func

# Modelos
from app.models.clients import Cliente, PrecioEspecialCliente
from app.models.products import Producto
from app.models.infrastructure import RutaReparto, ActivoFrio
from app.models.users import Usuario
from app.models.catalogs import CatPuesto, CatTipoDescuento
from app.models.orders import OrdenVenta
from app.forms import ClienteForm

clients_bp = Blueprint('clients', __name__, url_prefix='/clientes')

# --- UTILIDAD: GUARDAR IMÁGENES ---
def guardar_imagen(file, prefix):
    if not file or not file.filename: return None
    filename = secure_filename(f"{prefix}_{file.filename}")
    db_path = f"uploads/clientes/{filename}"
    save_path = os.path.join(current_app.root_path, 'static', 'uploads', 'clientes')
    os.makedirs(save_path, exist_ok=True)
    file.save(os.path.join(save_path, filename))
    return db_path

# --- LISTADO ---
@clients_bp.route('/')
@login_required
def index():
    clientes = Cliente.query.filter_by(activo=True).order_by(Cliente.nombre_negocio).all()
    return render_template('clients/index.html', clientes=clientes)

# --- CREAR ---
@clients_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def create():
    form = ClienteForm()
    cargar_selectores_inteligentes(form)

    if form.validate_on_submit():
        # En CREAR no usamos populate_obj para tener control total desde cero
        nuevo_cliente = Cliente(
            nombre_negocio=form.nombre_negocio.data,
            rfc=form.rfc.data,
            tipo_negocio=form.tipo_negocio.data,
            nombres_encargado=form.nombres_encargado.data,
            apellidos_encargado=form.apellidos_encargado.data,
            telefono=form.telefono.data,
            celular=form.celular.data,
            email=form.email.data,
            calle=form.calle.data,
            num_exterior=form.num_exterior.data,
            colonia=form.colonia.data,
            codigo_postal=form.codigo_postal.data,
            ciudad=form.ciudad.data,
            estado=form.estado.data,
            ruta_id=form.ruta_id.data,
            vendedor_habitual_id=form.vendedor_id.data if form.vendedor_id.data > 0 else None,
            repartidor_habitual_id=form.repartidor_id.data if form.repartidor_id.data > 0 else None,
            limite_credito=form.limite_credito.data,
            saldo_actual=0.0,
            activo=True
        )

        # Guardado de imágenes inicial
        if form.img_fachada.data: 
            nuevo_cliente.img_fachada = guardar_imagen(form.img_fachada.data, 'fac')
        if form.img_ine_frente.data:
            nuevo_cliente.img_ine_frente = guardar_imagen(form.img_ine_frente.data, 'inef')
        if form.img_ine_reverso.data:
            nuevo_cliente.img_ine_reverso = guardar_imagen(form.img_ine_reverso.data, 'iner')

        db.session.add(nuevo_cliente)
        db.session.commit()
        
        flash('✅ Cliente registrado. Ahora configura sus precios especiales.', 'success')
        return redirect(url_for('clients.edit', id=nuevo_cliente.id))

    return render_template('clients/form.html', form=form, titulo="Nuevo Cliente", cliente=None)

# --- EDITAR (AQUI ESTABA EL ERROR) ---
@clients_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    cliente = Cliente.query.get_or_404(id)
    form = ClienteForm(obj=cliente)
    cargar_selectores_inteligentes(form)
    
    if request.method == 'GET':
        form.vendedor_id.data = cliente.vendedor_habitual_id or 0
        form.repartidor_id.data = cliente.repartidor_habitual_id or 0

    if form.validate_on_submit():
        # 1. Rescatamos las rutas actuales ANTES de que populate_obj las borre
        ruta_fachada_actual = cliente.img_fachada
        ruta_ine_f_actual = cliente.img_ine_frente
        ruta_ine_r_actual = cliente.img_ine_reverso

        # 2. Actualizamos los campos de texto
        form.populate_obj(cliente) 
        
        # 3. Lógica de Rescate de Imágenes:
        # Si el usuario subió archivo nuevo (data y filename existen) -> Guardamos nueva ruta
        # Si NO subió archivo (FileStorage vacío) -> Restauramos la ruta vieja

        # Fachada
        if form.img_fachada.data and form.img_fachada.data.filename:
            cliente.img_fachada = guardar_imagen(form.img_fachada.data, f'fac_{id}')
        else:
            cliente.img_fachada = ruta_fachada_actual

        # INE Frente
        if form.img_ine_frente.data and form.img_ine_frente.data.filename:
            cliente.img_ine_frente = guardar_imagen(form.img_ine_frente.data, f'inef_{id}')
        else:
            cliente.img_ine_frente = ruta_ine_f_actual

        # INE Reverso
        if form.img_ine_reverso.data and form.img_ine_reverso.data.filename:
            cliente.img_ine_reverso = guardar_imagen(form.img_ine_reverso.data, f'iner_{id}')
        else:
            cliente.img_ine_reverso = ruta_ine_r_actual

        # 4. Ajuste de IDs manuales
        cliente.vendedor_habitual_id = form.vendedor_id.data if form.vendedor_id.data > 0 else None
        cliente.repartidor_habitual_id = form.repartidor_id.data if form.repartidor_id.data > 0 else None

        db.session.commit()
        flash('✅ Datos actualizados.', 'success')
        return redirect(url_for('clients.edit', id=id))

    # Cálculo de Deuda Real
    ventas_en_curso = db.session.query(func.sum(OrdenVenta.total_venta))\
        .filter(OrdenVenta.cliente_id == id)\
        .filter(OrdenVenta.estado.in_(['CONFIRMADA', 'EN_PRODUCCION', 'EMPACADO', 'EN_RUTA']))\
        .scalar() or 0.0
    
    riesgo_total = float(cliente.saldo_actual) + float(ventas_en_curso)

    productos = Producto.query.filter_by(activo=True).order_by(Producto.descripcion).all()
    tipos_descuento = CatTipoDescuento.query.all()

    return render_template('clients/form.html', 
                           form=form, 
                           titulo="Editar Cliente", 
                           cliente=cliente,
                           productos=productos,
                           tipos_descuento=tipos_descuento,
                           riesgo_total=riesgo_total)

# --- BAJA LÓGICA ---
@clients_bp.route('/eliminar/<int:id>')
@login_required
def delete(id):
    cliente = Cliente.query.get_or_404(id)
    if cliente.saldo_actual > 1:
        flash(f'⚠️ No se puede dar de baja. Tiene deuda de ${cliente.saldo_actual}.', 'warning')
        return redirect(url_for('clients.index'))

    cliente.activo = False
    db.session.commit()
    flash(f'🗑️ Cliente "{cliente.nombre_negocio}" dado de baja.', 'info')
    return redirect(url_for('clients.index'))

# --- PRECIOS ESPECIALES ---
@clients_bp.route('/add-precio', methods=['POST'])
@login_required
def add_precio():
    try:
        nuevo = PrecioEspecialCliente(
            cliente_id=int(request.form.get('cliente_id')),
            producto_id=int(request.form.get('producto_id')),
            tipo_descuento_id=int(request.form.get('tipo_descuento_id')),
            valor_descuento=float(request.form.get('valor'))
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('✅ Precio especial agregado.', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('clients.edit', id=request.form.get('cliente_id')))

@clients_bp.route('/del-precio/<int:id>')
@login_required
def del_precio(id):
    precio = PrecioEspecialCliente.query.get_or_404(id)
    cid = precio.cliente_id
    db.session.delete(precio)
    db.session.commit()
    flash('Precio eliminado.', 'info')
    return redirect(url_for('clients.edit', id=cid))

# --- HELPERS ---
def cargar_selectores_inteligentes(form):
    form.ruta_id.choices = [(r.id, r.descripcion) for r in RutaReparto.query.all()]
    
    puestos_vend = CatPuesto.query.filter(CatPuesto.nombre.ilike('%Vendedor%')).all()
    ids_vend = [p.id for p in puestos_vend]
    if ids_vend:
        vendedores = Usuario.query.filter(Usuario.puesto_id.in_(ids_vend), Usuario.activo==True).all()
    else:
        vendedores = []
    form.vendedor_id.choices = [(0, '-- Sin Asignar --')] + [(u.id, f"{u.nombres} {u.apellido_paterno}") for u in vendedores]

    puestos_rep = CatPuesto.query.filter(CatPuesto.nombre.ilike('%Repartidor%')).all()
    ids_rep = [p.id for p in puestos_rep]
    if ids_rep:
        repartidores = Usuario.query.filter(Usuario.puesto_id.in_(ids_rep), Usuario.activo==True).all()
    else:
        repartidores = []
    form.repartidor_id.choices = [(0, '-- Sin Asignar --')] + [(u.id, f"{u.nombres} {u.apellido_paterno}") for u in repartidores]