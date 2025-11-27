window.validarAcceso = function(rolPermitido) {
    const token = localStorage.getItem("access_token");
    const role  = localStorage.getItem("role");

    if (!token || role !== rolPermitido) {
        window.location.href = "../../login/login.html";
    }
};
