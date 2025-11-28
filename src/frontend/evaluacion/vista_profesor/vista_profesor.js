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
                <td><button class="btn-evaluar">Evaluar</button></td>
            `;

            tabla.appendChild(fila);
        });

    } catch (error) {
        console.error("Error:", error);
        alert("Error de conexión");
    }

});
