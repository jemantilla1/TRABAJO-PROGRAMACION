import re

from entidad import EntidadBase
from excepciones import ClienteInvalidError
from logs import log_info, log_error


class Cliente(EntidadBase):
    """Representa a un cliente del sistema Software FJ."""

    def __init__(
        self,
        id_cliente: str,
        nombre: str,
        email: str,
        telefono: str
    ):
        self.__id_cliente = None
        self.__nombre = None
        self.__email = None
        self.__telefono = None

        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

        log_info(
            f"Cliente registrado exitosamente: "
            f"ID={self.__id_cliente}, Nombre={self.__nombre}"
        )

    # =========================================================
    # ID DEL CLIENTE
    # =========================================================

    @property
    def id_cliente(self) -> str:
        return self.__id_cliente

    @id_cliente.setter
    def id_cliente(self, valor: str):
        if (
            not valor
            or not isinstance(valor, str)
            or len(valor.strip()) == 0
        ):
            msg = "El ID del cliente no puede estar vacío."
            log_error(f"Error de validación Cliente: {msg}")
            raise ClienteInvalidError(msg)

        self.__id_cliente = valor.strip()

    # =========================================================
    # NOMBRE DEL CLIENTE
    # =========================================================

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if (
            not valor
            or not isinstance(valor, str)
            or len(valor.strip()) < 2
        ):
            msg = "El nombre del cliente debe tener al menos 2 caracteres."
            log_error(f"Error de validación Cliente: {msg}")
            raise ClienteInvalidError(msg)

        self.__nombre = valor.strip()

    # =========================================================
    # CORREO ELECTRÓNICO
    # =========================================================

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str):
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not valor or not re.match(patron_email, valor):
            msg = f"El formato de correo electrónico '{valor}' es inválido."
            log_error(f"Error de validación Cliente: {msg}")
            raise ClienteInvalidError(msg)

        self.__email = valor.strip()

    # =========================================================
    # TELÉFONO
    # =========================================================

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        if (
            not valor
            or not str(valor).replace("+", "").replace(" ", "").isdigit()
        ):
            msg = (
                f"El número telefónico '{valor}' debe contener "
                "únicamente dígitos válidos."
            )

            log_error(f"Error de validación Cliente: {msg}")
            raise ClienteInvalidError(msg)

        self.__telefono = str(valor).strip()

    # =========================================================
    # OBTENER ID
    # =========================================================

    def obtener_id(self) -> str:
        return self.__id_cliente

    # =========================================================
    # RESUMEN DEL CLIENTE
    # =========================================================

    def obtener_resumen(self) -> str:
        return (
            f"Cliente [{self.__id_cliente}] - "
            f"{self.__nombre} "
            f"({self.__email}, Tel: {self.__telefono})"
        )
