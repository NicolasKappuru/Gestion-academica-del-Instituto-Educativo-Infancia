const form = document.getElementById('newPasswordForm');
const formContainer = document.getElementById('formContainer');
const expiredContainer = document.getElementById('expiredContainer');

// Obtener params de la URL
const urlParams = new URLSearchParams(window.location.search);
const token = urlParams.get('token');
const uid = urlParams.get('uid'); // Nuevo standard
const codigo_usuario = urlParams.get('id'); // Legacy support

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

// Validar que exista al menos uno de los IDs y el token
if (!token || (!uid && !codigo_usuario)) {
    // Si faltan datos críticos, asumir link roto/expirado
    formContainer.style.display = 'none';
    expiredContainer.style.display = 'block';
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const password_1 = document.getElementById('password_1').value;
    const password_2 = document.getElementById('password_2').value;

    try {
        const response = await fetch('http://127.0.0.1:8000/api/restablecer/validar-contrasena/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                uid: uid,
                codigo_usuario: codigo_usuario,
                token: token,
                password_1: password_1,
                password_2: password_2
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Exito
            window.showMessage("Contraseña actualizada exitosamente", "success", 5000);
            setTimeout(() => {
                window.location.href = '../../login/login.html';
            }, 5000);
        } else {
            // Manejo de errores especificos
            if (data.error === "El enlace de activación ha caducado" || data.error === "Usuario no válido") {
                // Caso Token Expirado o Usuario no encontrado
                formContainer.style.display = 'none';
                expiredContainer.style.display = 'block';
            } else if (response.status === 403) {
                // Intentar más tarde / Bloqueo
                window.showMessage(data.error || "Intentar más tarde", "error", 5000);
                // Opcional: deshabilitar por un momento
                form.querySelector('button').disabled = true;
                setTimeout(() => {
                    form.querySelector('button').disabled = false;
                }, 5000);
            } else {
                // Otros errores (pass no coincide, etc)
                if (data.error === 'Contraseña no coincide') {
                    window.showMessage("Contraseña no coincide", "error", 3000);
                } else {
                    window.showMessage(data.error || "Error al actualizar", "error", 3000);
                }
            }
        }

    } catch (error) {
        window.showMessage("Ha ocurrido un error... intente más tarde", "error", 5000);
    }
});
