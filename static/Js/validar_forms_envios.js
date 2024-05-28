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

document.getElementById('calle').addEventListener('input', function (e) {
    validateInput(e, 30, 0, 1000);
});

document.getElementById('cruzamiento_1').addEventListener('input', function (e) {
    validateInput(e, 30, 0, 1000);
});

document.getElementById('cruzamiento_2').addEventListener('input', function (e) {
    validateInput(e, 30, 0, 1000);
});

document.addEventListener('DOMContentLoaded', function () {
    var modal = document.getElementById('abrirModal');
    var resetButton = document.getElementById('btn_reset');

    modal.addEventListener('show.bs.modal', function () {
        resetButton.click();
    });
});