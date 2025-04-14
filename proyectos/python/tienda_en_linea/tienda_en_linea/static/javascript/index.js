// Archivo: static/scripts/index.js
document.addEventListener("DOMContentLoaded", () => {
    const productoCards = document.querySelectorAll(".producto-card");

    productoCards.forEach(card => {
        card.addEventListener("mouseenter", () => {
            card.style.transform = "translateY(-10px)";
        });
        card.addEventListener("mouseleave", () => {
            card.style.transform = "translateY(0)";
        });
    });
});
