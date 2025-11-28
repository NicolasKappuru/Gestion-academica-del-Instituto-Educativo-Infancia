import { cambiarEstado } from "./habilitar_deshabilitar.js";

validarAcceso("administrador_usuarios");

// Variables globales
const tabla = document.getElementById("tablaBody");
const rolSelect = document.getElementById("rolSelect");
const btnCrear = document.getElementById("btnCrearUsuario");

// Paginación
let paginaActual = 1;
let totalPaginas = 1;
const pageSize = 10;
let rolActual = "";

// Controles de paginación
const btnPrev = document.getElementById("btnPrev");
const btnNext = document.getElementById("btnNext");
const pageInfo = document.getElementById("pageInfo");


// Cargar usuarios 
async function cargarUsuarios() {
    if (!rolActual) return;

    try {
        const token = localStorage.getItem("access_token");

        const response = await fetch("http://localhost:8000/api/listarUsuarios/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                role: rolActual,
                page: paginaActual,
                page_size: pageSize
            })
        });

        const data = await response.json();

        if (response.ok) {
            renderUsuarios(data.usuarios);

            totalPaginas = data.total_pages;
            actualizarControles();
        } else {
            showMessage(data.error || "Ocurrió un error inesperado", "error");
        }

    } catch (error) {
        showMessage("Error al conectar con el servidor. Verifica tu conexión o intenta más tarde.", "error");
    }
}


// Renderizar tabla
function renderUsuarios(lista) {
    tabla.innerHTML = "";

    lista.forEach(u => {
        const fila = document.createElement("tr");

        fila.innerHTML = `
            <td>${u.nombre}</td>
            <td>${u.estado}</td>
            <td>
                <button 
                    class="btn-accion ${u.estado === "Habilitado" ? "btn-deshabilitar" : "btn-habilitar"}"
                    data-user="${u.id_user}">
                    ${u.estado === "Habilitado" ? "Deshabilitar" : "Habilitar"}
                </button>
            </td>
        `;

        tabla.appendChild(fila);
    });

    activarBotonesAccion();
}

function activarBotonesAccion() {
    document.querySelectorAll(".btn-accion").forEach(btn => {
        btn.addEventListener("click", async () => {
            const userId = btn.getAttribute("data-user");
            await cambiarEstado(userId);
            cargarUsuarios();
        });
    });
}

// Controles de paginación
function actualizarControles() {
    pageInfo.textContent = `Página ${paginaActual} de ${totalPaginas}`;

    btnPrev.disabled = paginaActual === 1;
    btnNext.disabled = paginaActual === totalPaginas;
}

btnPrev.addEventListener("click", () => {
    if (paginaActual > 1) {
        paginaActual--;
        cargarUsuarios();
    }
});

btnNext.addEventListener("click", () => {
    if (paginaActual < totalPaginas) {
        paginaActual++;
        cargarUsuarios();
    }
});

// Evento para seleccionar rol
rolSelect.addEventListener("change", () => {
    const value = rolSelect.value;

    if (value === "") return;

    // Mapeo del select → roles reales del modelo
    const mapaRoles = {
        "acudiente": "acudiente",
        "profesor": "profesor",
        "directivo": "administrador_academico",
        "administrador": "administrador_usuarios"
    };

    rolActual = mapaRoles[value];
    paginaActual = 1;

    cargarUsuarios();
});


// Botón Crear Usuario
btnCrear.addEventListener("click", () => {
    window.location.href = "../creacion_usuario/creacion_usuario.html";
});

// Botón Crear Usuario Acudiente
const btnCrearAcudiente = document.getElementById("btnCrearUsuarioAcudinte");

btnCrearAcudiente.addEventListener("click", () => {
    window.location.href = "../creacion_usuario_acudiente/creacion_usuario_acudiente.html";
});
