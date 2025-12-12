validarAcceso("acudiente");

const username = localStorage.getItem("username");

fetch(`${API_BASE_URL}/api/listadoEstudiantesBoletines/`, {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    },
    body: JSON.stringify({ username })
})
    .then(resp => resp.json())
    .then(data => {

        if (data.error) {
            showMessage(data.error || "Ocurrió un error inesperado", "error");
            return;
        }

        cargarBoletines(data.estudiantes);
    })
    .catch(err => {
        showMessage(err || "Ocurrió un error inesperado", "error");
    });

function cargarBoletines(lista) {
    const tabla = document.getElementById("tablaBoletines");
    tabla.innerHTML = "";

    lista.forEach(est => {
        const fila = document.createElement("tr");

        fila.innerHTML = `
            <td>${est.nombre}</td>
            <td>
                <button class="btn-ver" onclick="verBoletin(${est.id_persona}, '${est.nombre}')">Ver</button>
            </td>
        `;


        tabla.appendChild(fila);
    });
}

function verBoletin(id_persona, nombre) {
    localStorage.setItem("id_estudiante_boletin", id_persona);
    localStorage.setItem("nombre_estudiante_boletin", nombre);

    window.location.href = "../boletin_particular/boletin_particular.html";
}
