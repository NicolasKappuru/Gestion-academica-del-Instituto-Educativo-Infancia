document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("access_token");
  const btnInicio = document.getElementById("btn-inicio");

  if (btnInicio) {
    if (token) {
      // Usuario logueado → ocultar Inicio
      btnInicio.style.display = "none";  
      // Otra opción: btnInicio.href = "#";
    } else {
      // Usuario NO logueado → mostrar Inicio
      btnInicio.style.display = "";
    }
  }
});
