// generarBoletin.js

document.addEventListener("DOMContentLoaded", () => {

    // ===== Buscar botón =====
    const botonesPosibles = ["btnGuardar", "btnGuardarBoletin", "btnGuardarBoletines", "btn-guardar"];
    let btnGuardar = null;

    for (let id of botonesPosibles) {
        const el = document.getElementById(id);
        if (el) {
            btnGuardar = el;
            break;
        }
    }

    if (!btnGuardar) {
        btnGuardar = document.querySelector(".btn-guardar");
    }

    if (!btnGuardar) {
        console.error("⚠️ No se encontró botón para guardar.");
        return;
    }

    // ===== Evento click =====
    btnGuardar.addEventListener("click", async () => {

        console.log("🔥 Guardando boletín...");

        const username = localStorage.getItem("username");
        const idEstudiante = localStorage.getItem("id_estudiante");

        if (!username || !idEstudiante) {
            alert("No hay usuario ni estudiante en localStorage");
            return;
        }

        // ===== Leer datos de la tabla =====
        const filas = document.querySelectorAll("#tablaEvaluaciones tr");
        const evaluaciones = [];

        filas.forEach((fila, index) => {
            const selects = fila.querySelectorAll(".select-evaluacion");
            if (selects.length === 0) return; // ignorar filas sin select

            const evaluacionObj = {
                id_evaluacion: fila.dataset.evaluacionId,
                id_logro: fila.dataset.logroId
            };

            selects.forEach(select => {
                const [corte] = select.name.split("_");
                evaluacionObj[corte] = select.value;
            });


            evaluaciones.push(evaluacionObj);

            console.log(`Fila ${index}`, evaluacionObj);
        });

        if (evaluaciones.length === 0) {
            alert("No se encontraron evaluaciones para guardar.");
            return;
        }

        // ===== Preparar payload =====
        const payload = {
            username,
            id_estudiante: idEstudiante,
            evaluaciones
        };
        console.log("📤 Payload a enviar:", payload);

        // ===== Enviar al backend =====
        try {
            const resp = await fetch(`${API_BASE_URL}/api/generarBoletin/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("access_token")}`
                },
                body: JSON.stringify(payload)
            });

            const data = await resp.json();

            console.log("📥 Respuesta del backend:", data);

            if (data.error) {
                alert("❌ Error: " + data.error);
                return;
            }

            alert("✅ Cambios guardados con éxito 🔥");

        } catch (err) {
            console.error("Error al guardar boletín:", err);
            alert("❌ Error al guardar boletín");
        }
    });

});