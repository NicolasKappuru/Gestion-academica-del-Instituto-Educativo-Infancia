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
    const msg = document.getElementById("message");

    if (response.ok) {
      msg.textContent = "Inicio de sesión exitoso.";
      msg.style.color = "green";

      // ✅ Guardamos los tokens y el usuario
      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);
      localStorage.setItem("username", data.username);

      console.log("Token guardado:", data.access);

      // ✅ Redirigimos al index.html después de 1 segundo
      setTimeout(() => {
        window.location.href = "../index.html";
      }, 1000);
    } else {
      msg.textContent = data.error || "Error en el inicio de sesión.";
      msg.style.color = "red";
    }
  } catch (error) {
    console.error("Error:", error);
  }
});
