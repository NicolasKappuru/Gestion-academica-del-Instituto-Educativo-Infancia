validarAcceso("administrador_usuarios");

document.addEventListener("DOMContentLoaded", () => {

    const lista = document.getElementById("listaCodigos");

    // Botón Volver
    document.getElementById("btnVolver").addEventListener("click", () => {
        window.location.href = "../vista_admin_usuarios/vista_admin_usuarios.html";
    });

    // ---- PAGINACIÓN ----
    let paginaActual = 1;
    const pageSize = 10;
    let totalPaginas = 1;

    async function cargarListado(page = 1) {
        try {
            const token = localStorage.getItem("access_token");

            const response = await fetch(`${API_BASE_URL}/api/listarCreacionAcudientes/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ page, page_size: pageSize })
            });

            const data = await response.json();

            if (!response.ok) {
                showMessage("Error al obtener datos, intente más tarde", "error");
                console.error("Error al obtener listado:", data);
                return;
            }

            // render solicitudes
            renderTabla(data.solicitudes);

            // actualizar paginación
            paginaActual = data.page;
            totalPaginas = data.total_pages;
            actualizarControles();

        } catch (err) {
            showMessage("Error al obtener datos, intente más tarde", "error");
            console.error("Error:", err);
        }
    }

    // Render tabla con botones
    function renderTabla(solicitudes) {
        lista.innerHTML = "";

        if (!solicitudes || solicitudes.length === 0) {
            lista.innerHTML = `
                <tr><td colspan="2" style="text-align:center;">No hay solicitudes pendientes</td></tr>
            `;
            return;
        }

        solicitudes.forEach(item => {
            const fila = document.createElement("tr");

            fila.innerHTML = `
                <td>${item.codigo_creacion}</td>
                <td>
                    <button class="btn-crear" data-id="${item.id_solicitud}">
                        Crear usuario
                    </button>
                </td>
            `;

            lista.appendChild(fila);
        });

        document.querySelectorAll(".btn-crear").forEach(btn => {
            btn.addEventListener("click", () => {
                const idSolicitud = btn.getAttribute("data-id");
                crearUsuarioDesdeSolicitud(idSolicitud);
            });
        });
    }

    // Crear usuario Acudiente usando la solicitud
    async function crearUsuarioDesdeSolicitud(idSolicitud) {
        if (!idSolicitud) {
            showMessage("ID de solicitud inválido", "error");
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/api/crearUsuarioAcudiente/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + localStorage.getItem("access_token")
                },
                body: JSON.stringify({ id_solicitud: idSolicitud })
            });

            const data = await response.json();

            if (!response.ok) {
                showMessage("Error: " + (data.error || "No se pudo procesar la solicitud"), "error");

                // IMPORTANTE: si ya existe el usuario, backend marca como Finalizada → recargar lista
                if (data.error && data.error.includes("Ya existe un usuario")) {
                    cargarListado(paginaActual);
                }

                return;
            }

            showMessage("Usuario creado correctamente para el acudiente", "success");

            // Actualizar tabla para que la solicitud desaparezca
            cargarListado(paginaActual);

        } catch (error) {
            showMessage("Error al conectar con el servidor", "error");
            console.log(error);
        }
    }

    // ---- Controles de paginación ----
    const btnPrev = document.getElementById("btnPrev");
    const btnNext = document.getElementById("btnNext");
    const pageInfo = document.getElementById("pageInfo");

    function actualizarControles() {
        pageInfo.textContent = `Página ${paginaActual} de ${totalPaginas}`;
        btnPrev.disabled = paginaActual <= 1;
        btnNext.disabled = paginaActual >= totalPaginas;
    }

    btnPrev.addEventListener("click", () => {
        if (paginaActual > 1) {
            paginaActual--;
            cargarListado(paginaActual);
        }
    });

    btnNext.addEventListener("click", () => {
        if (paginaActual < totalPaginas) {
            paginaActual++;
            cargarListado(paginaActual);
        }
    });

    // ---- Carga inicial ----
    cargarListado();

});
