document.addEventListener("DOMContentLoaded", async () => {

    // === 1. Tomar id del estudiante pasado desde la pantalla anterior ===
    const idEstudiante = localStorage.getItem("id_estudiante");

    if (!idEstudiante) {
        alert("Falta id_estudiante");
        return;
    }

    try {
        console.log("ID", idEstudiante)

        const resp = await fetch("http://127.0.0.1:8000/api/listEvaluacionEstudiante/", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`
            },
            body: JSON.stringify({ id_estudiante: idEstudiante })
        });

        const data = await resp.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        // === 2. Título ===
        document.querySelector(".evaluacion-titulo").innerHTML =
            `Evaluación de ${data.estudiante}`;

        // === 3. Llenar tabla ===
        const tabla = document.getElementById("tablaEvaluaciones");
        tabla.innerHTML = "";

        const opciones = [
            "Por evaluar",
            "Realizado",
            "En progreso",
            "No realizado"
        ];

        data.evaluaciones.forEach((ev, index) => {

            const tr = document.createElement("tr");

            // === Agregar id_evaluacion y id_logro como atributos y clase ===
            tr.classList.add("fila-evaluacion");
            tr.dataset.evaluacionId = ev.id_evaluacion;
            tr.dataset.logroId = ev.id_logro;

            tr.innerHTML = `
                <td>${ev.logro}</td>
                <td class="descripcion">${ev.descripcion}</td>

                ${["corte1","corte2","corte3"].map(c => `
                    <td>
                        <select name="${c}_${index}" class="select-evaluacion">
                            ${opciones.map(opt => `
                                <option ${opt === ev[c] ? "selected" : ""}>
                                    ${opt}
                                </option>
                            `).join("")}
                        </select>
                    </td>
                `).join("")}
            `;

            tabla.appendChild(tr);
        });

    } catch (err) {
        console.error(err);
        alert("Error al cargar evaluaciones");
    }

});