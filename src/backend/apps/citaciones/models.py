
class Citacion: 
    def __init__(self, nombre_acudiente, apellido_acudiente, correo_acudiente, 
                 nombre_acudido, apellido_acudido, fecha_cita, hora_cita, 
                 lugar_cita, tipo_cita, motivo, administrador=None):
        self._nombre_acudiente = nombre_acudiente
        self._apellido_acudiente = apellido_acudiente
        self._correo_acudiente = correo_acudiente
        self._nombre_acudido = nombre_acudido
        self._apellido_acudido = apellido_acudido
        self._fecha_cita = fecha_cita
        self._hora_cita = hora_cita
        self._lugar_cita = lugar_cita
        self._tipo_cita = tipo_cita
        self._motivo = motivo
        self._administrador = administrador

    def __str__(self):
        return f"Citacion para {self._nombre_acudiente} - {self._fecha_cita}"

    # ===========================
    #          GETTERS
    # ===========================
    def get_nombre_acudiente(self):
        return self._nombre_acudiente

    def get_apellido_acudiente(self):
        return self._apellido_acudiente

    def get_correo_acudiente(self):
        return self._correo_acudiente

    def get_nombre_acudido(self):
        return self._nombre_acudido

    def get_apellido_acudido(self):
        return self._apellido_acudido

    def get_fecha_cita(self):
        return self._fecha_cita

    def get_hora_cita(self):
        return self._hora_cita

    def get_lugar_cita(self):
        return self._lugar_cita

    def get_tipo_cita(self):
        return self._tipo_cita

    def get_motivo(self):
        return self._motivo

    def get_administrador(self):
        return self._administrador

    # ===========================
    #          SETTERS
    # ===========================
    def set_nombre_acudiente(self, value):
        self._nombre_acudiente = value

    def set_apellido_acudiente(self, value):
        self._apellido_acudiente = value

    def set_correo_acudiente(self, value):
        self._correo_acudiente = value

    def set_nombre_acudido(self, value):
        self._nombre_acudido = value

    def set_apellido_acudido(self, value):
        self._apellido_acudido = value

    def set_fecha_cita(self, value):
        self._fecha_cita = value

    def set_hora_cita(self, value):
        self._hora_cita = value

    def set_lugar_cita(self, value):
        self._lugar_cita = value

    def set_tipo_cita(self, value):
        self._tipo_cita = value

    def set_motivo(self, value):
        self._motivo = value

    def set_administrador(self, value):
        self._administrador = value
