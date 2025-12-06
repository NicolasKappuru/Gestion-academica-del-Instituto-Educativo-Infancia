document.addEventListener("DOMContentLoaded", () => {
  const loginLink = document.querySelector(".login-link");

  if (!loginLink) return;

  const token = localStorage.getItem("access_token");

  if (token) {
    // Usuario autenticado → mostrar Cerrar sesión
    loginLink.textContent = "Cerrar sesión";
    loginLink.href = "#"; // para evitar que vaya al login
    loginLink.addEventListener("click", handleLogout);
  } else {
    // Usuario NO autenticado → mostrar Iniciar sesión
    loginLink.textContent = "Iniciar sesión";
    loginLink.href = "../login/login.html";
  }
});

function handleLogout() {
  // Borrar tokens y usuario
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("username");
  localStorage.removeItem("role");

  // Redirigir al login
  window.location.href = "../../login/login.html";
}
