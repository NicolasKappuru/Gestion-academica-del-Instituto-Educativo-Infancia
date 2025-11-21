const lista = document.getElementById("listaCodigos");

// ------------------------------
// 1. Botón Volver
// ------------------------------
document.getElementById("btnVolver").addEventListener("click", () => {
    window.location.href = "../interfaz_admin_usuarios/vista_admin_usuarios.html";
});

// ------------------------------
// 2. Cargar listado desde el backend
// ------------------------------
async function cargarListado(page = 1, page_size = 10) {
    try {
        const response = await fetch("http://127.0.0.1:8000/api/listarCreacionAcudientes/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ page, page_size })
        });

        const data = await response.json();

        if (!response.ok) {
            console.error("Error al obtener datos:", data);
            return;
        }

        renderTabla(data.solicitudes);

    } catch (err) {
        console.error("Error en fetch:", err);
    }
}

// ------------------------------
// 3. Llenar tabla
// ------------------------------
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

    // Eventos de botones "Crear usuario"
    document.querySelectorAll(".btn-crear").forEach(btn => {
        btn.addEventListener("click", () => {
            const idSolicitud = btn.getAttribute("data-id");

            // Lógica provisional
            alert("Crear usuario para el código: " + idSolicitud);

            // Luego cambiarás esta ruta para la pantalla real:
            // window.location.href = `crear_usuario.html?id=${idSolicitud}`;
        });
    });
}

// ------------------------------
// 4. Ejecutar carga inicial
// ------------------------------
cargarListado();
