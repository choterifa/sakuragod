var audio = document.getElementById("audio-fondo");
var toggleAudio = document.getElementById("audio");
var audioEncendido = false;

toggleAudio.addEventListener("click", function (event) {
    event.preventDefault(); // Evitar la acción predeterminada del enlace

    if (!audioEncendido) {
        audio.play(); // Reproducir el audio
        toggleAudio.innerHTML = '<i class="bi bi-pause-fill"></i>'; // Cambiar a icono de audio encendido

        audioEncendido = true;
    } else {
        audio.pause(); // Pausar el audio
        toggleAudio.innerHTML = '<i class="bi bi-music-note-beamed"></i>'; // Cambiar a icono de audio encendido

        audioEncendido = false;
    }
});
