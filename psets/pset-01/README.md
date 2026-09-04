# PSet 1 — ReservaU

Nombre: Valeria Alanuca
Código: 00342425

## Contenido de esta carpeta

- `implementacion/`
  - `usuario.py`, `equipo.py`, `regla_prioridad.py`, `cancha.py`, `horario.py`, `reserva.py` — Clases del modelo de dominio.
  - `simulacion.py` — Script que instancia las clases y ejecuta todos los flujos, imprimiendo cada paso en el mismo orden que el flujo principal documentado.
  - `Dockerfile` — Contenedor que ejecuta `simulacion.py`.

## Ejecutar

```bash
cd implementacion
python3 simulacion.py
```

O con Docker:

```bash
cd implementacion
docker build -t reservau .
docker run reservau
```

## Trazabilidad (ejemplo)

**RF-06 / RF-07 / RF-08** (regla de las 2 horas la decide el sistema, no el usuario)
→ Caso de uso *Cancelar reserva*, paso 3 (flujos alternos 3a/3b)
→ Clase `Reserva`, método `cancelar(hora_actual)`
→ Observable en `simulacion.py`, secciones "Cancelar reserva (con anticipación suficiente)" y "Cancelar reserva (con menos de 2 horas -> no-show)".

**RF-03 / RF-14** (prioridad de equipos oficiales antes de las 6:00 p.m.)
→ Caso de uso *Reservar cancha*, paso 3 (flujo alterno 3a) y *Resolver conflicto de reservas*
→ Clases `ReglaPrioridadAntesDe6pm` (compuesta en `Capitan`) y `Administrador.resolver_conflicto(...)`
→ Observable en `simulacion.py`, secciones "Reservar cancha (Maria Lopez, capitan, con conflicto)" y "Resolver conflicto de reservas".
