
import re
from datetime import datetime

from regla_prioridad import ReglaPrioridad, ReglaSinPrioridad, ReglaPrioridadAntesDe6pm
from reserva import Reserva

PATRON_CODIGO_BANNER = re.compile(r"^00\d{6}$")  # 8 digitos, inicia con '00'


class Usuario:

    def __init__(self, codigo_banner: str, nombre: str):
        if not self.validar_codigo_banner(codigo_banner):
            raise ValueError(
                f"Codigo banner invalido para '{nombre}': '{codigo_banner}' "
                "(debe tener 8 digitos e iniciar con '00')."
            )
        self.codigo_banner = codigo_banner
        self.nombre = nombre

    @staticmethod
    def validar_codigo_banner(codigo: str) -> bool:
      
        return bool(PATRON_CODIGO_BANNER.match(codigo))


class Estudiante(Usuario):
    def __init__(self, codigo_banner: str, nombre: str,
                 regla_prioridad: ReglaPrioridad = None):
        super().__init__(codigo_banner, nombre)
        # Cada solicitante tiene su propia regla de prioridad en lugar
        # de decidirla con un if dentro de este metodo (RNF-02).
        self.regla_prioridad: ReglaPrioridad = regla_prioridad or ReglaSinPrioridad()

    def solicitar_reserva(self, cancha, horario, momento: datetime):

 
        if not cancha.verificar_disponibilidad(horario):
            return None
        reserva = Reserva(self, cancha, horario)
        cancha.marcar_reservado(horario)
        cancha.registrar_reserva(reserva)
        reserva.confirmar(momento)
        return reserva

    def cancelar_reserva(self, reserva: Reserva, momento: datetime) -> None:
        
        reserva.cancelar(momento)


class Capitan(Estudiante):
    def __init__(self, codigo_banner: str, nombre: str, equipo):

        super().__init__(codigo_banner, nombre,
                          regla_prioridad=ReglaPrioridadAntesDe6pm())
        self.equipo = equipo
        equipo.capitan = self


class Administrador(Usuario):
    def agregar_cancha(self, cancha, catalogo: list) -> None:
   
        catalogo.append(cancha)

    def retirar_cancha(self, cancha, catalogo: list) -> bool:
       
        if cancha.tiene_reservas_activas():
            return False
        catalogo.remove(cancha)
        return True

    def resolver_conflicto(self, reserva_sin_prioridad: Reserva,
                            reserva_con_prioridad: Reserva,
                            momento: datetime) -> Reserva:
      
        regla = reserva_con_prioridad.usuario.regla_prioridad
        if regla.aplica_prioridad(reserva_con_prioridad.horario):
            reserva_sin_prioridad.reasignar(momento)
            reserva_con_prioridad.confirmar(momento)
            return reserva_con_prioridad
        reserva_con_prioridad.reasignar(momento)
        return reserva_sin_prioridad
#Valeria Alanuca
#00342425