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

  // Determinar redirección por rol - Solo para login/exito
  getRedirectUrl() {
    const base = window.location.origin;
    const role = localStorage.getItem("role");

    // Fix paths for deployment (removing src/frontend legacy)
    const rutas = {
      profesor: `${base}/evaluacion/vista_profesor/vista_profesor.html`,
      administrador_academico: `${base}/academico/vista_admin_academico/vista_admin_academico.html`,
      administrador_usuarios: `${base}/usuarios/vista_admin_usuarios/vista_admin_usuarios.html`
    };

    // ruta por defecto (main)
    return rutas[role] || `${base}/interfaz_inicial/main.html`;
  },

  // Registrar fallo
  fallo() {
    const nuevoValor = this.getContador() + 1;
    this.setContador(nuevoValor);
    console.log("Intentos fallidos:", this.getContador());

    if (nuevoValor > this.maxIntentos) {
      this.setContador(0);

      showMessage("Intentos agotados. Intente más tarde.", "error");

      setTimeout(() => {
        // Force redirect to main page on failure, ignoring role
        const base = window.location.origin;
        window.location.href = `${base}/interfaz_inicial/main.html`;
      }, 3000); // 3 seconds delay
    }
  },

  // Registrar éxito
  exito() {
    this.reset();
  }
};
