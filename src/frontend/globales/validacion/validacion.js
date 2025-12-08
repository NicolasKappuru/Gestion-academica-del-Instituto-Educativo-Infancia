window.validarAcceso = function (rolPermitido) {
    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("role");

    if (!token) {
        window.location.href = "../../login/login.html";
        return;
    }

    if (Array.isArray(rolPermitido)) {
        if (!rolPermitido.includes(role)) {
            window.location.href = "../../login/login.html";
        }
    } else {
        if (role !== rolPermitido) {
            window.location.href = "../../login/login.html";
        }
    }
};
