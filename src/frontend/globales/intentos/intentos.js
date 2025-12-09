window.Intentos = {
  maxIntentos: 3,

  // Obtener contador
  getContador() {
    return parseInt(localStorage.getItem("intentos") || "0", 10);
  },

  // Guardar contador
  setContador(valor) {
    localStorage.setItem("intentos", valor.toString());
  },

  // Reset a cero
  reset() {
    this.setContador(0);
  },

  // Determinar redirección por rol
  getRedirectUrl() {
    const base = window.location.origin; // ej. "http://127.0.0.1:5500"
    const role = localStorage.getItem("role");

    const rutas = {
      profesor: `${base}/src/frontend/evaluacion/vista_profesor/vista_profesor.html`,
      administrador_academico: `${base}/src/frontend/academico/vista_admin_academico/vista_admin_academico.html`,
      administrador_usuarios: `${base}/src/frontend/usuarios/vista_admin_usuarios/vista_admin_usuarios.html`
    };

    // ruta por defecto (main)
    return rutas[role] || `${base}/src/frontend/interfaz_inicial/main.html`;
  },

  // Registrar fallo
  fallo() {
    const nuevoValor = this.getContador() + 1;
    this.setContador(nuevoValor);
    console.log(this.getContador())

    if (nuevoValor > this.maxIntentos) {
      this.setContador(0);

      showMessage("Intentos agotados. Intente más tarde.", "error");

      setTimeout(() => {
        window.location.href = this.getRedirectUrl();
      }, 1200);
    }
  },

  // Registrar éxito
  exito() {
    this.reset();
    console.log(this.getContador())

  }
};
