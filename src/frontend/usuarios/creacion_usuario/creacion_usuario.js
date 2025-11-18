document.addEventListener("DOMContentLoaded", () => {

    // Botón crear usuario
    document.getElementById("btnCrear").addEventListener("click", () => {
        const rol = document.getElementById("inputRol").value;
        const correo = document.getElementById("inputCorreo").value;
        const nit = document.getElementById("inputNIT").value;

        if (!rol || !correo || !nit) {
            alert("Por favor complete todos los campos.");
            return;
        }

        // Aquí luego conectarás tu API real
        console.log("Creando usuario con:", {
            rol,
            correo,
            nit
        });

        alert("Usuario creado (lógica backend pendiente).");
    });

    // Botón volver ya funciona desde el HTML con window.location.href
});


document.addEventListener("DOMContentLoaded", () => {

    const btnVolver = document.getElementById("btnVolver");

    btnVolver.addEventListener("click", () => {
        window.location.href = "../vista_admin_usuarios/vista_admin_usuarios.html";
    });

});

