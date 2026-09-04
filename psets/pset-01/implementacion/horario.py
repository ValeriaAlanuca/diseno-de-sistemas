
from dataclasses import dataclass
from datetime import date, time, datetime


@dataclass
class Horario:
    fecha: date
    hora_inicio: time
    hora_fin: time
    disponible: bool =True

    def inicio_datetime(self) -> datetime:
        return datetime.combine(self.fecha, self.hora_inicio)

    def coincide_con(self, otro: "Horario") -> bool:
        return self.fecha == otro.fecha and self.hora_inicio == otro.hora_inicio

    def __str__(self) -> str:
        return (f"{self.fecha.isoformat()} "
                f"{self.hora_inicio.strftime('%H:%M')}-{self.hora_fin.strftime('%H:%M')}")
#Valeria Alanuca
#00342425