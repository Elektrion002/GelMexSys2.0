# app/blueprints/home.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user # <--- 1. IMPORTAR ESTO

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@home_bp.route('/dashboard')
@login_required # <--- 2. ESTE ES EL CANDADO (Si no hay login, no pasa)
def dashboard():
    # Pasamos el usuario actual a la plantilla (aunque Flask-Login ya lo hace globalmente)
    return render_template('home/index.html', user=current_user)