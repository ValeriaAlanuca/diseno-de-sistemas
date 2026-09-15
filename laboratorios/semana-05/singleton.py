class GestorDeConfiguracion:
    _objeto = None  # vacío

    def __init__(self):
        self.modo_matenimiento = False
        GestorDeConfiguracion._objeto = self

    @staticmethod
    def obtener_objeto():
        if GestorDeConfiguracion._objeto is None:
            GestorDeConfiguracion()
        return GestorDeConfiguracion._objeto


def reserva_permitida(gestor):
    return not gestor.modo_matenimiento