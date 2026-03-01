from flask import Blueprint, render_template, session

help_center_bp = Blueprint('help_center', __name__, url_prefix='/ayuda')

@help_center_bp.route('/')
def index():
    # Detectar si es usuario administrativo o cliente para personalizar la vista
    es_cliente = 'customer_id' in session
    return render_template('help_center/index.html', es_cliente=es_cliente)

@help_center_bp.route('/cliente')
def client_manual():
    return render_template('help_center/manual_cliente.html')

@help_center_bp.route('/administracion')
def admin_manual():
    return render_template('help_center/manual_admin.html')
