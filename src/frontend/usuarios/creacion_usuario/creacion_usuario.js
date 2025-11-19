document.addEventListener("DOMContentLoaded", () => {

    const btnCrear = document.getElementById("btnCrear");
    const btnVolver = document.getElementById("btnVolver");

    // Mapa para convertir el texto del select al rol de la BD
    const ROLES_MAP = {
        "Acudiente": "acudiente",
        "Profesor": "profesor",
        "Administrador académico": "administrador_academico",
        "Administrador de usuarios": "administrador_usuarios"
    };

    btnVolver.addEventListener("click", () => {
        window.location.href = "../interfaz_admin_usuarios/vista_admin_usuarios.html";
    });

    btnCrear.addEventListener("click", async () => {
        const rolTexto = document.getElementById("inputRol").value;
        const email = document.getElementById("inputCorreo").value;
        const nit = document.getElementById("inputNIT").value;

        if (!rolTexto || !email || !nit) {
            alert("Debe llenar todos los campos.");
            return;
        }

        const role = ROLES_MAP[rolTexto];

        try {
            const response = await fetch("http://127.0.0.1:8000/api/crearUsuario/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + localStorage.getItem("access_token")
                },
                body: JSON.stringify({
                    role: role,
                    email: email,
                    nit: nit
                })
            });

            const data = await response.json();

            if (!response.ok) {
                alert("Error: " + (data.error || "No se pudo crear el usuario"));
                return;
            }

            alert("Usuario creado correctamente");

            // Limpiar inputs
            document.getElementById("inputRol").value = "";
            document.getElementById("inputCorreo").value = "";
            document.getElementById("inputNIT").value = "";

        } catch (error) {
            alert("Error en la conexión con el servidor.");
            console.log(error);
        }
    });

});
