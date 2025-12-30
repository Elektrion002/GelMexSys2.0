import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from app.extensions import db

# Modelos
from app.models.users import Usuario
from app.models.catalogs import CatPuesto
from app.forms import UsuarioForm

users_bp = Blueprint('users', __name__, url_prefix='/usuarios')

# --- UTILIDAD: GUARDAR IMÁGENES ---
def guardar_imagen_user(file, prefix):
    # Validación estricta: Si no hay archivo o no tiene nombre, retorna None
    if not file or not file.filename: return None
    
    filename = secure_filename(f"{prefix}_{file.filename}")
    db_path = f"uploads/usuarios/{filename}"
    save_path = os.path.join(current_app.root_path, 'static', 'uploads', 'usuarios')
    os.makedirs(save_path, exist_ok=True)
    file.save(os.path.join(save_path, filename))
    return db_path

# --- LISTADO ---
@users_bp.route('/')
@login_required
def index():
    if current_user.nivel_usuario < 4:
        flash('⛔ Acceso denegado. Se requiere nivel Gerencial.', 'danger')
        return redirect(url_for('home.dashboard'))

    usuarios = Usuario.query.order_by(Usuario.activo.desc(), Usuario.nombres).all()
    return render_template('users/index.html', usuarios=usuarios)

# --- CREAR (CORREGIDO ERROR FILESTORAGE) ---
@users_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.nivel_usuario < 4: return redirect(url_for('home.dashboard'))

    form = UsuarioForm()
    form.puesto_id.choices = [(p.id, p.nombre) for p in CatPuesto.query.filter_by(activo=True).all()]

    if form.validate_on_submit():
        if not form.password.data:
            flash('⚠️ La contraseña es obligatoria para nuevos usuarios.', 'warning')
            return render_template('users/form.html', form=form, title="Nuevo Empleado")

        nuevo_user = Usuario()
        
        # 1. Llenamos datos automáticos (Esto ensucia los campos de imagen con FileStorage)
        form.populate_obj(nuevo_user)
        
        # 2. LIMPIEZA INMEDIATA DE IMÁGENES (Solución del error)
        # Llamamos a guardar_imagen_user siempre. Si no hay archivo, devuelve None y limpia el FileStorage.
        nuevo_user.foto_perfil = guardar_imagen_user(form.foto_perfil.data, 'avatar')
        nuevo_user.img_ine_frente = guardar_imagen_user(form.img_ine_frente.data, 'ine_f')
        nuevo_user.img_ine_reverso = guardar_imagen_user(form.img_ine_reverso.data, 'ine_r')
        nuevo_user.img_licencia_frente = guardar_imagen_user(form.img_licencia_frente.data, 'lic_f')
        nuevo_user.img_licencia_reverso = guardar_imagen_user(form.img_licencia_reverso.data, 'lic_r')

        # 3. Configuración Manual
        nuevo_user.password_hash = generate_password_hash(form.password.data)
        nuevo_user.activo = True

        try:
            db.session.add(nuevo_user)
            db.session.commit()
            flash('✅ Empleado registrado correctamente.', 'success')
            return redirect(url_for('users.index'))
        except Exception as e:
            db.session.rollback()
            print(f"ERROR DB: {e}")
            flash(f'Error al guardar en BD: {str(e)}', 'danger')
    
    # Debug visual
    if request.method == 'POST':
        print("❌ ERROR FORMULARIO:", form.errors)

    return render_template('users/form.html', form=form, title="Nuevo Empleado")

# --- EDITAR (CORREGIDO ERROR FILESTORAGE) ---
@users_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.nivel_usuario < 4: return redirect(url_for('home.dashboard'))

    usuario = Usuario.query.get_or_404(id)
    form = UsuarioForm(obj=usuario)
    form.puesto_id.choices = [(p.id, p.nombre) for p in CatPuesto.query.filter_by(activo=True).all()]

    if form.validate_on_submit():
        # 1. Guardar rutas actuales (backup)
        rutas_old = {
            'foto_perfil': usuario.foto_perfil,
            'img_ine_frente': usuario.img_ine_frente,
            'img_ine_reverso': usuario.img_ine_reverso,
            'img_licencia_frente': usuario.img_licencia_frente,
            'img_licencia_reverso': usuario.img_licencia_reverso
        }

        # 2. Actualizar textos (Esto ensucia las imágenes con FileStorage)
        form.populate_obj(usuario)

        # 3. Lógica de Contraseña
        if form.password.data:
            usuario.password_hash = generate_password_hash(form.password.data)
            flash('🔐 Contraseña actualizada.', 'info')
        
        # 4. LIMPIEZA Y RESTAURACIÓN DE IMÁGENES
        # Intentamos guardar la nueva. Si devuelve None (no subió nada), restauramos la vieja.
        usuario.foto_perfil = guardar_imagen_user(form.foto_perfil.data, f'avatar_{id}') or rutas_old['foto_perfil']
        usuario.img_ine_frente = guardar_imagen_user(form.img_ine_frente.data, f'ine_f_{id}') or rutas_old['img_ine_frente']
        usuario.img_ine_reverso = guardar_imagen_user(form.img_ine_reverso.data, f'ine_r_{id}') or rutas_old['img_ine_reverso']
        usuario.img_licencia_frente = guardar_imagen_user(form.img_licencia_frente.data, f'lic_f_{id}') or rutas_old['img_licencia_frente']
        usuario.img_licencia_reverso = guardar_imagen_user(form.img_licencia_reverso.data, f'lic_r_{id}') or rutas_old['img_licencia_reverso']

        try:
            db.session.commit()
            flash('✅ Datos actualizados correctamente.', 'success')
            return redirect(url_for('users.index'))
        except Exception as e:
            db.session.rollback()
            print(f"ERROR DB EDIT: {e}")
            flash(f'Error al actualizar: {str(e)}', 'danger')
    
    else:
        if request.method == 'POST':
            print("\n❌ ERROR DE VALIDACIÓN:", form.errors)
            flash('⚠️ Error en el formulario. Revisa los campos en rojo.', 'danger')

    return render_template('users/form.html', form=form, title="Editar Empleado", usuario=usuario)

@users_bp.route('/toggle-status/<int:id>')
@login_required
def toggle_status(id):
    if current_user.nivel_usuario < 4: return redirect(url_for('home.dashboard'))
    
    if id == current_user.id:
        flash('⛔ No puedes desactivar tu propia cuenta.', 'danger')
        return redirect(url_for('users.index'))

    usuario = Usuario.query.get_or_404(id)
    usuario.activo = not usuario.activo
    db.session.commit()
    
    estado = "Activado" if usuario.activo else "Desactivado"
    flash(f'🔄 Usuario {usuario.nombres} {estado}.', 'info')
    return redirect(url_for('users.index'))