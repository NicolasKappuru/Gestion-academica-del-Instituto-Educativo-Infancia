const form = document.getElementById('resetForm');
const messageBox = document.getElementById('messageBox');
let isBlocked = false;

function showMessage(text, type, duration = 3000) {
    messageBox.textContent = text;
    messageBox.className = `message ${type}`;
    messageBox.style.display = 'block';

    if (duration > 0) {
        setTimeout(() => {
            messageBox.style.display = 'none';
        }, duration);
    }
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (isBlocked) return;

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
            // Escenario B: Datos Válidos -> Mensaje "Revisar el correo electrónico" por 5 seg (aprox, el diagrama dice mostar mensaje)
            // El diagrama dice: "Mostrar mensaje de revisar el correo electrónico" -> Fin de esta parte de la UI (usuario va al correo).
            // No dice que se cierre sola, pero asumimos visualización temporal o info.
            showMessage("Revisar el correo electrónico", "success", 5000);
            form.reset();
        } else {
            // Escenario A: Datos Inválidos
            if (response.status === 403) {
                // Bloqueo
                showMessage("Bloqueo por 5 minutos", "error", 0); // 0 = no ocultar automaticamente o manejar aparte
                isBlocked = true;
                form.querySelector('button').disabled = true;
                setTimeout(() => {
                    isBlocked = false;
                    form.querySelector('button').disabled = false;
                    messageBox.style.display = 'none';
                }, 5 * 60 * 1000); // 5 minutos
            } else {
                // Mensaje simple "Datos incorrectos" por 3 segundos
                showMessage("Datos incorrectos", "error", 3000);
            }
        }

    } catch (error) {
        // Error de conexión
        showMessage("Error de conexión a la BD", "error", 3000); // Usamos 3s como standar para mensajes de error temporales
    }
});
