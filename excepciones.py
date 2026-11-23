# ==========================================================================
# EXCEPCIÓN BASE DEL SISTEMA
# ==========================================================================

class SoftwareFJError(Exception):
    """Excepción base para todos los errores del sistema Software FJ."""

    def __init__(self, mensaje: str, codigo_error: str = "ERR_GENERICO"):
        super().__init__(mensaje)

        self.mensaje = mensaje
        self.codigo_error = codigo_error

    def __str__(self):
        return f"[{self.codigo_error}] {self.mensaje}"


# ==========================================================================
# EXCEPCIONES RELACIONADAS CON CLIENTES
# ==========================================================================

class ClienteInvalidError(SoftwareFJError):
    """Excepción cuando los datos de un cliente son inválidos o faltantes."""

    def __init__(self, mensaje: str):
        super().__init__(
            mensaje,
            codigo_error="ERR_CLIENTE_INVALIDO"
        )


# ==========================================================================
# EXCEPCIONES RELACIONADAS CON SERVICIOS
# ==========================================================================

class ServicioInvalidError(SoftwareFJError):
    """Excepción cuando un servicio contiene parámetros inválidos."""

    def __init__(self, mensaje: str):
        super().__init__(
            mensaje,
            codigo_error="ERR_SERVICIO_INVALIDO"
        )


class ServicioNoDisponibleError(ServicioInvalidError):
    """Excepción cuando se intenta reservar un servicio no disponible."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje)

        self.codigo_error = "ERR_SERVICIO_NO_DISPONIBLE"


# ==========================================================================
# EXCEPCIONES RELACIONADAS CON RESERVAS
# ==========================================================================

class ReservaInvalidError(SoftwareFJError):
    """Excepción para operaciones de reserva inválidas o fuera de regla de negocio."""

    def __init__(self, mensaje: str):
        super().__init__(
            mensaje,
            codigo_error="ERR_RESERVA_INVALIDA"
        )


class CapacidadExcedidaError(ReservaInvalidError):
    """Excepción cuando el número de asistentes supera la capacidad máxima de la sala."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje)

        self.codigo_error = "ERR_CAPACIDAD_EXCEDIDA"


# ==========================================================================
# EXCEPCIONES RELACIONADAS CON CÁLCULOS
# ==========================================================================

class CalculoInconsistenteError(SoftwareFJError):
    """Excepción para inconsistencias numéricas o de duración en cálculos."""

    def __init__(self, mensaje: str):
        super().__init__(
            mensaje,
            codigo_error="ERR_CALCULO_INCONSISTENTE"
        )
