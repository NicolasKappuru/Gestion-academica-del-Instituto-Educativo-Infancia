validarAcceso("administrador_usuarios");

document.addEventListener("DOMContentLoaded", () => {

    const lista = document.getElementById("listaCodigos");

    // Botón Volver
    document.getElementById("btnVolver").addEventListener("click", () => {
        window.location.href = "../vista_admin_usuarios/vista_admin_usuarios.html";
    });

    async function cargarListado(page = 1, page_size = 10) {
        try {
            const token = localStorage.getItem("access_token");

            const response = await fetch("http://127.0.0.1:8000/api/listarCreacionAcudientes/", {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ page, page_size })
            });

            const data = await response.json();
            
            if (!response.ok) {
                showMessage("Error al obtener datos, intente mas tarde", "error");
                console.error("Error al obtener datos:", data);
                return;
            }

            renderTabla(data.solicitudes);

        } catch (err) {
            showMessage("Error al obtener datos, intente mas tarde", "error");
            console.error("Error:", err);
        }
    }


    // Render tabla con botones
    function renderTabla(solicitudes) {
        lista.innerHTML = "";

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
            const response = await fetch("http://127.0.0.1:8000/api/crearUsuarioAcudiente/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + localStorage.getItem("access_token")
                },
                body: JSON.stringify({ id_solicitud: idSolicitud })
            });

            const data = await response.json();

            if (!response.ok) {
                showMessage("Error: " + (data.error || "No se pudo crear el usuario") , "error");
                return;
            }
            showMessage("Usuario creado correctamente para el acudiente" , "success");

            // recargar listado sin la solicitud
            cargarListado();

        } catch (error) {
            showMessage("Error al conectar con el servidor" , "error");
            console.log(error);
        }
    }

    // ------------------------------
    // Carga inicial
    // ------------------------------
    cargarListado();

});
