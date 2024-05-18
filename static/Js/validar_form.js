document.getElementById("nombre").addEventListener("input", function () {
    var nombre = this.value;
    var patron = /^[A-Za-z\s]+$/; // Expresión regular para permitir solo letras y números
    var mensajeError = document.getElementById("nombre-error");

    if (!patron.test(nombre)) {
        this.value = nombre.replace(/[^A-Za-z\s]/g, ""); // Eliminar caracteres no permitidos
        alert("Por favor, ingresa solo letras y espacios en el nombre.");
    } else {
        mensajeError.textContent = "";
    }
});

function validarCampoNumerico(campoId, mensajeErrorId) {
    var campo = document.getElementById(campoId);
    var valor = campo.value;
    var patron = /^[0-9]+(\.[0-9]+)?$/; // Expresión regular para permitir solo números
    var mensajeError = document.getElementById(mensajeErrorId);

    if (!patron.test(valor)) {
        campo.value = valor.replace(/[^0-9\s]/g, ""); // Eliminar caracteres no permitidos
        mensajeError.textContent=("Por favor, ingresa solo numeros.");
    } else {
        mensajeError.textContent = "";
    }
}

document.getElementById("precio_compra").addEventListener("input", function () {
    validarCampoNumerico("precio_compra", "precio_compra-error");
});

document.getElementById("precio_venta").addEventListener("input", function () {
    validarCampoNumerico("precio_venta", "precio_venta-error");
});
document.getElementById("ganancia").addEventListener("input", function () {
    validarCampoNumerico("ganancia", "precio_venta-error");
});
document.getElementById("existencias").addEventListener("input", function () {
    validarCampoNumerico("existencias", "precio_venta-error");
});
document.getElementById("existencias_deseadas").addEventListener("input", function () {
    validarCampoNumerico("existencias_deseadas", "precio_venta-error");
});


// Agrega más llamadas a validarCampoNumerico para otros campos si es necesario
