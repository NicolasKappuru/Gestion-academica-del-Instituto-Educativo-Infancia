const form = document.getElementById('resetForm');

// Verificación de seguridad para msg global con reintento
let msgCheckInterval = setInterval(() => {
    if (typeof window.showMessage === 'function') {
        clearInterval(msgCheckInterval);
    } else {
        console.warn("Esperando carga de mensaje.js...");
    }
}, 100);

// Timeout de seguridad para limpiar intervalo
setTimeout(() => clearInterval(msgCheckInterval), 5000);

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const codigo_usuario = document.getElementById('codigo_usuario').value;
    const email = document.getElementById('email').value;

    try {
        const response = await fetch('http://127.0.0.1:8000/api/restablecer/validar-datos/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ codigo_usuario, email })
        });

        const data = await response.json();

        if (response.ok) {
            window.showMessage("Revisar el correo electrónico", "success", 5000);
            form.reset();
        } else {
            if (response.status === 403) {
                // Mensaje simple de bloqueo por 5 segundos
                window.showMessage("Bloqueado por 5 minutos", "error", 5000);
            } else {
                window.showMessage("Datos incorrectos", "error", 3000);
            }
        }

    } catch (error) {
        window.showMessage("Error de conexión a la BD", "error", 3000);
    }
});
