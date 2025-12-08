const form = document.getElementById('newPasswordForm');
const messageBox = document.getElementById('messageBox');

// Obtener params de la URL
const urlParams = new URLSearchParams(window.location.search);
const token = urlParams.get('token');
const codigo_usuario = urlParams.get('id');

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

if (!token || !codigo_usuario) {
    showMessage("Enlace inválido o incompleto", "error", 0);
    form.querySelector('button').disabled = true;
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const password_1 = document.getElementById('password_1').value;
    const password_2 = document.getElementById('password_2').value;

    try {
        const response = await fetch('http://127.0.0.1:8000/api/restablecer/validar-contrasena/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ codigo_usuario, token, password_1, password_2 })
        });

        const data = await response.json();

        if (response.ok) {
            // Exito
            showMessage("Contraseña actualizada exitosamente", "success", 5000);
            setTimeout(() => {
                window.location.href = '../../login/login.html';
            }, 5000);
        } else {
            if (response.status === 403) { // Intentar más tarde / Bloqueo
                showMessage("Intentar más tarde", "error", 0);
                form.querySelector('button').disabled = true;
            } else {
                if (data.error === 'Contraseña no coincide') {
                    showMessage("Contraseña no coincide", "error", 3000); // 3 intentos o menos logic handled in backend to return 403 eventually
                } else {
                    showMessage(data.error || "Error al actualizar", "error", 3000);
                }
            }
        }

    } catch (error) {
        showMessage("Error de conexión a la BD", "error", 3000);
    }
});
