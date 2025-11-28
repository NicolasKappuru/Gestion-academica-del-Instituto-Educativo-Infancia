// Habilitar / Deshabilitar Usuario
export async function cambiarEstado(idUser) {
    try {
        const token = localStorage.getItem("access_token");

        await fetch("http://localhost:8000/api/habilitarDeshabilitar/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ id_user: idUser })
        });

    } catch (error) {
        console.error("Error al cambiar estado:", error);
    }
}