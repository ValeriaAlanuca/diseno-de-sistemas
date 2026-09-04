from reserva import EstadoReserva
#Valeria Alanuca
#00342425

class Cancha:
    def __init__(self, id_cancha: str, nombre: str, deporte: str):
        self.id_cancha = id_cancha
        self.nombre = nombre
        self.deporte = deporte
        self.horarios: list = []
        self._reservas: list = []

    def agregar_horario(self, horario) -> None:
        self.horarios.append(horario)

    def verificar_disponibilidad(self, horario) -> bool:
        """RF-02/RF-13: indica si la cancha esta libre en ese horario."""
        for h in self.horarios:
            if h.coincide_con(horario):
                return h.disponible
        return False

    def marcar_reservado(self, horario) -> None:
        for h in self.horarios:
            if h.coincide_con(horario):
                h.disponible = False

    def liberar_horario(self, horario) -> None:
        for h in self.horarios:
            if h.coincide_con(horario):
                h.disponible = True

    def registrar_reserva(self, reserva) -> None:
        self._reservas.append(reserva)

    def tiene_reservas_activas(self) -> bool:
        """RF-10: una cancha con reservas CONFIRMADA no puede retirarse."""
        return any(r.estado == EstadoReserva.CONFIRMADA for r in self._reservas)

    def __str__(self) -> str:
        return f"{self.nombre} ({self.deporte})"
