validarAcceso("administrador_usuarios");

document.addEventListener("DOMContentLoaded", () => {

    const btnCrear = document.getElementById("btnCrear");
    const btnVolver = document.getElementById("btnVolver");


    const isOnlyNumbers = (str) => /^[0-9]+$/.test(str);
    const isValidEmail = (str) => /^[\w.-]+@[A-Za-z]+\.[A-Za-z]{2,}$/.test(str);
    
    // Mapa para convertir el texto del select al rol de la BD
    const ROLES_MAP = {
        "Profesor": "profesor",
        "Administrador académico": "administrador_academico",
        "Administrador de usuarios": "administrador_usuarios"
    };

    btnVolver.addEventListener("click", () => {
        window.location.href = "../vista_admin_usuarios/vista_admin_usuarios.html";
    });

    btnCrear.addEventListener("click", async () => {
        const rolTexto = document.getElementById("inputRol").value;
        const email = document.getElementById("inputCorreo").value;
        const nit = document.getElementById("inputNIT").value;

        if (!rolTexto || !email || !nit) {
            showMessage("Debe llenar todos los campos.", "error");
            return;
        }

        if (!isValidEmail(email)) {
        showMessage("Ingrese un correo electrónico válido.", "error");
        return;
        }

        if (!isOnlyNumbers(nit)) {
        showMessage("La cédula solo debe contener números.", "error");
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
                showMessage(data.error || "No se pudo crear el usuario", "error");
                return;
            }

            showMessage("Usuario creado correctamente", "success");

            // Limpiar inputs
            document.getElementById("inputRol").value = "";
            document.getElementById("inputCorreo").value = "";
            document.getElementById("inputNIT").value = "";

        } catch (error) {
            showMessage("Error en la conexión con el servidor.", "error");
            console.log(error);
        }
    });

});
