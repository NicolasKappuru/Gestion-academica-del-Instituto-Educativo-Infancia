function descargarBoletin(id_boletin) {

    const id_persona = localStorage.getItem("id_estudiante_boletin");

    fetch("http://127.0.0.1:8000/api/descargar-boletin/", {
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
    .then(resp => resp.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `boletin_${id_boletin}.pdf`;
        a.click();
    });
}
