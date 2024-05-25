document.addEventListener('DOMContentLoaded', function () {
    var bodyElement = document.body;
    var themeToggleButton = document.querySelector('.dropdown-toggle');
    var themeButtons = document.querySelectorAll('[data-bs-theme-value]');
    var iconoActivo = themeToggleButton.querySelector('.theme-icon-active');
    var isDarkMode = localStorage.getItem('darkModeEnabled') === 'true';

    // Aplica el modo oscuro si está activado
    if (isDarkMode) {
        bodyElement.classList.add('dark-mode');
        bodyElement.setAttribute('data-bs-theme', 'dark');
    }

    function setActiveIcon(theme) {
        var iconClass = {
            'light': 'bi-sun-fill',
            'dark': 'bi-moon-stars-fill',
            'auto': 'bi-circle-half'
        }[theme];
        iconoActivo.className = `bi ${iconClass} theme-icon-active my-1`;
    }

    function updateThemeSelection(theme) {
        themeButtons.forEach(function (button) {
            var buttonTheme = button.getAttribute('data-bs-theme-value');
            var checkIcon = button.querySelector('i:last-child');
            if (buttonTheme === theme) {
                button.classList.add('active');
                checkIcon.classList.remove('d-none');
            } else {
                button.classList.remove('active');
                checkIcon.classList.add('d-none');
            }
        });
    }

    // Ejecuta la función para cambiar el icono cuando se carga la página
    setActiveIcon(isDarkMode ? 'dark' : 'light');
    updateThemeSelection(isDarkMode ? 'dark' : 'light');

    themeButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            var theme = this.getAttribute('data-bs-theme-value');
            isDarkMode = theme === 'dark';
            localStorage.setItem('darkModeEnabled', isDarkMode.toString());

            if (isDarkMode) {
                bodyElement.classList.add('dark-mode');
                bodyElement.setAttribute('data-bs-theme', 'dark');
            } else if (theme === 'light') {
                bodyElement.classList.remove('dark-mode');
                bodyElement.setAttribute('data-bs-theme', 'light');
            } else {
                bodyElement.classList.remove('dark-mode');
                bodyElement.removeAttribute('data-bs-theme');
            }

            setActiveIcon(theme);
            updateThemeSelection(theme);

            var imagenesClaras = document.querySelectorAll('.imagen-clara');
            var imagenesOscuras = document.querySelectorAll('.imagen-oscura');

            imagenesClaras.forEach(function (imagen) {
                imagen.classList.toggle('dark-mode', isDarkMode);
            });

            imagenesOscuras.forEach(function (imagen) {
                imagen.classList.toggle('dark-mode', isDarkMode);
            });

            var ubicacionImagen = document.querySelector('.Ubicacion__Imagen__Contenedor img');
            if (ubicacionImagen) {
                if (isDarkMode) {
                    ubicacionImagen.src = "../../static/imagenes/Logo/Letra negra.jpg";
                } else {
                    ubicacionImagen.src = "../../static/imagenes/Logo/Letra blanca.png";
                }
            }
        });
    });

    // Asegura que la página se muestre correctamente
    document.body.style.opacity = '1';
});
