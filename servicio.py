from abc import abstractmethod

from entidad import EntidadBase
from excepciones import ServicioInvalidError, CalculoInconsistenteError
from logs import log_info, log_error


class Servicio(EntidadBase):
    """Clase abstracta para representar los servicios de Software FJ."""

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        tarifa_base: float,
        disponible: bool = True
    ):
        if not id_servicio or len(id_servicio.strip()) == 0:
            raise ServicioInvalidError("El ID del servicio no puede estar vacío.")

        if not nombre or len(nombre.strip()) == 0:
            raise ServicioInvalidError("El nombre del servicio es obligatorio.")

        if tarifa_base is None or tarifa_base < 0:
            raise ServicioInvalidError(
                f"La tarifa base (${tarifa_base}) no puede ser negativa ni nula."
            )

        self._id_servicio = id_servicio.strip()
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

        log_info(
            f"Servicio instanciado: ID={self._id_servicio}, "
            f"Nombre={self._nombre}, TarifaBase=${self._tarifa_base}"
        )

    # =========================================================
    # PROPIEDADES
    # =========================================================

    @property
    def id_servicio(self) -> str:
        return self._id_servicio

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = bool(estado)

        log_info(
            f"Estado del servicio {self._id_servicio} actualizado a: "
            f"disponible={self._disponible}"
        )

    # =========================================================
    # MÉTODOS BASE
    # =========================================================

    def obtener_id(self) -> str:
        return self._id_servicio

    @abstractmethod
    def calcular_costo(self, duracion_horas: float, **kwargs) -> float:
        pass

    @abstractmethod
    def obtener_descripcion(self) -> str:
        pass

    def obtener_resumen(self) -> str:
        estado_str = "Disponible" if self._disponible else "No Disponible"

        return (
            f"Servicio [{self._id_servicio}] - {self._nombre} "
            f"(${self._tarifa_base}/h) - Estado: {estado_str}"
        )


# =============================================================
# SERVICIO DE RESERVA DE SALAS
# =============================================================

class ReservaSalas(Servicio):
    """Servicio de reserva de salas de reuniones/conferencias."""

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        tarifa_base: float,
        capacidad_maxima: int,
        equipamiento_audiovisual: bool = True,
        disponible: bool = True
    ):
        super().__init__(
            id_servicio,
            nombre,
            tarifa_base,
            disponible
        )

        if capacidad_maxima <= 0:
            raise ServicioInvalidError(
                "La capacidad máxima de la sala debe ser "
                "un número entero mayor a 0."
            )

        self.capacidad_maxima = capacidad_maxima
        self.equipamiento_audiovisual = equipamiento_audiovisual

    def calcular_costo(self, duracion_horas: float, **kwargs) -> float:
        if duracion_horas <= 0:
            raise CalculoInconsistenteError(
                "La duración para reserva de sala debe ser mayor a 0 horas."
            )

        costo_base = self._tarifa_base * duracion_horas

        recargo_eq = (
            0.15 if self.equipamiento_audiovisual else 0.0
        )

        asistentes = kwargs.get("asistentes", 1)

        recargo_asistentes = 0.05 if asistentes > 20 else 0.0

        costo_total = costo_base * (
            1 + recargo_eq + recargo_asistentes
        )

        return round(costo_total, 2)

    def obtener_descripcion(self) -> str:
        eq_str = (
            "Con equipos proyector/audio"
            if self.equipamiento_audiovisual
            else "Estándar"
        )

        return (
            f"Reserva de Sala: {self._nombre} "
            f"(Capacidad: {self.capacidad_maxima} pers., {eq_str})"
        )


# =============================================================
# SERVICIO DE ALQUILER DE EQUIPOS
# =============================================================

class AlquilerEquipos(Servicio):
    """Servicio de alquiler de equipos tecnológicos."""

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        tarifa_base: float,
        tipo_equipo: str,
        deposito_garantia: float,
        disponible: bool = True
    ):
        super().__init__(
            id_servicio,
            nombre,
            tarifa_base,
            disponible
        )

        if deposito_garantia < 0:
            raise ServicioInvalidError(
                "El depósito de garantía no puede ser negativo."
            )

        self.tipo_equipo = tipo_equipo
        self.deposito_garantia = deposito_garantia

    def calcular_costo(self, duracion_horas: float, **kwargs) -> float:
        if duracion_horas <= 0:
            raise CalculoInconsistenteError(
                "La duración para alquiler de equipos debe ser mayor a 0 horas."
            )

        dias = duracion_horas / 24.0

        if duracion_horas >= 24:
            costo = (
                self._tarifa_base * 24 * 0.8
            ) * dias
        else:
            costo = self._tarifa_base * duracion_horas

        incluir_deposito = kwargs.get("incluir_deposito", False)

        if incluir_deposito:
            costo += self.deposito_garantia

        return round(costo, 2)

    def obtener_descripcion(self) -> str:
        return (
            f"Alquiler de Equipo ({self.tipo_equipo}): "
            f"{self._nombre} "
            f"(Garantía: ${self.deposito_garantia})"
        )


# =============================================================
# SERVICIO DE ASESORÍA ESPECIALIZADA
# =============================================================

class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría técnica o consultoría en software."""

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        tarifa_base: float,
        consultor: str,
        nivel_especialidad: str,
        disponible: bool = True
    ):
        super().__init__(
            id_servicio,
            nombre,
            tarifa_base,
            disponible
        )

        if not consultor or len(consultor.strip()) == 0:
            raise ServicioInvalidError(
                "El nombre del consultor es obligatorio."
            )

        self.consultor = consultor
        self.nivel_especialidad = nivel_especialidad

    def calcular_costo(self, duracion_horas: float, **kwargs) -> float:
        if duracion_horas <= 0:
            raise CalculoInconsistenteError(
                "La duración de la asesoría especializada "
                "debe ser mayor a 0 horas."
            )

        multiplicadores = {
            "Senior": 1.2,
            "Master": 1.5,
            "Architect": 2.0
        }

        factor = multiplicadores.get(
            self.nivel_especialidad,
            1.0
        )

        costo_base = (
            self._tarifa_base * factor
        ) * duracion_horas

        return round(costo_base, 2)

    def obtener_descripcion(self) -> str:
        return (
            f"Asesoría Especializada: {self._nombre} "
            f"por {self.consultor} [{self.nivel_especialidad}]"
        )
