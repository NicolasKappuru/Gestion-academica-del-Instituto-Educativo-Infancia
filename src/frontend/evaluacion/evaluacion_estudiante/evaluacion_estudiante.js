document.addEventListener("DOMContentLoaded", () => {

    // Secuencia de estados
    const estados = ["Por asignar", "Realizado", "En progreso", "No realizado", "Por calificar"];

    // Busca todos los botones de asistencia
    const botones = document.querySelectorAll(".asistencia-btn");

    botones.forEach(btn => {
        btn.addEventListener("click", () => {

            // Estado actual
            const celda = btn.parentElement;
            const estadoActual = celda.getAttribute("data-estado");

            // Calcula el siguiente estado
            let indice = estados.indexOf(estadoActual);
            let siguiente = (indice + 1) % estados.length;

            // Actualiza celda
            celda.setAttribute("data-estado", estados[siguiente]);
            btn.textContent = estados[siguiente];
        });
    });

});
