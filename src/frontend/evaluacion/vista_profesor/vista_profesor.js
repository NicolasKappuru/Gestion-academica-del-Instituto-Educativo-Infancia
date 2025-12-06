document.addEventListener("DOMContentLoaded", async () => {

    validarAcceso("profesor"); 

    const username = localStorage.getItem("username");

    if (!username) {
        showMessage("No hay usuario en sesión", "error");
        return;
    }

    try {
        const resp = await fetch("http://127.0.0.1:8000/api/listadoEstudiantesGrupo/", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`
            },
            body: JSON.stringify({ username })
        });

        const data = await resp.json();

        if (data.error) {
            showMessage("Error: " + data.error, "error");
            return;
        }

        // === Cambiar título del grupo ===
        document.querySelector(".titulo-seccion").innerHTML = `
            Lista de estudiantes<br>
            grupo ${data.grupo}
        `;

        // === Llenar tabla ===
        const tabla = document.getElementById("tablaEstudiantes");
        tabla.innerHTML = "";

        data.estudiantes.forEach(est => {
            const fila = document.createElement("tr");

            fila.innerHTML = `
                <td>${est.nombre}</td>
                <td><button class="btn-evaluar" data-id="${est.id}">Evaluar</button></td>
            `;

            console.log("enviando id_estudiante:", est.id);

            tabla.appendChild(fila);
        });

        // === Listener de botones ===
        document.querySelectorAll(".btn-evaluar").forEach(btn => {
            btn.addEventListener("click", () => {
                const idEstudiante = btn.getAttribute("data-id");

                // Guardar id en localStorage
                localStorage.setItem("id_estudiante", idEstudiante);

                // Redirigir
                window.location.href = "../evaluacion_estudiante/evaluacion_estudiante.html";
            });
        });

    } catch (error) {
        console.error("Error:", error);
        showMessage("Error de conexión con el servidor", "error");
    }

});
