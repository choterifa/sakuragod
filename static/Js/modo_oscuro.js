document.addEventListener('DOMContentLoaded', function () {
    var bodyElement = document.body;
    var toggleDarkModeButton = document.getElementById('cambiarTema');
    var iconoModo = toggleDarkModeButton.querySelector('i');

    // Verifica si el modo oscuro está activado en el almacenamiento local
    var isDarkMode = localStorage.getItem('darkModeEnabled') === 'true';

    // Aplica el modo oscuro si está activado
    if (isDarkMode) {
        bodyElement.classList.add('dark-mode');
        bodyElement.setAttribute('data-bs-theme', 'dark');
    }

    // Función para cambiar el icono según el modo oscuro
    function cambiarIconoModoOscuro() {
        if (isDarkMode) {
            // Si el modo oscuro está activado, cambia el icono a sol
            iconoModo.classList.remove('bi-moon-fill');
            iconoModo.classList.add('bi-brightness-high');
        } else {
            // Si el modo oscuro está desactivado, cambia el icono a luna
            iconoModo.classList.remove('bi-brightness-high');
            iconoModo.classList.add('bi-moon-fill');
        }
    }

    // Ejecuta la función para cambiar el icono cuando se carga la página
    cambiarIconoModoOscuro();

    toggleDarkModeButton.addEventListener('click', function () {
        // Toggle del modo oscuro
        isDarkMode = !isDarkMode;
        localStorage.setItem('darkModeEnabled', isDarkMode.toString());

        if (isDarkMode) {
            bodyElement.classList.add('dark-mode');
            bodyElement.setAttribute('data-bs-theme', 'dark');
        } else {
            bodyElement.classList.remove('dark-mode');
            bodyElement.removeAttribute('data-bs-theme');
        }

        // Cambia el icono después de cambiar el modo oscuro
        cambiarIconoModoOscuro();

        // Toggle de las clases de las imágenes
        var imagenesClaras = document.querySelectorAll('.imagen-clara');
        var imagenesOscuras = document.querySelectorAll('.imagen-oscura');

        imagenesClaras.forEach(function (imagen) {
            imagen.classList.toggle('dark-mode');
        });

        imagenesOscuras.forEach(function (imagen) {
            imagen.classList.toggle('dark-mode');
        });
    });
});
