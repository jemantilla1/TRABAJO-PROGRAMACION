from entidad import EntidadBase
from cliente import Cliente
from servicio import Servicio, ReservaSalas
from excepciones import (
    ReservaInvalidError,
    ServicioNoDisponibleError,
    CapacidadExcedidaError,
    CalculoInconsistenteError
)
from logs import log_info, log_warning, log_error


class Reserva(EntidadBase):
    """Representa una reserva de servicio realizada por un cliente."""

    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion_horas: float,
        asistentes: int = 1
    ):
        if not id_reserva or len(id_reserva.strip()) == 0:
            raise ReservaInvalidError("El ID de la reserva es obligatorio.")

        if not isinstance(cliente, Cliente):
            raise ReservaInvalidError("La reserva requiere un objeto Cliente válido.")

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidError("La reserva requiere un objeto Servicio válido.")

        if duracion_horas <= 0:
            raise CalculoInconsistenteError(
                "La duración de la reserva debe ser estrictamente mayor a 0 horas."
            )

        self.__id_reserva = id_reserva.strip()
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion_horas = float(duracion_horas)
        self.__asistentes = int(asistentes)
        self.__estado = "PENDIENTE"

        self._validar_disponibilidad_y_capacidad()

        log_info(
            f"Reserva creada [PENDIENTE]: ID={self.__id_reserva}, "
            f"Cliente={cliente.nombre}, Servicio={servicio.nombre}"
        )

    # =========================================================
    # PROPIEDADES
    # =========================================================

    @property
    def id_reserva(self) -> str:
        return self.__id_reserva

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @property
    def servicio(self) -> Servicio:
        return self.__servicio

    @property
    def duracion_horas(self) -> float:
        return self.__duracion_horas

    @property
    def estado(self) -> str:
        return self.__estado

    # =========================================================
    # VALIDACIÓN DE DISPONIBILIDAD Y CAPACIDAD
    # =========================================================

    def _validar_disponibilidad_y_capacidad(self):
        """Valida que el servicio esté disponible y que la capacidad no sea excedida."""

        try:
            if not self.__servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self.__servicio.nombre}' "
                    "se encuentra actualmente NO DISPONIBLE."
                )

            if isinstance(self.__servicio, ReservaSalas):
                if self.__asistentes > self.__servicio.capacidad_maxima:
                    raise ValueError(
                        f"Asistentes ({self.__asistentes}) supera capacidad "
                        f"de sala ({self.__servicio.capacidad_maxima})."
                    )

        except ValueError as e:
            msg = (
                f"Capacidad excedida en la sala de reuniones "
                f"para la reserva {self.__id_reserva}."
            )

            log_error(msg, exc=e)
            raise CapacidadExcedidaError(msg) from e

        except ServicioNoDisponibleError as e:
            log_error(
                f"Error de disponibilidad en reserva {self.__id_reserva}: {e}"
            )
            raise

    # =========================================================
    # CONFIRMAR RESERVA
    # =========================================================

    def confirmar_reserva(self) -> bool:
        """Confirma la reserva aplicando bloque try/except/else/finally."""

        recurso_liberado = False

        try:
            log_info(
                f"Intentando confirmar reserva {self.__id_reserva}..."
            )

            if self.__estado != "PENDIENTE":
                raise ReservaInvalidError(
                    f"No se puede confirmar la reserva {self.__id_reserva} "
                    f"pues su estado actual es '{self.__estado}'."
                )

            self._validar_disponibilidad_y_capacidad()

        except (
            ReservaInvalidError,
            ServicioNoDisponibleError,
            CapacidadExcedidaError
        ) as exc:
            log_error(
                f"Fallo al confirmar la reserva {self.__id_reserva}: {exc}"
            )
            raise

        else:
            self.__estado = "CONFIRMADA"

            log_info(
                f"Reserva {self.__id_reserva} CONFIRMADA con éxito."
            )

            return True

        finally:
            recurso_liberado = True

            log_info(
                f"Finalizado proceso de confirmación de reserva "
                f"{self.__id_reserva}. "
                f"(Recursos auditados: {recurso_liberado})"
            )

    # =========================================================
    # CANCELAR RESERVA
    # =========================================================

    def cancelar_reserva(
        self,
        motivo: str = "Solicitud del cliente"
    ) -> bool:
        """Cancela la reserva cambiando su estado."""

        if self.__estado in ["PROCESADA", "CANCELADA"]:
            msg = (
                f"No es posible cancelar la reserva {self.__id_reserva} "
                f"en estado '{self.__estado}'."
            )

            log_warning(msg)
            raise ReservaInvalidError(msg)

        self.__estado = "CANCELADA"

        log_info(
            f"Reserva {self.__id_reserva} CANCELADA. Motivo: {motivo}"
        )

        return True

    # =========================================================
    # PROCESAR RESERVA
    # =========================================================

    def procesar_reserva(self) -> bool:
        """Procesa y ejecuta la reserva para cerrar el ciclo."""

        if self.__estado != "CONFIRMADA":
            msg = (
                f"La reserva {self.__id_reserva} debe estar CONFIRMADA "
                f"antes de ser procesada. Estado actual: '{self.__estado}'."
            )

            log_error(msg)
            raise ReservaInvalidError(msg)

        self.__estado = "PROCESADA"

        log_info(
            f"Reserva {self.__id_reserva} PROCESADA satisfactoriamente."
        )

        return True

    # =========================================================
    # CÁLCULO DEL COSTO TOTAL
    # =========================================================

    def calcular_costo_total(
        self,
        descuento: float = 0.0,
        impuesto: float = 0.19
    ) -> float:
        """Calcula el costo total incluyendo impuestos y posibles descuentos."""

        if descuento < 0 or descuento > 1.0:
            raise CalculoInconsistenteError(
                "El descuento debe ser un valor decimal entre 0.0 y 1.0."
            )

        if impuesto < 0:
            raise CalculoInconsistenteError(
                "El impuesto no puede ser negativo."
            )

        costo_subtotal = self.__servicio.calcular_costo(
            self.__duracion_horas,
            asistentes=self.__asistentes
        )

        costo_con_descuento = costo_subtotal * (1 - descuento)
        costo_final = costo_con_descuento * (1 + impuesto)

        return round(costo_final, 2)

    # =========================================================
    # OBTENER ID
    # =========================================================

    def obtener_id(self) -> str:
        return self.__id_reserva

    # =========================================================
    # RESUMEN DE RESERVA
    # =========================================================

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.__id_reserva}] | "
            f"Estado: {self.__estado} | "
            f"Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | "
            f"Duración: {self.__duracion_horas}h | "
            f"Costo Estimado: ${self.calcular_costo_total()}"
        )
