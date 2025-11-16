// USUARIOS DE PRUEBA (luego esto vendrá de tu backend)
const usuariosDemo = [
    { nombre: "Pepito Perez", estado: "Deshabilitado" },
    { nombre: "Juan Carlos", estado: "Habilitado" }
];

const tabla = document.getElementById("tablaBody");
const rolSelect = document.getElementById("rolSelect");
const btnCrear = document.getElementById("btnCrearUsuario");

// Render dinámico de usuarios
function renderUsuarios(lista) {
    tabla.innerHTML = "";

    lista.forEach(u => {
        const fila = document.createElement("tr");

        fila.innerHTML = `
            <td>${u.nombre}</td>
            <td>${u.estado}</td>
            <td>
                <button class="btn-accion ${u.estado === "Habilitado" ? "btn-deshabilitar" : "btn-habilitar"}">
                    ${u.estado === "Habilitado" ? "Deshabilitar" : "Habilitar"}
                </button>
            </td>
        `;

        tabla.appendChild(fila);
    });
}

// Evento de cambio de ROL
rolSelect.addEventListener("change", () => {
    // Aquí luego harás fetch al backend
    renderUsuarios(usuariosDemo);
});

// Event crear usuario
btnCrear.addEventListener("click", () => {
    window.location.href = "../crear_usuario/crear.html"; // Ajusta ruta
});

// Render inicial vacío
renderUsuarios([]);
