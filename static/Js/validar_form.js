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

document.getElementById('precio_compra').addEventListener('input', function (e) {
    validateInput(e, 30, 0, 1000);
});

document.getElementById('precio_venta').addEventListener('input', function (e) {
    validateInput(e, 30, 0, 1000);
});

document.getElementById('existencias').addEventListener('input', function (e) {
    validateInput(e, 30, 0, 500);
});

document.getElementById('existencias_deseadas').addEventListener('input', function (e) {
    validateInput(e, 30, 0, 500);
});
