document.addEventListener('DOMContentLoaded', function () {
    var bodyElement = document.body;
    var toggleDarkModeButton = document.getElementById('cambiarTema');
    var iconoModo = toggleDarkModeButton.querySelector('i');

    // Verifica si el modo oscuro está activado en el almacenamiento local
    var isDarkMode = localStorage.getItem('darkModeEnabled');

    if (isDarkMode === 'true') {
        // Si el modo oscuro está activado, agrega el atributo al body
        bodyElement.setAttribute('data-bs-theme', 'dark');
    }

    // Función para cambiar el icono según el modo oscuro
    function cambiarIconoModoOscuro() {
        if (isDarkMode === 'true') {
            // Si el modo oscuro está activado, cambia el icono a sol
            iconoModo.classList.remove('bi-moon-fill');
            iconoModo.classList.add('bi', 'bi-brightness-high');
        } else {
            // Si el modo oscuro está desactivado, cambia el icono a luna
            iconoModo.classList.remove('bi-brightness-high');
            iconoModo.classList.add('bi', 'bi-moon-fill');
        }
    }

    // Ejecuta la función para cambiar el icono cuando se carga la página
    cambiarIconoModoOscuro();

    toggleDarkModeButton.addEventListener('click', function () {
        // Toggle del modo oscuro
        if (isDarkMode === 'true') {
            // Si el modo oscuro está activado, desactívalo
            localStorage.setItem('darkModeEnabled', 'false');
            bodyElement.removeAttribute('data-bs-theme');
        } else {
            // Si el modo oscuro está desactivado, actívalo
            localStorage.setItem('darkModeEnabled', 'true');
            bodyElement.setAttribute('data-bs-theme', 'dark');
        }
        // Cambia el icono después de cambiar el modo oscuro
        cambiarIconoModoOscuro();
    });

    
    // // Obtén el elemento nav por su clase
    // const nav = document.querySelector('.Inicio__Nav');

    // // Obtén todos los enlaces dentro del nav
    // const enlaces = nav.querySelectorAll('.Inicio__Enlace');

    // // Cambia el color de fondo del nav
    // nav.style.backgroundColor = '#404040'; // Cambia el color de fondo del nav

    // // Itera sobre cada enlace y cambia su color
    // enlaces.forEach(enlace => {
    //     enlace.style.color = 'white'; // Cambia el color de cada enlace
    // });


});
