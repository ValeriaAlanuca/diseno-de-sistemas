# Vehiculo  -> se mueva y función sea mover
#auto conduce por carretera
#bote se mueve por mar
#avion se mueve por cielo

class Mover:
    def movimiento(self):
        raise NotImplementedError


class MueveMar(Mover):
    def movimiento(self):
        print("Navegando por agua.")

class MueveCielo(Mover):
    def movimiento(self):
        print("Volando por el aire")


class MueveCarretera(Mover):
    def movimiento(self):
        print("Conduciendo por carretera")


class Vehiculo:
    def __init__(self, comportamiento_movimiento):
        self.comportamiento_movimiento = comportamiento_movimiento

    def movimiento(self):
        self.comportamiento_movimiento.movimiento()


class Bote(Vehiculo):
    def __init__(self):
        mueve_mar = MueveMar()
        super().__init__(mueve_mar)


class Carro(Vehiculo):
    def __init__(self):
        mueve_carretera = MueveCarretera()
        super().__init__(mueve_carretera)


class Avion(Vehiculo):
    def __init__(self):
        mueve_cielo = MueveCielo()
        super().__init__(mueve_cielo)


if __name__ == "__main__":
    print("Auto:")
    auto = Carro()
    auto.movimiento()
    print("Bote:")
    bote = Bote()
    bote.movimiento()
    print("Avion:")
    avion = Avion()
    avion.movimiento()