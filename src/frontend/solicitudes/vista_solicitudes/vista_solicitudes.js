import { aceptarSolicitud } from "../aceptar_solicitud.js";
import { rechazarSolicitud } from "../rechazar_solicitud.js";

validarAcceso("administrador_academico");

const tabla = document.getElementById("tablaSolicitudes");
const btnPrev = document.getElementById("btnPrev");
const btnNext = document.getElementById("btnNext");
const pageInfo = document.getElementById("pageInfo");

let paginaActual = 1;
let totalPaginas = 1;
const pageSize = 10;

document.getElementById("btnVolver").addEventListener("click", () => {
    window.location.href = "../../academico/vista_admin_academico/vista_admin_academico.html";
});

async function cargarSolicitudes() {
    try {
        const token = localStorage.getItem("access_token");
        const resp = await fetch("http://localhost:8000/api/listarSolicitudes/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                page: paginaActual,
                page_size: pageSize
            })
        });

        const data = await resp.json();
        if (!resp.ok) {
            showMessage(data.error || "Error al obtener solicitudes", "error");
            return;
        }

        totalPaginas = data.total_pages || 1;
        renderSolicitudes(data.solicitudes || []);
        actualizarControles();
    } catch (err) {
        showMessage("Error de conexión. Intente más tarde.", "error");
    }
}

function renderSolicitudes(lista) {
    tabla.innerHTML = "";
    lista.forEach(sol => {
        const fila = document.createElement("tr");

        // determinar clases / disabled según estado
        const estado = sol.estado || "";
        const citarDisabled = (estado !== "Pendiente");
        const aceptarDisabled = (estado === "Aceptada" || estado === "Rechazada");
        const rechazarDisabled = aceptarDisabled;

        fila.innerHTML = `
            <td>${sol.id}</td>
            <td>${sol.aspirante}</td>
            <td>${sol.grado}</td>
            <td><b>${sol.cupos !== null ? sol.cupos : ""}</b></td>
            <td>${estado}</td>

            <td><button class="btn-aceptar" data-id="${sol.id}" ${aceptarDisabled ? "disabled" : ""}>✔️</button></td>
            <td><button class="btn-rechazar" data-id="${sol.id}" ${rechazarDisabled ? "disabled" : ""}>✖️</button></td>
            <td><button class="btn-citar" data-id="${sol.id}" ${citarDisabled ? "disabled style='opacity:.5;cursor:not-allowed'" : ""}>Citar</button></td>
        `;

        tabla.appendChild(fila);
    });

    activarEventos();
}

function activarEventos() {
    // aceptar
    document.querySelectorAll(".btn-aceptar").forEach(btn => {
        btn.addEventListener("click", async () => {
            const id = btn.dataset.id;
            btn.disabled = true;
            const res = await aceptarSolicitud(id);
            if (res && res.ok) {
                await cargarSolicitudes();
                showMessage("Solicitud aceptada correctamente", "success");
            } else {
                btn.disabled = false;
                showMessage("No se pudo aceptar la solicitud", "error");
            }
        });
    });

    // rechazar
    document.querySelectorAll(".btn-rechazar").forEach(btn => {
        btn.addEventListener("click", async () => {
            const id = btn.dataset.id;
            btn.disabled = true;
            const res = await rechazarSolicitud(id);
            if (res && res.ok) {
                await cargarSolicitudes();
                showMessage("Solicitud rechazada", "success");

            } else {
                btn.disabled = false;
                showMessage("No se pudo rechazar la solicitud", "error");
            }
        });
    });

    // citar (redirecciona a formulario de citación si esta permitido)
    document.querySelectorAll(".btn-citar").forEach(btn => {
        btn.addEventListener("click", () => {
            const id = btn.dataset.id;
            // si quieres pasar id en querystring:
            window.location.href = `./citar_solicitud.html?id=${id}`;
        });
    });
}

// paginación
function actualizarControles() {
    pageInfo.textContent = `Página ${paginaActual} de ${totalPaginas}`;
    btnPrev.disabled = paginaActual === 1;
    btnNext.disabled = paginaActual === totalPaginas;
}

btnPrev.addEventListener("click", () => {
    if (paginaActual > 1) {
        paginaActual--;
        cargarSolicitudes();
    }
});
btnNext.addEventListener("click", () => {
    if (paginaActual < totalPaginas) {
        paginaActual++;
        cargarSolicitudes();
    }
});

// carga inicial
document.addEventListener("DOMContentLoaded", cargarSolicitudes);
