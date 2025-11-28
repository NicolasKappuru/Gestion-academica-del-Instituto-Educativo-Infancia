validarAcceso("acudiente");

const username = localStorage.getItem("username");

fetch("http://127.0.0.1:8000/api/listadoEstudiantesBoletines/", {
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
                <button class="btn-ver" onclick="verBoletin('${est.nombre}')">Ver</button>
            </td>
        `;

        tabla.appendChild(fila);
    });
}

function verBoletin(nombre) {
    alert("Mostrando boletín de: " + nombre);
}
