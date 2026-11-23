import logging
import os


# ==========================================================================
# CONFIGURACIÓN GENERAL
# ==========================================================================

LOG_FILE_PATH = "software_fj_sistema.log"


# ==========================================================================
# CONFIGURACIÓN DEL SISTEMA DE LOGGING
# ==========================================================================

def configurar_logging():
    """Configura el sistema de registro de logs en archivo y consola."""

    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # Handler para archivo
        file_handler = logging.FileHandler(
            LOG_FILE_PATH,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)

        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formato de mensajes
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Aplicar formato a los handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Registrar handlers en el logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


# ==========================================================================
# INICIALIZACIÓN DEL LOGGER
# ==========================================================================

logger = configurar_logging()


# ==========================================================================
# FUNCIONES DE REGISTRO
# ==========================================================================

def log_info(mensaje: str):
    """Registra mensajes informativos."""
    logger.info(mensaje)


def log_warning(mensaje: str):
    """Registra mensajes de advertencia."""
    logger.warning(mensaje)


def log_error(mensaje: str, exc: Exception = None):
    """Registra errores, incluyendo detalles de excepciones si existen."""

    if exc:
        logger.error(
            f"{mensaje} | Detalle Excepción: {exc}",
            exc_info=True
        )
    else:
        logger.error(mensaje)
