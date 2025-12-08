// Validar acceso para administradores academicos
validarAcceso(["administrador_academico"]);

document.addEventListener('DOMContentLoaded', () => {
    const entrevistaForm = document.getElementById('entrevista-form');
    const aspiranteInfo = document.getElementById('aspirante-info');

    // Retry counter for activity diagram compliance (max 4 attempts)
    let intentosCarga = 0;
    let intentosEnvio = 0;
    const MAX_INTENTOS = 4;

    // Get ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    const idSolicitud = urlParams.get('id');

    if (!idSolicitud) {
        showMessage('No se ha especificado ninguna solicitud', 'error', 5000);
        setTimeout(() => {
            window.history.back();
        }, 5000);
        return;
    }

    // Load Solicitud Details
    cargarInfoSolicitud();

    function cargarInfoSolicitud() {
        fetch('http://127.0.0.1:8000/api/citaciones/solicitudes/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('DB Error');
                }
                return response.json();
            })
            .then(data => {
                // Reset retry counter on success
                intentosCarga = 0;

                const solicitud = data.find(s => s.id_solicitud == idSolicitud);
                if (solicitud) {
                    aspiranteInfo.textContent = `Aspirante: ${solicitud.nombre_aspirante} (Acudiente: ${solicitud.nombre_acudiente})`;
                } else {
                    aspiranteInfo.textContent = `Solicitud ID: ${idSolicitud}`;
                }
            })
            .catch(error => {
                console.error('Error loading solicitud info:', error);
                intentosCarga++;

                // Activity diagram: check if intentos > 4
                if (intentosCarga > MAX_INTENTOS) {
                    showMessage('por favor vuelva a intentarlo más tarde', 'error', 5000);
                } else {
                    // Activity diagram: "Mostrar mensaje de error de conexión con la base de datos, por favor intente más tarde, durante 5 segundos"
                    showMessage('error de conexión con la base de datos, por favor intente más tarde', 'error', 5000);
                }
            });
    }

    entrevistaForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const comentario = document.getElementById('comentario').value;
        const fecha = document.getElementById('fecha').value;
        const hora = document.getElementById('hora').value;
        const lugar = document.getElementById('lugar').value.trim();

        // Activity diagram: "¿Todos los campos han sido llenados correctamente?"
        // Note: comentario is optional as per activity diagram
        if (!fecha || !hora || !lugar) {
            // Activity diagram: "Mostrar mensaje de por favor complete los campos correctamente, durante 5 segundos"
            showMessage('por favor complete los campos correctamente', 'error', 5000);
            return;
        }

        const data = {
            id_solicitud: idSolicitud,
            comentario: comentario,
            fecha: fecha,
            hora: hora,
            lugar: lugar
        };

        fetch('http://127.0.0.1:8000/api/citaciones/entrevista/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (response.ok) {
                    return response.json().then(data => {
                        // Reset retry counter on success
                        intentosEnvio = 0;
                        // Activity diagram: "Mostrar mensaje de se ha enviado la citación de entrevista exitosamente, durante 5 segundos"
                        showMessage('se ha enviado la citación de entrevista exitosamente', 'success', 5000);
                        // Redirect back to requests list after message
                        setTimeout(() => {
                            window.location.href = '../../solicitudes/vista_solicitudes/vista_solicitudes.html';
                        }, 5000);
                    });
                } else {
                    return response.json().then(err => {
                        throw new Error(err.error || 'Error');
                    });
                }
            })
            .catch(error => {
                console.error('Error sending interview citation:', error);
                intentosEnvio++;

                // Activity diagram: check if intentos > 4
                if (intentosEnvio > MAX_INTENTOS) {
                    showMessage('por favor vuelva a intentarlo más tarde', 'error', 5000);
                } else {
                    // Determine if it's a DB error or email error based on message
                    const errorMsg = error.message.toLowerCase();
                    if (errorMsg.includes('correo') || errorMsg.includes('mail') || errorMsg.includes('smtp')) {
                        // Activity diagram: "Mostrar mensaje de ha ocurrido un error al enviar el correo, por favor inténtelo más tarde, durante 5 segundos"
                        showMessage('ha ocurrido un error al enviar el correo, por favor inténtelo más tarde', 'error', 5000);
                    } else {
                        // Activity diagram: "Error de conexión a la BD"
                        showMessage('error de conexión con la base de datos, por favor intente más tarde', 'error', 5000);
                    }
                }
            });
    });
});
