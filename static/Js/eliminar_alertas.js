// Esperar 3 segundos antes de cerrar automáticamente la alerta de actualización
function cerrarAlertas() {
    setTimeout(function () {
        var alertas = document.querySelectorAll('.alert-dismissible'); // Seleccionar todas las alertas con botón de cierre
        alertas.forEach(function (alerta) {
            alerta.classList.remove('show'); // Ocultar la alerta
            setTimeout(function () {
                alerta.remove(); // Eliminar la alerta del DOM después de la animación
            }, 240); // Esperar 1 segundo después de la animación de desvanecimiento antes de eliminar el elemento
        });
    }, 7000); // Esperar 3 segundos antes de ejecutar la función
}
cerrarAlertas();