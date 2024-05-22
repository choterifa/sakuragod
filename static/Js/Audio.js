var audio = document.getElementById("audio-fondo");
var toggleAudio = document.getElementById("audio");
var audioEncendido = true; // Inicialmente true porque el audio está reproduciéndose

// Configurar el icono inicial
toggleAudio.innerHTML = '<i class="bi bi-pause-fill"></i>';

toggleAudio.addEventListener("click", function (event) {
    event.preventDefault(); // Evitar la acción predeterminada del enlace

    if (audioEncendido) {
        audio.pause(); // Pausar el audio
        toggleAudio.innerHTML = '<i class="bi bi-music-note-beamed"></i>'; // Cambiar a icono de play
        audioEncendido = false;
    } else {
        audio.play(); // Reproducir el audio
        toggleAudio.innerHTML = '<i class="bi bi-pause-fill"></i>'; // Cambiar a icono de pausa
        audioEncendido = true;
    }
});


// Lista de reproducción de audios
const playlist = [
    "../../static/Audio/Audio.mp3",
    "../../static/Audio/ventura.mp3",
    "../../static/Audio/mavine.mp3"
];

let currentTrack = 0;
const audioElement = document.getElementById('audio-fondo');

// Función para reproducir el siguiente audio en la lista de reproducción
function playNextTrack() {
    currentTrack++;
    if (currentTrack < playlist.length) {
        audioElement.src = playlist[currentTrack];
        audioElement.play();
    } else {
        currentTrack = 0; // Reinicia la lista de reproducción
        audioElement.src = playlist[currentTrack];
        audioElement.play();
    }
}

// Evento para cuando el audio termine de reproducirse
audioElement.addEventListener('ended', playNextTrack);

// Iniciar la reproducción del primer audio
audioElement.src = playlist[0];
audioElement.play();