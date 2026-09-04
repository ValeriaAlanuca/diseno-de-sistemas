from datetime import date, time, datetime

from equipo import Equipo
from usuario import Estudiante, Capitan, Administrador
from cancha import Cancha
from horario import Horario


def linea(titulo: str) -> None:
    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)


def main() -> None:
    hoy = date(2026, 9, 3)

    admin = Administrador("00100001", "Ana Torres (Administradora)")

    catalogo_canchas: list[Cancha] = []
    cancha_futbol = Cancha("C01", "Cancha de Futbol 1", "Futbol")
    cancha_basquet = Cancha("C02", "Cancha de Basquet 1", "Basquetbol")
    admin.agregar_cancha(cancha_futbol, catalogo_canchas)
    admin.agregar_cancha(cancha_basquet, catalogo_canchas)

    horario_tarde = Horario(hoy, time(16, 0), time(17, 0))
    horario_noche = Horario(hoy, time(20, 0), time(21, 0))
    cancha_futbol.agregar_horario(horario_tarde)
    cancha_futbol.agregar_horario(Horario(hoy, time(16, 0), time(17, 0)))  # slot alterno
    cancha_basquet.agregar_horario(horario_noche)

    equipo_tigres = Equipo("EQ01", "Tigres FC")
    estudiante = Estudiante("00203040", "Luis Perez")
    capitan = Capitan("00304050", "Maria Lopez", equipo_tigres)


    # CASO DE USO 1: Reservar cancha (flujo principal, sin conflicto)
    linea("CASO DE USO: Reservar cancha (Luis Perez, estudiante regular)")
    momento_reserva_1 = datetime(2026, 9, 3, 10, 0)
    print("1. El usuario solicita reservar una cancha para una fecha y hora "
          f"({estudiante.nombre} -> {cancha_futbol} el {horario_tarde}).")
    print("2. El sistema verifica la disponibilidad de la cancha.")
    disponible = cancha_futbol.verificar_disponibilidad(horario_tarde)
    print(f"   -> Disponible: {disponible}")
    print("3. El sistema aplica la regla de prioridad del usuario sobre el horario.")
    print(f"   -> ¿Aplica prioridad?: {estudiante.regla_prioridad.aplica_prioridad(horario_tarde)}")
    reserva_luis = estudiante.solicitar_reserva(cancha_futbol, horario_tarde, momento_reserva_1)
    print("4. El sistema crea la reserva con estado CONFIRMADA.")
    print("5. El sistema registra el cambio de estado con fecha y hora.")
    print(f"   -> Historial: {[str(c) for c in reserva_luis.historial]}")
    print("6. El sistema confirma la reserva al usuario.")
    print(f"   -> {reserva_luis}")


    # CASO DE USO 1 (flujo alterno 3a): conflicto de prioridad
    linea("CASO DE USO: Reservar cancha (Maria Lopez, capitan, con conflicto)")
    horario_conflicto = Horario(hoy, time(16, 0), time(17, 0))
    momento_reserva_2 = datetime(2026, 9, 3, 11, 0)
    print("1. El usuario solicita reservar una cancha para una fecha y hora "
          f"({capitan.nombre} -> {cancha_futbol} el {horario_conflicto}, antes de 6pm).")
    print("2. El sistema verifica la disponibilidad de la cancha.")
    print("   -> El horario ya esta ocupado por la reserva de Luis Perez.")
    print("3. El sistema aplica la regla de prioridad del usuario sobre el horario.")
    aplica = capitan.regla_prioridad.aplica_prioridad(horario_conflicto)
    print(f"   -> ¿Aplica prioridad? (capitan, antes de 6pm): {aplica}")
    print("3a. Existe conflicto con una reserva sin prioridad -> el sistema "
          "deriva el conflicto al Administrador.")

    # CASO DE USO 4: Resolver conflicto de reservas
    linea("CASO DE USO: Resolver conflicto de reservas (Administrador)")
    # Se construye la solicitud en conflicto del capitan (aun no confirmada).
    from reserva import Reserva
    reserva_capitan = Reserva(capitan, cancha_futbol, horario_conflicto)
    momento_conflicto = datetime(2026, 9, 3, 11, 0, 5)
    print("1. El sistema notifica al administrador sobre el conflicto.")
    print("2. El administrador revisa las reservas en conflicto:")
    print(f"   -> Reserva existente (sin prioridad): {reserva_luis}")
    print(f"   -> Solicitud nueva (con prioridad):    {reserva_capitan}")
    print("3. El administrador decide cual solicitud prevalece, respetando "
          "la regla de prioridad de capitanes.")
    ganadora = admin.resolver_conflicto(reserva_luis, reserva_capitan, momento_conflicto)
    if ganadora is reserva_capitan:
        print("3->4a. Prevalece la solicitud con prioridad: la reserva "
              "anterior pasa a REASIGNADA y se notifica al estudiante afectado.")
    else:
        print("3->4b. Se mantiene la reserva existente; se rechaza la "
              "solicitud con prioridad.")
    print("5. El sistema registra el cambio de estado con fecha y hora.")
    print(f"   -> {reserva_luis}")
    print(f"   -> {reserva_capitan}")

    # CASO DE USO 2: Cancelar reserva (cancelacion regular, >= 2h)
    linea("CASO DE USO: Cancelar reserva (con anticipacion suficiente)")
    momento_cancelacion_1 = datetime(2026, 9, 3, 13, 0)  # 3 horas antes de las 16:00
    print(f"1. El usuario solicita cancelar su reserva ({reserva_capitan.id_reserva}).")
    print("2. El sistema calcula el tiempo restante hasta el inicio de la reserva.")
    restante = reserva_capitan.horario.inicio_datetime() - momento_cancelacion_1
    print(f"   -> Tiempo restante: {restante}")
    print("3. El sistema determina si la accion se registra como cancelacion "
          "regular o como no-show.")
    capitan.cancelar_reserva(reserva_capitan, momento_cancelacion_1)
    print("4. El sistema registra el cambio de estado con fecha y hora.")
    print("5. El sistema confirma la cancelacion al usuario.")
    print(f"   -> {reserva_capitan}")

    # CASO DE USO 2 (flujo alterno 3a): cancelacion tardia -> NO_SHOW
    linea("CASO DE USO: Cancelar reserva (con menos de 2 horas -> no-show)")
    momento_reserva_3 = datetime(2026, 9, 3, 9, 0)
    reserva_luis_noche = estudiante.solicitar_reserva(cancha_basquet, horario_noche, momento_reserva_3)
    momento_cancelacion_2 = datetime(2026, 9, 3, 19, 30)  # 30 min antes de las 20:00
    print(f"1. El usuario solicita cancelar su reserva ({reserva_luis_noche.id_reserva}).")
    print("2. El sistema calcula el tiempo restante hasta el inicio de la reserva.")
    restante2 = reserva_luis_noche.horario.inicio_datetime() - momento_cancelacion_2
    print(f"   -> Tiempo restante: {restante2} (menor a 2 horas)")
    print("3a. Faltan menos de 2 horas -> el sistema registra la reserva como NO_SHOW.")
    estudiante.cancelar_reserva(reserva_luis_noche, momento_cancelacion_2)
    print("4. El sistema registra el cambio de estado con fecha y hora.")
    print("5. El sistema confirma la cancelacion al usuario.")
    print(f"   -> {reserva_luis_noche}")

    # CASO DE USO 3: Gestionar canchas (agregar)
    linea("CASO DE USO: Gestionar canchas (agregar)")
    cancha_voley = Cancha("C03", "Cancha de Voley 1", "Voleibol")
    print("1. El administrador solicita agregar una cancha nueva.")
    admin.agregar_cancha(cancha_voley, catalogo_canchas)
    print("2. El sistema registra la cancha con sus atributos.")
    print("3. El sistema confirma el registro de la cancha.")
    print(f"   -> Catalogo actual: {[str(c) for c in catalogo_canchas]}")

    # CASO DE USO 3 (flujo alterno): retirar cancha SIN reservas activas
    linea("CASO DE USO: Gestionar canchas (retirar, sin reservas activas)")
    print("1a. El administrador solicita retirar una cancha existente "
          f"({cancha_voley.nombre}).")
    print("2a. El sistema verifica si la cancha tiene reservas activas.")
    retirada = admin.retirar_cancha(cancha_voley, catalogo_canchas)
    if retirada:
        print("4a. La cancha no tenia reservas activas -> el sistema la "
              "elimina del catalogo.")
    else:
        print("3a. La cancha tiene reservas activas -> el sistema rechaza el retiro.")
    print(f"   -> Catalogo actual: {[str(c) for c in catalogo_canchas]}")

  
    # CASO DE USO 3 (flujo alterno): retirar cancha CON reservas activas
    linea("CASO DE USO: Gestionar canchas (retirar, con reservas activas -> rechazo)")
    # Se crea una nueva reserva CONFIRMADA para poder demostrar el rechazo.
    otro_horario = Horario(hoy, time(18, 0), time(19, 0))
    cancha_futbol.agregar_horario(otro_horario)
    estudiante.solicitar_reserva(cancha_futbol, otro_horario, datetime(2026, 9, 3, 8, 0))
    print("1a. El administrador solicita retirar una cancha existente "
          f"({cancha_futbol.nombre}).")
    print("2a. El sistema verifica si la cancha tiene reservas activas.")
    retirada_futbol = admin.retirar_cancha(cancha_futbol, catalogo_canchas)
    if retirada_futbol:
        print("4a. La cancha no tenia reservas activas -> el sistema la "
              "elimina del catalogo.")
    else:
        print("3a. La cancha tiene reservas activas (reserva CONFIRMADA de "
              "Luis Perez) -> el sistema rechaza el retiro.")
    print(f"   -> Catalogo actual: {[str(c) for c in catalogo_canchas]}")


    # Validacion de RF-15 / RNF-06: codigo banner invalido
    linea("VALIDACION: registro con codigo banner invalido (RF-15 / RNF-06)")
    try:
        Estudiante("12345", "Usuario con codigo invalido")
    except ValueError as error:
        print(f"-> El sistema rechaza el registro: {error}")

    print("\nSimulacion completa ejecutada sin errores.")


if __name__ == "__main__":
    main()
#Valeria Alanuca
#00342425
