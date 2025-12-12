validarAcceso("administrador_usuarios");

document.addEventListener("DOMContentLoaded", () => {

    const btnCrear = document.getElementById("btnCrear");
    const btnVolver = document.getElementById("btnVolver");


    const isOnlyNumbers = (str) => /^[0-9]+$/.test(str);
    const isValidEmail = (str) => /^[\w.-]+@[A-Za-z]+\.[A-Za-z]{2,}$/.test(str);
    const isOnlyLetters = (str) => /^[A-Za-z\s]+$/.test(str);
    const capitalize = (str) =>
        str
            .toLowerCase()
            .replace(/\b\w/g, (c) => c.toUpperCase())
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "");

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
        const primerNombre = document.getElementById("inputPrimerNombre").value.trim();
        const segundoNombre = document.getElementById("inputSegundoNombre").value.trim();
        const primerApellido = document.getElementById("inputPrimerApellido").value.trim();
        const segundoApellido = document.getElementById("inputSegundoApellido").value.trim();

        const email = document.getElementById("inputCorreo").value;
        const nit = document.getElementById("inputNIT").value;

        if (!rolTexto || !email || !nit) {
            showMessage("Debe llenar todos los campos.", "error");
            window.Intentos.fallo();
            return;
        }

        if (!isValidEmail(email)) {
            showMessage("Ingrese un correo electrónico válido.", "error");
            window.Intentos.fallo();
            return;
        }

        if (!isOnlyNumbers(nit)) {
            showMessage("La cédula solo debe contener números.", "error");
            window.Intentos.fallo();
            return;
        }

        if (!primerNombre || !primerApellido) {
            showMessage("Debe ingresar al menos primer nombre y primer apellido.", "error");
            window.Intentos.fallo();
            return;
        }

        const nombresYApellidos = [
            primerNombre,
            segundoNombre,
            primerApellido,
            segundoApellido
        ].filter(Boolean);

        if (!nombresYApellidos.every(isOnlyLetters)) {
            showMessage("Solo se permiten letras en los campos de nombre y apellido.", "error");
            window.Intentos.fallo();
            return;
        }

        const pNombre = capitalize(primerNombre);
        const sNombre = capitalize(segundoNombre);
        const pApellido = capitalize(primerApellido);
        const sApellido = capitalize(segundoApellido);


        const role = ROLES_MAP[rolTexto];

        try {
            const response = await fetch(`${API_BASE_URL}/api/crearUsuario/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + localStorage.getItem("access_token")
                },
                body: JSON.stringify({
                    role: role,
                    email: email,
                    nit: nit,
                    primer_nombre: primerNombre,
                    segundo_nombre: segundoNombre,
                    primer_apellido: primerApellido,
                    segundo_apellido: segundoApellido
                })
            });

            const data = await response.json();

            if (!response.ok) {
                showMessage(data.error || "No se pudo crear el usuario", "error");
                window.Intentos.fallo();
                return;
            }

            showMessage("Usuario creado correctamente", "success");
            window.Intentos.exito();


            // Limpiar inputs
            document.getElementById("inputRol").value = "";
            document.getElementById("inputCorreo").value = "";
            document.getElementById("inputNIT").value = "";

        } catch (error) {
            showMessage("Error en la conexión con el servidor.", "error");
            window.Intentos.fallo();
            console.log(error);
        }
    });

});
