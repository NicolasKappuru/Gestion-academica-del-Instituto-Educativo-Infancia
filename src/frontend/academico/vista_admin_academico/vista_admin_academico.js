const anio = new Date().getFullYear(); // Año actual

fetch("http://127.0.0.1:8000/api/listadoGruposPeriodo/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({ anio })
})
.then(resp => resp.json())
.then(data => {

    if (data.error) {
        alert("Error: " + data.error);
        return;
    }

    cargarGrupos(data.grupos);
})
.catch(err => {
    console.error("Error de conexión:", err);
});

function cargarGrupos(lista) {
    const tabla = document.getElementById("tablaGrupos");
    tabla.innerHTML = "";

    lista.forEach(g => {
        const fila = document.createElement("tr");

        fila.innerHTML = `
            <td>${g.nombre}</td>
            <td>
                <button class="btn-tabla" onclick="consultarGrupo('${g.nombre}')">
                    Consultar
                </button>
            </td>
            <td>
                <button class="btn-tabla" onclick="realizarGrupo('${g.nombre}')">
                    Realizar
                </button>
            </td>
        `;

        tabla.appendChild(fila);
    });
}

function consultarGrupo(nombre) {
    alert("Consultando grupo: " + nombre);
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
