function descargarBoletin(id_boletin) {
    const id_persona = localStorage.getItem("id_estudiante_boletin");

    fetch(`${API_BASE_URL}/api/descargar-boletin/`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id_boletin: id_boletin,
            id_persona: id_persona
        })
    })
        .then(resp => {
            if (!resp.ok) {
                throw new Error(`Error HTTP ${resp.status}`);
            }
            return resp.blob();
        })
        .then(blob => {
            if (blob.size === 0) {
                throw new Error("El archivo PDF está vacío.");
            }

            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `boletin_${id_boletin}.pdf`;
            a.click();
        })
        .catch(err => {
            showMessage("Error al descargar PDF", "error");
        });
}
