validarAcceso("administrador_academico");

const idGrupo = localStorage.getItem("grupo_a_asignar");

// 1. Obtener lista de profesores
fetch(`${API_BASE_URL}/api/listarProfesores/`, {
    method: "GET"
})
    .then(r => r.json())
    .then(data => {
        const cont = document.getElementById("contenedor-profesores");

        data.profesores.forEach(p => {
            const div = document.createElement("div");
            div.classList.add("prof-card");

            div.innerHTML = `
            <p>${p.nombre} ${p.apellido}</p>
            <button onclick="asignar(${p.id_persona})">Asignar</button>
        `;

            cont.appendChild(div);
        });
    })
    .catch(err => console.error(err));


// 2. Asignar profesor a grupo
function asignar(idProfesor) {
    fetch(`${API_BASE_URL}/api/asignarProfesor/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`
        },
        body: JSON.stringify({
            grupo: idGrupo,
            profesor: idProfesor
        })
    })
        .then(r => r.json())
        .then(data => {
            if (data.error)
                alert("Error: " + data.error);
            else {
                alert("Profesor asignado correctamente");
                window.location.href = "../vista_admin_academico/vista_admin_academico.html";
            }
        });
}
