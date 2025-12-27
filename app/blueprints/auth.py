# app/blueprints/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.users import Usuario

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Si ya está logueado, lo mandamos directo al dashboard
    if current_user.is_authenticated:
        return redirect(url_for('home.dashboard'))

    if request.method == 'POST':
        email_form = request.form.get('email')
        password_form = request.form.get('password')
        
        # 1. Buscar usuario en DB
        usuario = Usuario.query.filter_by(email_acceso=email_form).first()
        
        # 2. Validar que exista y que la contraseña sea correcta
        if usuario and usuario.check_password(password_form):
            login_user(usuario) # Crear la sesión (Cookie)
            flash(f'¡Bienvenido de nuevo, {usuario.nombres}!', 'success')
            
            # Redirigir a donde quería ir o al dashboard
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home.dashboard'))
        else:
            flash('Correo o contraseña incorrectos. Intenta de nuevo.', 'danger')
        
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required # Solo si estás logueado puedes salir
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('auth.login'))