// Datos de prueba (luego vendrán del backend)
const estudiantesDemo = [
    { nombre: "Pepito Perez" },
    { nombre: "Juan Carlos" }
];

const tabla = document.getElementById("tablaBoletines");

// Render dinámico de la tabla
function cargarBoletines(lista) {
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

// Acción del botón VER
function verBoletin(nombre) {
    // Luego abrirás un PDF o una vista interna
    alert("Mostrando boletín de: " + nombre);
}

// Render inicial
cargarBoletines(estudiantesDemo);
