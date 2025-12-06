const tabla = document.getElementById("tablaPeriodos");
const btnVolver = document.getElementById("btnVolver");

const id_est = localStorage.getItem("id_estudiante_boletin");
console.log("ID estudiante recibido:", id_est);
const nombre_est = localStorage.getItem("nombre_estudiante_boletin");

document.getElementById("nombreEstudiante").innerText = nombre_est;


// Cargar boletines reales
fetch("http://127.0.0.1:8000/api/listadoBoletinesEstudiante/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    },
    body: JSON.stringify({ id_persona: id_est })
})
.then(resp => resp.json())
.then(data => {
    if (data.boletines.length === 0) {
        tabla.innerHTML = `
            <tr><td colspan="2">El estudiante no tiene boletines disponibles</td></tr>
        `;
        return;
    }

    cargarPeriodos(data.boletines);
})
.catch(err => {
    tabla.innerHTML = `
        <tr><td colspan="2">Error cargando boletines</td></tr>
    `;
});

// Render dinámico de periodos
function cargarPeriodos(lista) {
    tabla.innerHTML = "";

    lista.forEach(p => {
        const fila = document.createElement("tr");

        fila.innerHTML = `
            <td>${p.periodo}</td>
            <td>
                <button class="btn-ver-boletin" onclick="descargarBoletin(${p.id_boletin})">Descargar</button>
            </td>
        `;

        tabla.appendChild(fila);
    });
}

btnVolver.addEventListener("click", () => {
    window.location.href = "../vista_boletines/boletines.html";
});
