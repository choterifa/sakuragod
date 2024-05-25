document.addEventListener('DOMContentLoaded', function () {
    var bodyElement = document.body;
    var htmlElement = document.documentElement;
    var activarModo = document.getElementById('activar_modo');

    // Función para activar el modo oscuro
    function activarModoOscuro() {
        bodyElement.classList.add('dark-mode');
        htmlElement.setAttribute('data-bs-theme', 'dark'); // Agregar el atributo al elemento <html>
        localStorage.setItem('darkModeEnabled', 'true');
        activarModo.textContent = "Modo día"; // Cambiar el texto del elemento a "Modo día"
    }

    // Función para desactivar el modo oscuro
    function desactivarModoOscuro() {
        bodyElement.classList.remove('dark-mode');
        htmlElement.removeAttribute('data-bs-theme'); // Eliminar el atributo del elemento <html>
        localStorage.setItem('darkModeEnabled', 'false');
        activarModo.textContent = "Modo oscuro"; // Cambiar el texto del elemento a "Modo oscuro"
    }

    // Evento clic en el elemento "activar_modo"
    activarModo.addEventListener('click', function () {
        var isDarkMode = localStorage.getItem('darkModeEnabled') === 'true';
        if (isDarkMode) {
            desactivarModoOscuro();
        } else {
            activarModoOscuro();
        }
    });

    // Verificar si el modo oscuro está activado al cargar la página
    var isDarkMode = localStorage.getItem('darkModeEnabled') === 'true';
    if (isDarkMode) {
        activarModoOscuro();
    }
});
