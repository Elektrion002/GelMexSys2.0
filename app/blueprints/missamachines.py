from app.extensions import db
from app.models.missamachines import MissaVenta, MissaCliente
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime

missamachines_bp = Blueprint('missamachines', __name__, 
                              url_prefix='/missamachines',
                              template_folder='../templates/missamachines')

@missamachines_bp.route('/')
def dashboard():
    """Panel principal de Missa Machines."""
    ventas = MissaVenta.query.order_by(MissaVenta.fecha.desc()).all()
    
    # Calculate KPIs
    ingresos = sum(v.anticipo for v in ventas)  # As a basic KPI example
    equipos = len(ventas)
    clientes = MissaCliente.query.count()
    
    return render_template('index.html', ventas=ventas, ingresos=ingresos, equipos=equipos, total_clientes=clientes)

@missamachines_bp.route('/nueva_venta', methods=['GET', 'POST'])
def nueva_venta():
    """Formulario para crear una nueva nota de venta/cotización."""
    if request.method == 'POST':
        # Retrieve form data
        nuevo_cliente = MissaCliente(
            nombre_completo=request.form.get('cliente_nombre'),
            telefono=request.form.get('cliente_telefono'),
            direccion=request.form.get('cliente_direccion'),
            sector=request.form.get('cliente_sector'),
            email=request.form.get('cliente_email')
        )
        db.session.add(nuevo_cliente)
        db.session.flush() # To get the newly created client ID
        
        # Dynamic Items
        cantidades = request.form.getlist('item_cantidad[]')
        descripciones = request.form.getlist('item_descripcion[]')
        subtotales_arr = request.form.getlist('item_subtotal[]')
        anticipos_arr = request.form.getlist('item_anticipo[]')

        grand_subtotal = 0.0
        grand_anticipo = 0.0
        grand_resta = 0.0

        nueva_venta = MissaVenta(
            cliente_id=nuevo_cliente.id,
            vendedor=request.form.get('vendedor'),
            tipo_documento=request.form.get('tipo_documento', 'venta')
        )
        db.session.add(nueva_venta)
        db.session.flush()

        from app.models.missamachines import MissaVentaDetalle
        for i in range(len(cantidades)):
            # Fallbacks in case empty
            if not descripciones[i].strip():
                continue
            
            c = int(cantidades[i] or 1)
            desc = descripciones[i]
            s = float(subtotales_arr[i] or 0)
            a = float(anticipos_arr[i] or 0)
            r = s - a

            grand_subtotal += s
            grand_anticipo += a
            grand_resta += r

            detalle = MissaVentaDetalle(
                venta_id=nueva_venta.id,
                cantidad=c,
                descripcion=desc,
                subtotal=s,
                anticipo=a,
                resta=r
            )
            db.session.add(detalle)

        imp = float(request.form.get('impuestos_val', 0) or 0)
        nueva_venta.subtotal = grand_subtotal
        nueva_venta.impuestos = imp
        nueva_venta.anticipo = grand_anticipo
        nueva_venta.resta = (grand_subtotal + imp) - grand_anticipo
        nueva_venta.total = grand_subtotal + imp
        db.session.commit()
        
        flash('Nota de venta creada correctamente', 'success')
        return redirect(url_for('missamachines.ver_venta', venta_id=nueva_venta.id))
        
    return render_template('sale_form.html')

@missamachines_bp.route('/venta/<int:venta_id>')
def ver_venta(venta_id):
    """Vista detallada de la nota de venta (apta para imprimir)"""
    venta = MissaVenta.query.get_or_404(venta_id)
    return render_template('sale_print.html', venta=venta)

@missamachines_bp.route('/clientes')
def clients():
    """Directorio de clientes"""
    clientes = MissaCliente.query.all()
    return render_template('clients.html', clientes=clientes)

@missamachines_bp.route('/editar_cliente/<int:cliente_id>', methods=['GET', 'POST'])
def editar_cliente(cliente_id):
    """Edición de información de cliente."""
    cliente = MissaCliente.query.get_or_404(cliente_id)
    if request.method == 'POST':
        cliente.nombre_completo = request.form.get('nombre_completo')
        cliente.telefono = request.form.get('telefono')
        cliente.direccion = request.form.get('direccion')
        cliente.sector = request.form.get('sector')
        db.session.commit()
        flash('Cliente actualizado correctamente', 'success')
        return redirect(url_for('missamachines.clients'))
    return render_template('edit_client.html', cliente=cliente)

@missamachines_bp.route('/convertir_venta/<int:venta_id>', methods=['POST'])
def convertir_venta(venta_id):
    """Convierte una cotización en una nota de venta oficial."""
    venta = MissaVenta.query.get_or_404(venta_id)
    if venta.tipo_documento == 'cotizacion':
        venta.tipo_documento = 'venta'
        from datetime import datetime
        venta.fecha = datetime.utcnow()
        db.session.commit()
        flash('La cotización fue convertida a Venta Oficial exitosamente.', 'success')
    return redirect(url_for('missamachines.dashboard'))

@missamachines_bp.route('/docs')
def docs():
    """Documentacion Operativa y Tecnica"""
    return render_template('docs.html')

