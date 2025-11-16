// Datos de prueba (luego vendrá del backend)
const periodosDemo = [
    { periodo: "2025-1" },
    { periodo: "2024-3" },
    { periodo: "2024-2" }
];

const tabla = document.getElementById("tablaPeriodos");
const btnVolver = document.getElementById("btnVolver");

// Render dinámico de periodos
function cargarPeriodos(lista) {
    tabla.innerHTML = "";

    lista.forEach(p => {
        const fila = document.createElement("tr");

        fila.innerHTML = `
            <td>${p.periodo}</td>
            <td>
                <button class="btn-ver-boletin" onclick="verBoletinPeriodo('${p.periodo}')">Ver</button>
            </td>
        `;

        tabla.appendChild(fila);
    });
}

// Acción al pulsar "Ver"
function verBoletinPeriodo(periodo) {
    alert("Abrir boletín del periodo: " + periodo);
    // Aquí luego cargarás PDF o vista detallada
}

// Acción volver
btnVolver.addEventListener("click", () => {
    window.history.back();
});

// Render inicial
cargarPeriodos(periodosDemo);
