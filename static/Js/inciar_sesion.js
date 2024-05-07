// Espera a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function () {
    // Obtén el elemento del contador
    var counterElement = document.getElementById('contador');

    // Inicializa el contador
    var count = 10;

    // Crea una función para actualizar el contador
    function updateCounter() {
        counterElement.textContent = count;
    }

    // Crea una función para animar el contador
    function animateCounter() {
        // Incrementa el contador
        count--;

        // Actualiza el contenido del contador
        updateCounter();

        // Si el contador no ha llegado a 0, programa la próxima actualización
        if (count > 0) {
            setTimeout(animateCounter, 1000); // Ejecuta cada segundo (1000 milisegundos)
        }
    }

    // Comienza la animación del contador
    animateCounter();
});


// Simular clic en el botón automáticamente cuando la página se cargue
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('modal').click();
});

