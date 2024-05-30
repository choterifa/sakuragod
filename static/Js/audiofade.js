document.addEventListener('DOMContentLoaded', (event) => {
    const audio = document.getElementById('audio-fondo');
    audio.volume = 0; // Inicia el volumen en 0
    const fadeInTime = 5700; // Tiempo para hacer fade-in en milisegundos

    let fadeAudio = setInterval(() => {
        if (audio.volume < 1.0) {
            audio.volume = Math.min(audio.volume + 0.01, 1.0);
        } else {
            clearInterval(fadeAudio);
        }
    }, fadeInTime / 100); // Ajuste de tiempo de incremento

    audio.play();
});