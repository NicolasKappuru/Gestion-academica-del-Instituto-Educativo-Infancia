// rechazar_solicitud.js
export async function rechazarSolicitud(id_solicitud) {
    try {
        const token = localStorage.getItem("access_token");
        const resp = await fetch("http://localhost:8000/api/solicitud/rechazar/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ id_solicitud })
        });
        const data = await resp.json();
        if (!resp.ok) {
            console.error("Error rechazar:", data);
        }
        return data;
    } catch (err) {
        console.error("Fetch rechazar error:", err);
        return null;
    }
}
