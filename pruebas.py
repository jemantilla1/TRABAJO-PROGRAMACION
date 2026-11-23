import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from cliente import Cliente
from servicio import ReservaSalas, AlquilerEquipos, AsesoriaEspecializada
from reserva import Reserva
from excepciones import (
    SoftwareFJError,
    ClienteInvalidError,
    ServicioInvalidError,
    ServicioNoDisponibleError,
    ReservaInvalidError,
    CapacidadExcedidaError,
    CalculoInconsistenteError
)
from logs import log_info, log_error, log_warning


def ejecutar_simulaciones():
    """Ejecuta la suite completa de 12 pruebas de simulación garantizando resiliencia."""

    log_info("==========================================================================")
    log_info("INICIANDO SUITE DE SIMULACIONES Y PRUEBAS AUTOMATIZADAS DE SOFTWARE FJ")
    log_info("==========================================================================")

    resultados = []

    # PRUEBA 1
    try:
        log_info("\n--- [Escenario 1/12] Registro Válido de Cliente ---")

        cli1 = Cliente(
            "CLI-001",
            "Jorge Martínez",
            "jorge.martinez@ejemplo.com",
            "3001234567"
        )

        resultados.append((
            "Escenario 1",
            "Registro Cliente Válido",
            "ÉXITO",
            cli1.obtener_resumen()
        ))

    except SoftwareFJError as e:
        resultados.append((
            "Escenario 1",
            "Registro Cliente Válido",
            "FALLO",
            str(e)
        ))

    # PRUEBA 2
    try:
        log_info("\n--- [Escenario 2/12] Registro Inválido de Cliente (Email Erróneo) ---")

        cli_bad = Cliente(
            "CLI-999",
            "Pedro Pérez",
            "correo_invalido_sin_ arroba",
            "3119876543"
        )

        resultados.append((
            "Escenario 2",
            "Registro Cliente Email Inválido",
            "FALLO INESPERADO",
            cli_bad.obtener_resumen()
        ))

    except ClienteInvalidError as e:
        log_warning(f"Excepción capturada correctamente en Escenario 2: {e}")

        resultados.append((
            "Escenario 2",
            "Registro Cliente Email Inválido",
            "ÉXITO (ERROR CONTROLADO)",
            str(e)
        ))

    # PRUEBA 3
    try:
        log_info("\n--- [Escenario 3/12] Registro Válido de Servicio (ReservaSalas) ---")

        srv_sala = ReservaSalas(
            "SRV-SALA-01",
            "Sala Ejecutiva Innovation",
            45000.0,
            capacidad_maxima=15,
            equipamiento_audiovisual=True
        )

        resultados.append((
            "Escenario 3",
            "Creación Servicio Sala Válido",
            "ÉXITO",
            srv_sala.obtener_descripcion()
        ))

    except SoftwareFJError as e:
        resultados.append((
            "Escenario 3",
            "Creación Servicio Sala Válido",
            "FALLO",
            str(e)
        ))

    # PRUEBA 4
    try:
        log_info("\n--- [Escenario 4/12] Registro Inválido de Servicio (Tarifa Negativa) ---")

        srv_bad = AlquilerEquipos(
            "SRV-EQ-BAD",
            "Laptop Gamer Pro",
            -5000.0,
            "Computador",
            100000.0
        )

        resultados.append((
            "Escenario 4",
            "Creación Servicio Tarifa Negativa",
            "FALLO INESPERADO",
            srv_bad.obtener_resumen()
        ))

    except ServicioInvalidError as e:
        log_warning(f"Excepción capturada correctamente en Escenario 4: {e}")

        resultados.append((
            "Escenario 4",
            "Creación Servicio Tarifa Negativa",
            "ÉXITO (ERROR CONTROLADO)",
            str(e)
        ))

    # PRUEBA 5
    try:
        log_info("\n--- [Escenario 5/12] Registro Válido de Equipos y Asesoría ---")

        srv_eq = AlquilerEquipos(
            "SRV-EQ-01",
            "Servidor Workstation RACK 4U",
            25000.0,
            "Servidores",
            300000.0
        )

        srv_asesoria = AsesoriaEspecializada(
            "SRV-ASE-01",
            "Consultoría en Arquitectura Cloud",
            80000.0,
            "Dr. Carlos Gómez",
            "Architect"
        )

        resultados.append((
            "Escenario 5",
            "Creación Servicios Equipos y Asesoría",
            "ÉXITO",
            f"{srv_eq.nombre} y {srv_asesoria.nombre}"
        ))

    except SoftwareFJError as e:
        resultados.append((
            "Escenario 5",
            "Creación Servicios Equipos y Asesoría",
            "FALLO",
            str(e)
        ))

    # PRUEBA 6
    try:
        log_info("\n--- [Escenario 6/12] Creación de Reserva Válida y Cálculo de Costo ---")

        res1 = Reserva(
            "RES-1001",
            cli1,
            srv_asesoria,
            duracion_horas=5.0
        )

        costo_total = res1.calcular_costo_total(
            descuento=0.10,
            impuesto=0.19
        )

        resultados.append((
            "Escenario 6",
            "Reserva Válida y Costo",
            "ÉXITO",
            f"Costo Total 5h Asesoría Architect: ${costo_total:,.2f}"
        ))

    except SoftwareFJError as e:
        resultados.append((
            "Escenario 6",
            "Reserva Válida y Costo",
            "FALLO",
            str(e)
        ))

    # PRUEBA 7
    try:
        log_info("\n--- [Escenario 7/12] Reserva Fallida (Servicio No Disponible) ---")

        srv_sala.disponible = False

        res_nodisp = Reserva(
            "RES-1002",
            cli1,
            srv_sala,
            duracion_horas=2.0
        )

        resultados.append((
            "Escenario 7",
            "Reserva Servicio No Disponible",
            "FALLO INESPERADO",
            res_nodisp.obtener_resumen()
        ))

    except ServicioNoDisponibleError as e:
        log_warning(f"Excepción capturada correctamente en Escenario 7: {e}")

        resultados.append((
            "Escenario 7",
            "Reserva Servicio No Disponible",
            "ÉXITO (ERROR CONTROLADO)",
            str(e)
        ))

    finally:
        srv_sala.disponible = True

    # PRUEBA 8
    try:
        log_info("\n--- [Escenario 8/12] Reserva Fallida por Exceso de Capacidad (Encadenamiento) ---")

        res_cap = Reserva(
            "RES-1003",
            cli1,
            srv_sala,
            duracion_horas=3.0,
            asistentes=30
        )

        resultados.append((
            "Escenario 8",
            "Reserva Exceso Capacidad",
            "FALLO INESPERADO",
            res_cap.obtener_resumen()
        ))

    except CapacidadExcedidaError as e:
        log_warning(f"Excepción capturada correctamente en Escenario 8: {e}")

        causa = (
            f"Causa raíz encadenada: {e.__cause__}"
            if e.__cause__
            else "Sin causa encadenada"
        )

        resultados.append((
            "Escenario 8",
            "Reserva Exceso Capacidad",
            "ÉXITO (ERROR CONTROLADO)",
            f"{e} | {causa}"
        ))

    # PRUEBA 9
    try:
        log_info("\n--- [Escenario 9/12] Flujo Completo: Creación -> Confirmación -> Procesamiento ---")

        cli2 = Cliente(
            "CLI-002",
            "María Fernanda Torres",
            "m.torres@empresa.com",
            "3158889900"
        )

        res_flujo = Reserva(
            "RES-1004",
            cli2,
            srv_sala,
            duracion_horas=4.0,
            asistentes=10
        )

        res_flujo.confirmar_reserva()
        res_flujo.procesar_reserva()

        resultados.append((
            "Escenario 9",
            "Flujo Confirmación y Procesamiento",
            "ÉXITO",
            res_flujo.obtener_resumen()
        ))

    except SoftwareFJError as e:
        resultados.append((
            "Escenario 9",
            "Flujo Confirmación y Procesamiento",
            "FALLO",
            str(e)
        ))

    # PRUEBA 10
    try:
        log_info("\n--- [Escenario 10/12] Cancelación de Reserva Ya Procesada ---")

        res_flujo.cancelar_reserva("Cambio de opinión del usuario")

        resultados.append((
            "Escenario 10",
            "Cancelar Reserva Procesada",
            "FALLO INESPERADO",
            "Se permitió cancelar una reserva procesada"
        ))

    except ReservaInvalidError as e:
        log_warning(f"Excepción capturada correctamente en Escenario 10: {e}")

        resultados.append((
            "Escenario 10",
            "Cancelar Reserva Procesada",
            "ÉXITO (ERROR CONTROLADO)",
            str(e)
        ))

    # PRUEBA 11
    try:
        log_info("\n--- [Escenario 11/12] Cálculo Inconsistente (Duración = -2 horas) ---")

        res_bad_dur = Reserva(
            "RES-1005",
            cli1,
            srv_eq,
            duracion_horas=-2.0
        )

        resultados.append((
            "Escenario 11",
            "Duración Negativa",
            "FALLO INESPERADO",
            res_bad_dur.obtener_resumen()
        ))

    except CalculoInconsistenteError as e:
        log_warning(f"Excepción capturada correctamente en Escenario 11: {e}")

        resultados.append((
            "Escenario 11",
            "Duración Negativa",
            "ÉXITO (ERROR CONTROLADO)",
            str(e)
        ))

    # PRUEBA 12
    try:
        log_info("\n--- [Escenario 12/12] Procesamiento de Reserva en Estado PENDIENTE ---")

        res_pend = Reserva(
            "RES-1006",
            cli1,
            srv_eq,
            duracion_horas=12.0
        )

        res_pend.procesar_reserva()

        resultados.append((
            "Escenario 12",
            "Procesar Sin Confirmar",
            "FALLO INESPERADO",
            "Se procesó sin estar confirmada"
        ))

    except ReservaInvalidError as e:
        log_warning(f"Excepción capturada correctamente en Escenario 12: {e}")

        resultados.append((
            "Escenario 12",
            "Procesar Sin Confirmar",
            "ÉXITO (ERROR CONTROLADO)",
            str(e)
        ))

    log_info("\n==========================================================================")
    log_info("FINALIZACIÓN DE PRUEBAS DE SIMULACIÓN - TODAS LAS EXCEPCIONES MANEJADAS")
    log_info("==========================================================================")

    return resultados
