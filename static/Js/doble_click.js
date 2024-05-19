// Obtenemos todos los elementos con la clase "doble_click"
var elementosDobleClick = document.querySelectorAll('.doble_click');

// Iteramos sobre cada elemento y añadimos el evento de doble click
elementosDobleClick.forEach(function (elemento) {
    elemento.addEventListener('dblclick', function () {
        // Buscamos el botón de editar dentro de este elemento y hacemos clic en él
        elemento.querySelector('.btn__editar').click();
    });
});
