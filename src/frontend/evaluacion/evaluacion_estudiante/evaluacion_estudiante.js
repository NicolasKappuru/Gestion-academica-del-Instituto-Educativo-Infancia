/***************************************************
 *  SIMULACIÓN DE DATOS (luego lo reemplazas)
 ***************************************************/
const dataEvaluaciones = [
  {
    categoria: "Logro 1",
    descripcion: "Descripción 1",
    corte1: "Por evaluar",
    corte2: "Realizado",
    corte3: "En progreso",
  },
  {
    categoria: "Logro 2",
    descripcion: "Descripción 2",
    corte1: "No realizado",
    corte2: "Por calificar",
    corte3: "Por asignar",
  },
  {
    categoria: "Logro 3",
    descripcion: "Descripción 3",
    corte1: "Por asignar",
    corte2: "En progreso",
    corte3: "Realizado",
  },
];

/***************************************************
 *  OPCIONES DE EVALUACIÓN
 ***************************************************/
const opciones = [
  "Por evaluar",
  "Realizado",
  "En progreso",
  "No realizado",
];

/***************************************************
 *  CARGAR TABLA
 ***************************************************/
const tbody = document.getElementById("tablaEvaluaciones");

dataEvaluaciones.forEach((item, index) => {
  const tr = document.createElement("tr");

  tr.innerHTML = `
    <td>${item.categoria}</td>
    <td>${item.descripcion}</td>
    ${[item.corte1, item.corte2, item.corte3]
      .map(
        (valor, corteIndex) => `
      <td>
        <select name="corte${corteIndex + 1}_${index}" class="select-evaluacion">
          ${opciones
            .map(
              (opt) => `
              <option value="${opt}" ${opt === valor ? "selected" : ""}>
                ${opt}
              </option>
            `
            )
            .join("")}
        </select>
      </td>
    `
      )
      .join("")}
  `;

  tbody.appendChild(tr);
});

/***************************************************
 *  SUBMIT
 ***************************************************/
const form = document.getElementById("formEvaluacionEstudiante");

form.addEventListener("submit", (e) => {
  e.preventDefault();

  // Ejemplo de cómo tomar los datos
  const formData = new FormData(form);

  // Aquí haces tu POST a Django
  console.log("DATOS A ENVIAR:");
  for (let [key, value] of formData.entries()) {
    console.log(key, value);
  }

  // TODO:
  // fetch("/api/guardarEvaluaciones/...", { method:"POST", body:formData })
});
