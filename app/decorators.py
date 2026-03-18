from functools import wraps
from flask import abort
from flask_login import current_user

def role_required(roles):
    """
    Decorador para restringir el acceso a rutas basado en el nombre del puesto.
    :param roles: Lista de nombres de puestos permitidos (ej. ['Repartidor', 'Finanzas'])
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            
            # Verificamos si el puesto del usuario está en la lista permitida
            # El objeto current_user.puesto tiene el atributo 'nombre'
            if current_user.puesto.nombre not in roles and current_user.puesto.nombre != 'Super Administrador':
                abort(403) # Prohibido
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator
