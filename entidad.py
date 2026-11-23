from abc import ABC, abstractmethod


# ==========================================================================
# CLASE BASE ABSTRACTA DEL SISTEMA
# ==========================================================================

class EntidadBase(ABC):
    """Clase base abstracta que representa cualquier entidad dentro del sistema Software FJ."""

    # ----------------------------------------------------------------------
    # MÉTODOS ABSTRACTOS
    # ----------------------------------------------------------------------

    @abstractmethod
    def obtener_id(self) -> str:
        """Devuelve el identificador único de la entidad."""
        pass

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Devuelve una representación textual resumida de la entidad."""
        pass
