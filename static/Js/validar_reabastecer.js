function validateNumberInput(event, minLength, maxValue) {
    var numericValue = parseFloat(event.target.value);

    // Limitar la longitud máxima del valor
    var value = event.target.value.toString();
    if (value.length > minLength) {
        event.target.value = value.slice(0, minLength);
    }

    // Asegurar el rango de valores
    if (numericValue < 0 || isNaN(numericValue)) {
        event.target.value = 0;
    } else if (numericValue > maxValue) {
        event.target.value = maxValue;
    }
}

document.addEventListener('DOMContentLoaded', function () {
    var resurtirCantidadInputs = document.querySelectorAll('.resurtir-cantidad');

    resurtirCantidadInputs.forEach(function (input) {
        input.addEventListener('input', function (e) {
            validateNumberInput(e, 10, 500);
        });
    });
});