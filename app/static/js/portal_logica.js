/**
 * GelMex Portal de Clientes - Lógica de Interfaz
 * Basado en metodología 5S
 */

document.addEventListener('DOMContentLoaded', function() {
    // --- BÚSQUEDA EN CATÁLOGO ---
    const buscador = document.getElementById('catalogSearch');
    if (buscador) {
        buscador.addEventListener('keyup', function() {
            const valor = this.value.toLowerCase().trim();
            const tarjetas = document.querySelectorAll('.product-card');
            const grilla = document.getElementById('catalogGrid');
            const sinResultados = document.getElementById('noResults');
            let contador = 0;

            tarjetas.forEach(tarjeta => {
                const data = tarjeta.dataset.search.toLowerCase();
                if (data.includes(valor)) {
                    tarjeta.classList.remove('d-none');
                    contador++;
                } else {
                    tarjeta.classList.add('d-none');
                }
            });

            if (contador === 0) {
                if (sinResultados) sinResultados.classList.remove('d-none');
                if (grilla) grilla.classList.add('d-none');
            } else {
                if (sinResultados) sinResultados.classList.add('d-none');
                if (grilla) grilla.classList.remove('d-none');
            }
        });
    }

    // --- LÓGICA DE PEDIDOS ---
    const productFilter = document.getElementById('productFilter');
    if (productFilter) {
        productFilter.addEventListener('keyup', function() {
            const val = this.value.toLowerCase().trim();
            const rows = document.querySelectorAll('.item-row');
            rows.forEach(row => {
                const name = row.dataset.name.toLowerCase();
                row.style.display = name.includes(val) ? '' : 'none';
            });
        });
    }
});

/**
 * Cambia la cantidad de un producto en el pedido
 */
function cambiarCantidad(id, delta) {
    const input = document.getElementById('qty_' + id);
    if (!input) return;
    
    let val = parseInt(input.value) + delta;
    if (val < 0) val = 0;
    input.value = val;
    actualizarResumen();
}

/**
 * Actualiza el resumen visual del pedido
 */
function actualizarResumen() {
    const inputs = document.querySelectorAll('.qty-input');
    const resumenContenedor = document.getElementById('selectedItems');
    const badgeTotal = document.getElementById('totalItems');
    let totalArticulos = 0;
    let html = '';

    inputs.forEach(input => {
        let val = parseInt(input.value);
        if (val > 0) {
            totalArticulos += val;
            const fila = input.closest('tr');
            const nombre = fila.dataset.name.split(' SKU')[0];
            html += `
                <div class="d-flex justify-content-between align-items-center mb-2 small">
                    <span class="text-truncate me-2" style="max-width: 150px;">${nombre}</span>
                    <span class="fw-bold">x ${val}</span>
                </div>
            `;
        }
    });

    if (totalArticulos > 0) {
        if (resumenContenedor) resumenContenedor.innerHTML = html;
    } else {
        if (resumenContenedor) {
            resumenContenedor.innerHTML = `
                <div class="text-muted text-center py-4 bg-light rounded-3 mb-3">
                    <i class="fa-solid fa-basket-shopping fa-2x mb-2 opacity-25"></i>
                    <p class="small mb-0">Selecciona cantidades para comenzar</p>
                </div>
            `;
        }
    }
    if (badgeTotal) badgeTotal.innerText = totalArticulos;
}

/**
 * Reinicia la búsqueda del catálogo
 */
function limpiarBusqueda() {
    const buscador = document.getElementById('catalogSearch');
    if (buscador) {
        buscador.value = '';
        const tarjetas = document.querySelectorAll('.product-card');
        tarjetas.forEach(c => c.classList.remove('d-none'));
        
        const grilla = document.getElementById('catalogGrid');
        const sinResultados = document.getElementById('noResults');
        if (sinResultados) sinResultados.classList.add('d-none');
        if (grilla) grilla.classList.remove('d-none');
    }
}
