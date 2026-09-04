from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

LIMITE_CANCELACION = timedelta(hours=2)


class EstadoReserva(Enum):
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    NO_SHOW = "NO_SHOW"
    REASIGNADA = "REASIGNADA"


@dataclass
class CambioEstado:
    """RF-12 / RNF-03: registro individual del historial de una reserva."""
    estado: EstadoReserva
    fecha_hora: datetime

    def __str__(self) -> str:
        return f"{self.estado.value} @ {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"


class Reserva:
    _contador = 0

    def __init__(self, usuario, cancha, horario):
        Reserva._contador += 1
        self.id_reserva = f"R{Reserva._contador:04d}"
        self.usuario = usuario
        self.cancha = cancha
        self.horario = horario
        self.estado: EstadoReserva | None = None
        self.historial: list[CambioEstado] = []

    def confirmar(self, momento: datetime) -> None:
        """RF-01: confirma la reserva recien creada."""
        self.estado = EstadoReserva.CONFIRMADA
        self._registrar_cambio(EstadoReserva.CONFIRMADA, momento)

    def cancelar(self, hora_actual: datetime) -> None:
        """RF-06/RF-07/RF-08: el sistema, no el usuario, decide si la
        cancelacion se registra como CANCELADA o como NO_SHOW, segun el
        tiempo restante hasta el inicio del horario reservado."""
        tiempo_restante = self.horario.inicio_datetime() - hora_actual
        if tiempo_restante < LIMITE_CANCELACION:
            nuevo_estado = EstadoReserva.NO_SHOW
        else:
            nuevo_estado = EstadoReserva.CANCELADA
        self.estado = nuevo_estado
        self._registrar_cambio(nuevo_estado, hora_actual)

    def reasignar(self, momento: datetime) -> None:
        """RF-04/RF-11: usada cuando el Administrador resuelve un
        conflicto de reservas a favor de otra solicitud."""
        self.estado = EstadoReserva.REASIGNADA
        self._registrar_cambio(EstadoReserva.REASIGNADA, momento)

    def _registrar_cambio(self, estado: EstadoReserva, momento: datetime) -> None:
        """RF-12 / RNF-03: guarda cada cambio de estado con fecha/hora."""
        self.historial.append(CambioEstado(estado, momento))

    def __str__(self) -> str:
        estado_txt = self.estado.value if self.estado else "SOLICITADA (sin confirmar)"
        return (f"{self.id_reserva} | {self.usuario.nombre} | "
                f"{self.cancha.nombre} | {self.horario} | "
                f"estado={estado_txt}")
#Valeria Alanuca
#00342425