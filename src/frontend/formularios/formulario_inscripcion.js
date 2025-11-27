document.addEventListener("DOMContentLoaded", () => {
  const btnEnviar = document.getElementById("btnEnviar");

  // Crear contenedor para mensajes
  const msgBox = document.createElement("div");
  msgBox.className = "msg-box";
  document.body.appendChild(msgBox);

  // Función para mostrar mensajes en pantalla
  const showMessage = (texto, tipo = "error") => {
    msgBox.textContent = texto;
    msgBox.className = `msg-box ${tipo}`;
    msgBox.style.display = "block";
    setTimeout(() => (msgBox.style.display = "none"), 3000);
  };

  // Función para capitalizar texto (primera letra mayúscula)
  const capitalize = (str) =>
    str
      .toLowerCase()
      .replace(/\b\w/g, (c) => c.toUpperCase())
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, ""); // elimina acentos

  // Verificaciones
  const isOnlyLetters = (str) => /^[A-Za-z\s]+$/.test(str);
  const isOnlyNumbers = (str) => /^[0-9]+$/.test(str);
  const isValidEmail = (str) => /^[\w.-]+@[A-Za-z]+\.[A-Za-z]{2,}$/.test(str);

  btnEnviar.addEventListener("click", (e) => {
    e.preventDefault();

    // Obtener valores
    const acudiente = {
      primerNombre: document.getElementById("nombreAcudiente1").value.trim(),
      segundoNombre: document.getElementById("nombreAcudiente2").value.trim(),
      primerApellido: document.getElementById("apellidoAcudiente1").value.trim(),
      segundoApellido: document.getElementById("apellidoAcudiente2").value.trim(),
      correo: document.getElementById("correoAcudiente").value.trim(),
      cedula: document.getElementById("cedulaAcudiente").value.trim(),
      autorizo: document.getElementById("autorizo").checked,
    };

    const infante = {
      primerNombre: document.getElementById("nombreInfante1").value.trim(),
      segundoNombre: document.getElementById("nombreInfante2").value.trim(),
      primerApellido: document.getElementById("apellidoInfante1").value.trim(),
      segundoApellido: document.getElementById("apellidoInfante2").value.trim(),
      fechaNacimiento: document.getElementById("fechaNacimiento").value,
      grado: document.getElementById("grado").value,
    };

    // === VALIDACIONES ===
    // 1. Campos vacíos obligatorios
    if (
      !acudiente.primerNombre ||
      !acudiente.primerApellido ||
      !acudiente.correo ||
      !acudiente.cedula ||
      !infante.primerNombre ||
      !infante.primerApellido ||
      !infante.fechaNacimiento ||
      !infante.grado
    ) {
      showMessage("Por favor, completa todos los campos obligatorios.");
      return;
    }

    // 2. Autorización
    if (!acudiente.autorizo) {
      showMessage("Debes autorizar el uso de datos personales.");
      return;
    }

    // 3. Validar solo letras en nombres/apellidos
    const nombresYApellidos = [
      acudiente.primerNombre,
      acudiente.segundoNombre,
      acudiente.primerApellido,
      acudiente.segundoApellido,
      infante.primerNombre,
      infante.segundoNombre,
      infante.primerApellido,
      infante.segundoApellido,
    ].filter(Boolean);

    if (!nombresYApellidos.every(isOnlyLetters)) {
      showMessage("Solo se permiten letras en los campos de nombre y apellido.");
      return;
    }

    // 4. Validar correo electrónico
    if (!isValidEmail(acudiente.correo)) {
      showMessage("Ingrese un correo electrónico válido.");
      return;
    }

    // 5. Validar cédula (solo números)
    if (!isOnlyNumbers(acudiente.cedula)) {
      showMessage("La cédula solo debe contener números.");
      return;
    }

    // 6. Validar edad del infante (entre 2 y 4 años)
    const fechaNacimiento = new Date(infante.fechaNacimiento);
    const hoy = new Date();

    // Calcular edad exacta
    let edad = hoy.getFullYear() - fechaNacimiento.getFullYear();
    const mesDiff = hoy.getMonth() - fechaNacimiento.getMonth();
    const diaDiff = hoy.getDate() - fechaNacimiento.getDate();
    if (mesDiff < 0 || (mesDiff === 0 && diaDiff < 0)) edad--;

    // Validar rango entre 2 y 4 años
    if (edad < 2 || edad > 4) {
    showMessage("El infante debe tener entre 2 y 4 años de edad.");
    return;
    }

    // Transformar nombres a mayúsculas con formato capitalizado
    acudiente.primerNombre = capitalize(acudiente.primerNombre);
    acudiente.segundoNombre = capitalize(acudiente.segundoNombre);
    acudiente.primerApellido = capitalize(acudiente.primerApellido);
    acudiente.segundoApellido = capitalize(acudiente.segundoApellido);
    infante.primerNombre = capitalize(infante.primerNombre);
    infante.segundoNombre = capitalize(infante.segundoNombre);
    infante.primerApellido = capitalize(infante.primerApellido);
    infante.segundoApellido = capitalize(infante.segundoApellido);

    (async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/formularioInscripcion/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            primerNombreAcudiente: acudiente.primerNombre,
            segundoNombreAcudiente: acudiente.segundoNombre,
            primerApellidoAcudiente: acudiente.primerApellido,
            segundoApellidoAcudiente: acudiente.segundoApellido,
            correoAcudiente: acudiente.correo,
            cedulaAcudiente: acudiente.cedula,
            primerNombreInfante: infante.primerNombre,
            segundoNombreInfante: infante.segundoNombre,
            primerApellidoInfante: infante.primerApellido,
            segundoApellidoInfante: infante.segundoApellido,
            fechaInfante: infante.fechaNacimiento,
            grado_aplicado: infante.grado
          }),
        });

        const data = await response.json();

        if (response.ok) {
          showMessage("Formulario enviado correctamente ✅", "success");
          console.log("Respuesta del servidor:", data);
        } else {
          showMessage("Error al enviar el formulario. " + (data.error || ""), "error");
        }

      } catch (error) {
        showMessage("Error de conexión con el servidor.", "error");
        console.error(error);
      }
    })();


    console.log("=== Datos del acudiente ===");
    console.log(acudiente);
    console.log("=== Datos del infante ===");
    console.log(infante);

    showMessage("Formulario enviado correctamente ✅", "success");
  });
});


