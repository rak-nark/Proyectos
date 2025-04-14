async function agregarAlCarrito(id) {
    const response = await fetch("/agregar-al-carrito", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ id: id, cantidad: 1 })
    });

    const data = await response.json();
    alert(data.mensaje);
}

document.querySelector(".agregar-carrito").addEventListener("click", function() {
    alert("Producto agregado al carrito");
});

