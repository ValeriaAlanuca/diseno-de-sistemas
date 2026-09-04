class Equipo:
    def __init__(self, id_equipo: str, nombre: str):
        self.id_equipo = id_equipo
        self.nombre = nombre
        self.capitan = None

    def __str__(self) -> str:
        return self.nombre
#Valeria Alanuca
#00342425