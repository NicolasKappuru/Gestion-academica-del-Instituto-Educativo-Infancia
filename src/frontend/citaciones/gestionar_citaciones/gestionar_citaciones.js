// Validar acceso para administradores academicos
validarAcceso(["administrador_academico"]);

document.addEventListener('DOMContentLoaded', () => {
    const grupoSelect = document.getElementById('grupo-select');
    const consultarBtn = document.getElementById('consultar-btn');
    const studentsSection = document.getElementById('students-section');
    const formSection = document.getElementById('form-section');
    const studentsTableBody = document.getElementById('students-table-body');
    const citacionForm = document.getElementById('citacion-form');
    const btnSelectAll = document.getElementById('btn-select-all');

    // Track if all are selected
    let allSelected = false;

    // Retry counter for activity diagram compliance (max 4 attempts)
    let intentosConsulta = 0;
    let intentosEnvio = 0;
    const MAX_INTENTOS = 4;

    // Check for group ID from admin view (auto-load mode)
    const grupoCitarId = localStorage.getItem('grupo_citar_id');

    if (grupoCitarId) {
        // Auto-load mode
        document.querySelector('.selection-section').style.display = 'none';
        consultarEstudiantes(grupoCitarId);
        localStorage.removeItem('grupo_citar_id'); // Clear after use
    } else {
        // Normal mode: Load Groups
        cargarGrupos();
    }

    function cargarGrupos() {
        fetch('http://127.0.0.1:8000/api/citaciones/grupos/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('DB Error');
                }
                return response.json();
            })
            .then(data => {
                data.forEach(grupo => {
                    const option = document.createElement('option');
                    option.value = grupo.id_grupo;
                    option.textContent = grupo.nombre_grupo;
                    grupoSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error loading groups:', error);
                // Activity diagram: "error de conexión con la base de datos, por favor intente mas tarde, durante 5 segundos"
                showMessage('error de conexión con la base de datos, por favor intente mas tarde', 'error', 5000);
            });
    }

    // Consult Students Button (Manual mode)
    consultarBtn.addEventListener('click', () => {
        const idGrupo = grupoSelect.value;
        if (!idGrupo) {
            showMessage('Por favor seleccione un grupo', 'error', 5000);
            return;
        }
        consultarEstudiantes(idGrupo);
    });

    function consultarEstudiantes(idGrupo) {
        fetch(`http://127.0.0.1:8000/api/citaciones/grupos/${idGrupo}/estudiantes/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('DB Error');
                }
                return response.json();
            })
            .then(data => {
                // Reset retry counter on success
                intentosConsulta = 0;

                studentsTableBody.innerHTML = '';
                if (data.length === 0) {
                    showMessage('No se encontraron estudiantes con acudientes para este grupo', 'error', 5000);
                    studentsSection.style.display = 'none';
                    formSection.style.display = 'none';
                    return;
                }

                data.forEach(est => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td><input type="checkbox" class="student-checkbox" data-student='${JSON.stringify(est)}'></td>
                        <td>${est.nombre_estudiante}</td>
                        <td>${est.nombre_acudiente}</td>
                        <td>${est.correo_acudiente}</td>
                    `;
                    studentsTableBody.appendChild(row);
                });
                studentsSection.style.display = 'block';
                formSection.style.display = 'block';

                // Reset select all state
                allSelected = false;
                btnSelectAll.textContent = 'Seleccionar todos';
            })
            .catch(error => {
                console.error('Error loading students:', error);
                intentosConsulta++;

                // Activity diagram: check if intentos > 4
                if (intentosConsulta > MAX_INTENTOS) {
                    showMessage('Por favor vuelva a intentarlo más tarde', 'error', 5000);
                } else {
                    showMessage('Error de conexión con la base de datos, por favor intente mas tarde', 'error', 5000);
                }
            });
    }

    // Select All / Deselect All button handler
    btnSelectAll.addEventListener('click', () => {
        const checkboxes = document.querySelectorAll('.student-checkbox');
        allSelected = !allSelected;

        checkboxes.forEach(cb => {
            cb.checked = allSelected;
        });

        // Update button text
        btnSelectAll.textContent = allSelected ? 'Deseleccionar todos' : 'Seleccionar todos';
    });

    // Send Citations
    citacionForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const selectedCheckboxes = document.querySelectorAll('.student-checkbox:checked');

        // Activity diagram: "¿Se selecciono por lo menos un acudiente?"
        if (selectedCheckboxes.length === 0) {
            showMessage('Por favor seleccione almenos un estudiante', 'error', 5000);
            return;
        }

        // Validate form fields
        const motivo = document.getElementById('motivo').value.trim();
        const fecha = document.getElementById('fecha').value;
        const hora = document.getElementById('hora').value;
        const lugar = document.getElementById('lugar').value.trim();

        // Activity diagram: "¿Todos los campos han sido llenados correctamente?"
        if (!motivo || !fecha || !hora || !lugar) {
            showMessage('Por favor complete los campos correctamente', 'error', 5000);
            return;
        }

        const citaciones = [];
        selectedCheckboxes.forEach(cb => {
            citaciones.push(JSON.parse(cb.getAttribute('data-student')));
        });

        const data = {
            citaciones: citaciones,
            motivo: motivo,
            fecha: fecha,
            hora: hora,
            lugar: lugar
        };

        fetch('http://127.0.0.1:8000/api/citaciones/enviar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (response.ok || response.status === 207) {
                    return response.json().then(data => {
                        intentosEnvio = 0;

                        // Activity diagram: "se han enviado las citaciones exitosamente, durante 5 segundos"
                        showMessage('Se han enviado las citaciones exitosamente', 'success', 5000);

                        // Reset form
                        citacionForm.reset();
                        document.querySelectorAll('.student-checkbox').forEach(cb => cb.checked = false);
                    });
                } else {
                    return response.json().then(err => {
                        throw new Error(err.error || 'Email Error');
                    });
                }
            })
            .catch(error => {
                console.error('Error sending citations:', error);

                intentosEnvio++;
                // Activity diagram: check if intentos > 4
                if (intentosEnvio > MAX_INTENTOS) {
                    showMessage('Por favor vuelva a intentarlo más tarde', 'error', 5000);
                } else {
                    // Activity diagram: "ha ocurrido un error al enviar el correo, por favor inténtelo más tarde, durante 5 segundos"
                    showMessage('Ha ocurrido un error al enviar el correo, por favor inténtelo más tarde', 'error', 5000);
                }
            });
    });
});
