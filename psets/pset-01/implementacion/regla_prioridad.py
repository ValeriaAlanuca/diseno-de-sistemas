from abc import ABC, abstractmethod
from datetime import time

from horario import Horario


class ReglaPrioridad(ABC):
    """Clase abstracta: contrato comun para toda regla de prioridad."""

    @abstractmethod
    def aplica_prioridad(self, horario: Horario) -> bool:
        """Devuelve True si, para el horario dado, el solicitante debe
        recibir prioridad de reserva."""
        raise NotImplementedError


class ReglaPrioridadAntesDe6pm(ReglaPrioridad):
    """Comportamiento 1: aplica prioridad si el horario solicitado
    empieza antes de las 6:00 p.m. (RF-03). Usada por los capitanes de
    equipos oficiales."""

    HORA_LIMITE = time(18, 0)

    def aplica_prioridad(self, horario: Horario) -> bool:
        return horario.hora_inicio < self.HORA_LIMITE


class ReglaSinPrioridad(ReglaPrioridad):
    """Comportamiento 2: nunca aplica prioridad. Es la regla por defecto
    de un estudiante que reserva de forma individual/informal."""

    def aplica_prioridad(self, horario: Horario) -> bool:
        return False
#Valeria Alanuca
#00342425