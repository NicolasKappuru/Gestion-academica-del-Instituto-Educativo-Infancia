document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

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
    console.log("Usuario autenticado:", data.username);
  } else {
    msg.textContent = data.error;
    msg.style.color = "red";
  }
});
