// Manejar la actualización de cantidad
document.querySelectorAll('.input-cantidad').forEach(input => {
    input.addEventListener('change', function () {
        const productId = this.dataset.productId;
        const newQuantity = this.value;

        fetch('/update_quantity', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_id: productId, quantity: newQuantity })
        }).then(response => response.json())
            .then(data => {
                if (data.success) location.reload();
            });
    });
});

// Manejar eliminación de productos
document.querySelectorAll('.btn-eliminar').forEach(button => {
    button.addEventListener('click', function () {
        const productId = this.dataset.productId;

        fetch('/remove_product', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_id: productId })
        }).then(response => response.json())
            .then(data => {
                if (data.success) location.reload();
            });
    });
});

function formatPrice(price) {
    return price.toLocaleString('es-CO', { style: 'currency', currency: 'COP' }).replace('COP', '').trim();
}

// Formatear precios
document.querySelectorAll('.price').forEach(element => {
    const price = parseInt(element.dataset.price);
    element.textContent = formatPrice(price);
});

// Actualizar el total en el frontend
function updateTotal() {
    let total = 0;
    document.querySelectorAll('.price').forEach(element => {
        const price = parseInt(element.dataset.price);
        const quantity = parseInt(element.closest('tr').querySelector('.input-cantidad').value);
        total += price * quantity;
    });
    const totalFormatted = formatPrice(total);
    document.getElementById('total-amount').textContent = totalFormatted;
}

// Llamar a updateTotal cuando cambie la cantidad
document.querySelectorAll('.input-cantidad').forEach(input => {
    input.addEventListener('change', updateTotal);
});

// Llamar a updateTotal inicialmente
updateTotal();








