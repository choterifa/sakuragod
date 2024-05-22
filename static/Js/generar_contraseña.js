document.addEventListener("DOMContentLoaded", function () {
    const generatePasswordBtn = document.getElementById("generatePasswordBtn");
    const passwordInput = document.getElementById("password");

    // Función para generar una contraseña aleatoria de letras y números
    function generatePassword(length) {
        const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        let password = "";
        for (let i = 0; i < length; i++) {
            const randomIndex = Math.floor(Math.random() * charset.length);
            password += charset[randomIndex];
        }
        return password;
    }

    // Evento clic en el botón "Generar"
    generatePasswordBtn.addEventListener("click", function () {
        const newPassword = generatePassword(12); // Cambiar el número 12 por la longitud deseada de la contraseña
        passwordInput.value = newPassword;
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const togglePasswordBtn = document.getElementById("togglePasswordBtn");
    const passwordInput = document.getElementById("password");
    const toggleIcon = document.getElementById("toggleIcon");

    // Función para cambiar entre mostrar y ocultar la contraseña
    function togglePasswordVisibility() {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            toggleIcon.classList.remove("bi-eye");
            toggleIcon.classList.add("bi-eye-slash");
        } else {
            passwordInput.type = "password";
            toggleIcon.classList.remove("bi-eye-slash");
            toggleIcon.classList.add("bi-eye");
        }
    }

    // Evento clic en el botón "Mostrar/Ocultar"
    togglePasswordBtn.addEventListener("click", function () {
        togglePasswordVisibility();
    });
});
