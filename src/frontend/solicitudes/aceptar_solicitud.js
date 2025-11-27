export async function aceptarSolicitud(id_solicitud) {
    try {
        const token = localStorage.getItem("access_token");
        const resp = await fetch("http://localhost:8000/api/aceptarSolicitud/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ id_solicitud })
        });
        const data = await resp.json();
        if (!resp.ok) {
            console.error("Error aceptar:", data);
        }
        return data;
    } catch (err) {
        console.error("Fetch aceptar error:", err);
        return null;
    }
}
