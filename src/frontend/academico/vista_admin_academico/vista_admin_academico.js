// Primero validar acceso, igual que en usuarios
validarAcceso("administrador_academico");

const tabla = document.getElementById("tablaGrupos");
const template = document.getElementById("filaGrupoTemplate");

const anio = new Date().getFullYear();

// Cargar grupos
async function cargarGrupos() {
    try {
        const token = localStorage.getItem("access_token");

        const response = await fetch("http://127.0.0.1:8000/api/listadoGruposPeriodo/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ anio })
        });

        const data = await response.json();

        if (response.ok) {
            renderGrupos(data.grupos);
        } else {
            showMessage(data.error || "Ocurrió un error inesperado", "error");
        }

    } catch (error) {
        showMessage("Error al conectar con el servidor. Inténtelo más tarde.", "error");
    }
}


// Renderizado de tabla
function renderGrupos(lista) {
    tabla.innerHTML = "";

    lista.forEach(g => {
        const clone = template.content.cloneNode(true);

        clone.querySelector(".td-nombre").textContent = g.nombre;

        const tdProfesor = clone.querySelector(".td-profesor");

        if (g.profesor_director) {
            tdProfesor.textContent = 
                `${g.profesor_director.nombre} ${g.profesor_director.apellido}`;
        } else {
            tdProfesor.innerHTML =
                `<button class="btn-asignar" data-id="${g.id}">Asignar</button>`;
        }

        // Botón realizar
        clone.querySelector(".btn-realizar").addEventListener("click", () => {
            realizarGrupo(g.nombre);
        });

        // Botón asignar
        if (!g.profesor_director) {
            clone.querySelector(".btn-asignar").addEventListener("click", () => {
                abrirAsignarProfesor(g.id);
            });
        }

        tabla.appendChild(clone);
    });
}


// Acciones auxiliares
function realizarGrupo(nombre) {
    alert("Realizando acciones para grupo: " + nombre);
}

function abrirAsignarProfesor(idGrupo) {
    localStorage.setItem("grupo_a_asignar", idGrupo);
    window.location.href = "../asignar_profesor/asignar_profesor.html";
}


// Botón de "Solicitudes"
document.querySelector(".btn-opcion").addEventListener("click", () => {
    window.location.href = "../../solicitudes/vista_solicitudes/vista_solicitudes.html";
});


// Carga inicial (igual que en usuarios)
cargarGrupos();
