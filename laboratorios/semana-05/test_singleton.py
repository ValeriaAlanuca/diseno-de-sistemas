from singleton import GestorDeConfiguracion, reserva_permitida


def test_rechaza_reserva():
    config = GestorDeConfiguracion.obtener_objeto()
    config.modo_matenimiento = True

    assert reserva_permitida(config) is False


def test_reserva_aceptada():
    config = GestorDeConfiguracion.obtener_objeto()
    config.modo_matenimiento = False

    assert reserva_permitida(config) is True


# La prueba falla porque Singleton usa un solo objeto para todo
# En la primera prueba cambio modo_matenimiento a True y ese valor se queda guardado
# Entonces cuando se ejecuta la segunda prueba, se vuelve a usar el mismo objeto y el valor sigue siendo True, 
# por eso reserva_permitida(config) devuelve False aunque la prueba esperaba True
# Al usar Singleton las pruebas comparten el mismo objeto y lo que se cambia en una puede afectar a la siguiente
