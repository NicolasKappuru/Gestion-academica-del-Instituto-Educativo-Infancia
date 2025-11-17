document.addEventListener("DOMContentLoaded", () => {

    // Datos de prueba — luego los reemplazas por tu fetch()
    const estudiantes = [
        { nombre: "Pepito Perez" },
        { nombre: "Juan Carlos" },
        { nombre: "Maria Gomez" }
    ];

    const tabla = document.getElementById("tablaEstudiantes");

    estudiantes.forEach(est => {
        const fila = document.createElement("tr");

        fila.innerHTML = `
            <td>${est.nombre}</td>
            <td><button class="btn-evaluar">Evaluar</button></td>
        `;

        tabla.appendChild(fila);
    });

});
