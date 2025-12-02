document.addEventListener("DOMContentLoaded", async () => {

    const username = localStorage.getItem("username");

    if (!username) {
        alert("No hay usuario en sesión");
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
            alert(data.error);
            return;
        }

        // Cambiar el título del grupo
        document.querySelector(".titulo-seccion").innerHTML = `
            Lista de estudiantes<br>
            grupo ${data.grupo}
        `;

        // Llenar la tabla
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

        document.querySelectorAll(".btn-evaluar").forEach(btn => {
            btn.addEventListener("click", () => {
                const idEstudiante = btn.getAttribute("data-id");
                
                // Guardamos el id en localStorage
                localStorage.setItem("id_estudiante", idEstudiante);

                // Redirigimos a la página de evaluación
                window.location.href = "../evaluacion_estudiante/evaluacion_estudiante.html";
            });
        });

    } catch (error) {
        console.error("Error:", error);
        alert("Error de conexión");
    }

});
