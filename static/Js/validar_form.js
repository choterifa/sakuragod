// document.getElementById("nombre").addEventListener("input", function () {
//     var nombre = this.value;
//     var patron = /^[a-zA-ZáéíóúÁÉÍÓÚüÜ\s]+$/; // Expresión regular para permitir solo letras y números
//     var mensajeError = document.getElementById("nombre-error");

//     if (!patron.test(nombre)) {
//         this.value = nombre.replace(/^[a-zA-ZáéíóúÁÉÍÓÚüÜ\s]+$/g, ""); // Eliminar caracteres no permitidos
//         alert("Por favor, Ingresa solo letras sin acentos y espacios en el nombre.");
//     } else {
//         mensajeError.textContent = "";
//     }
// });

// function validarCampoNumerico(campoId, mensajeErrorId) {
//     var campo = document.getElementById(campoId);
//     var valor = campo.value;
//     var patron = /^[0-9]+(\.[0-9]+)?$/; // Expresión regular para permitir solo números
//     var mensajeError = document.getElementById(mensajeErrorId);

//     if (!patron.test(valor)) {
//         campo.value = valor.replace(/[^0-9\s]/g, ""); // Eliminar caracteres no permitidos
//         mensajeError.textContent = ("Por favor, ingresa solo numeros.");
//     } else {
//         mensajeError.textContent = "";
//     }
// }

document.getElementById('nombre').addEventListener('input', function (e) {
    var value = e.target.value;
    // Permitir solo letras con acentos y espacios
    var pattern = /^[a-zA-ZáéíóúÁÉÍÓÚüÜ\s]*$/;
    if (!pattern.test(value)) {
        e.target.value = value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚüÜ\s]/g, '');
    }
});


function validateInput(event, maxLength, minValue, maxValue) {
    var value = event.target.value;
    // Limitar a maxLength caracteres
    if (value.length > maxLength) {
        event.target.value = value.slice(0, maxLength);
    }

    // Asegurar el rango de valores
    var numericValue = parseFloat(event.target.value);
    if (numericValue < minValue) {
        event.target.value = minValue;
    } else if (numericValue > maxValue) {
        event.target.value = maxValue;
    }
}

//Asegurar al rango establecido

document.getElementById('precio_compra').addEventListener('input', function (e) {
    validateInput(e, 30, 0, 1000);
});

document.getElementById('precio_venta').addEventListener('input', function (e) {
    validateInput(e, 30, 0, 1000);
});

document.getElementById('ganancia').addEventListener('input', function (e) {
    validateInput(e, 30, 0, 1000);
});

document.getElementById('existencias').addEventListener('input', function (e) {
    validateInput(e, 30, 0, 500);
});

document.getElementById('existencias_deseadas').addEventListener('input', function (e) {
    validateInput(e, 30, 0, 500);
});


// document.getElementById("precio_compra").addEventListener("input", function () {
//     validarCampoNumerico("precio_compra", "precio_compra-error");
// });

// document.getElementById("precio_venta").addEventListener("input", function () {
//     validarCampoNumerico("precio_venta", "precio_venta-error");
// });
// document.getElementById("ganancia").addEventListener("input", function () {
//     validarCampoNumerico("ganancia", "precio_venta-error");
// });
// document.getElementById("existencias").addEventListener("input", function () {
//     validarCampoNumerico("existencias", "precio_venta-error");
// });
// document.getElementById("existencias_deseadas").addEventListener("input", function () {
//     validarCampoNumerico("existencias_deseadas", "precio_venta-error");
// });


// Agrega más llamadas a validarCampoNumerico para otros campos si es necesario
