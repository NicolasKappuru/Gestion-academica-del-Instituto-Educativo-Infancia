validarAcceso("administrador_academico");

const anio = new Date().getFullYear(); 

fetch("http://127.0.0.1:8000/api/listadoGruposPeriodo/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    },
    body: JSON.stringify({ anio })
})
.then(resp => resp.json())
.then(data => {

    if (data.error) {
        showMessage(data.error || "Ocurrió un error inesperado", "error");
        return;
    }

    cargarGrupos(data.grupos);
})
.catch(err => {
    showMessage(err || "Error de conexión intentelo mas tarde", "error");
});


function cargarGrupos(lista) {
    const tabla = document.getElementById("tablaGrupos");
    const template = document.getElementById("filaGrupoTemplate");

    tabla.innerHTML = "";

    lista.forEach(g => {
        const clone = template.content.cloneNode(true);

        clone.querySelector(".td-nombre").textContent = g.nombre;

        // Profesor asignado o botón
        const tdProfesor = clone.querySelector(".td-profesor");
        if (g.profesor_director) {
            tdProfesor.textContent = 
                `${g.profesor_director.nombre} ${g.profesor_director.apellido}`;
        } else {
            tdProfesor.innerHTML = 
                `<button class="btn-asignar" data-id="${g.id}">Asignar</button>`;
        }
        
        // Evento realizar
        clone.querySelector(".btn-realizar").addEventListener("click", () => {
            realizarGrupo(g.nombre);
        });

        // Evento asignar
        if (!g.profesor_director) {
            tdProfesor.querySelector(".btn-asignar").addEventListener("click", () => {
                abrirAsignarProfesor(g.id);
            });
        }

        tabla.appendChild(clone);
    });
}


function realizarGrupo(nombre) {
    alert("Realizando acciones para grupo: " + nombre);
}

document.addEventListener("DOMContentLoaded", function () {

    const btnAdminSolicitudes = document.querySelector(".btn-opcion");

    btnAdminSolicitudes.addEventListener("click", function () {
        window.location.href = "../../solicitudes/vista_solicitudes.html"; 
        // Aquí pones el HTML al que quieres redirigir.
    });

});

function abrirAsignarProfesor(idGrupo) {
    localStorage.setItem("grupo_a_asignar", idGrupo);
    window.location.href = "../asignar_profesor/asignar_profesor.html";
}
