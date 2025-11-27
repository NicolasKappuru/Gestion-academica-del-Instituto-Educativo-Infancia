document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch("http://127.0.0.1:8000/api/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();

    if (response.ok) {
      showMessage("Inicio de sesión exitoso.", "success");

      // ✅ Guardamos los tokens y el usuario
      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);
      localStorage.setItem("username", data.username);
      localStorage.setItem("role", data.role);

      console.log("Token guardado:", data.access);

      setTimeout(() => {

      if (data.role === "acudiente") {
        window.location.href = "../boletines/vista_boletines/boletines.html";

      } else if (data.role === "profesor") {
        window.location.href = "../evaluacion/vista_profesor/vista_profesor.html";

      } else if (data.role === "administrador_academico") {
        window.location.href = "../academico/vista_admin_academico/vista_admin_academico.html";

      } else if (data.role === "administrador_usuarios") {
        window.location.href = "../usuarios/vista_admin_usuarios/vista_admin_usuarios.html";

      } else {
        // por si ocurre algo inesperado, enviarlo al index
        window.location.href = "../index.html";
      }

    }, 500);

    } else {
        showMessage(data.error || "Error en el inicio de sesión.");
    }
  } catch (error) {
    console.error("Error:", error);
    showMessage("Error al conectar con el servidor.");
  }
});
