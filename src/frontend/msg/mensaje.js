// ============ COMPONENTE GLOBAL DE MENSAJES ============
(function () {
  // Crear contenedor del mensaje si NO existe
  let msgBox = document.getElementById("global-msg-box");

  if (!msgBox) {
    msgBox = document.createElement("div");
    msgBox.id = "global-msg-box";
    msgBox.className = "msg-box";
    document.body.appendChild(msgBox);
  }

  // Hacer accesible la función global
  window.showMessage = function (texto, tipo = "error", duracion = 3000) {
    msgBox.textContent = texto;
    msgBox.className = `msg-box ${tipo}`;
    msgBox.style.display = "block";

    setTimeout(() => {
      msgBox.style.display = "none";
    }, duracion);
  };
})();
