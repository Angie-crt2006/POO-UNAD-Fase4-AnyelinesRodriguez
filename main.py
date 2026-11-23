from src.excepciones import ErrorSistemaFJ
from src.modelos import (
    RegistradorLogs,
    Cliente,
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
    Reserva,
)


def ejecutar_simulacion() -> None:
    logger = RegistradorLogs("logs/sistema.log")
    clientes = []
    servicios = []
    reservas = []

    logger.registrar("INFO", "=== Inicio de simulación del sistema Software FJ ===")
    print("=== SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ ===\n")

    # Operación 1: Registro válido de cliente 1
    try:
        c1 = Cliente("CLI-01", "Anyelines Rodríguez", "anyelines@unad.edu.co", "3001234567")
    except ErrorSistemaFJ as e:
        logger.registrar("ERROR", f"Op 1 fallida: {e}")
    else:
        clientes.append(c1)
        logger.registrar("INFO", f"Op 1 exitosa: {c1.obtener_resumen()}")
        print(f"[Op 1 OK] {c1.obtener_resumen()}")

    # Operación 2: Registro válido de cliente 2
    try:
        c2 = Cliente("CLI-02", "Carlos Mendoza", "cmendoza@empresa.com", "3109876543")
    except ErrorSistemaFJ as e:
        logger.registrar("ERROR", f"Op 2 fallida: {e}")
    else:
        clientes.append(c2)
        logger.registrar("INFO", f"Op 2 exitosa: {c2.obtener_resumen()}")
        print(f"[Op 2 OK] {c2.obtener_resumen()}")

    # Operación 3: Registro inválido de cliente (correo sin @ y teléfono corto)
    try:
        c_invalido = Cliente("CLI-03", "Ana", "correo_invalido", "123")
        clientes.append(c_invalido)
    except ErrorSistemaFJ as e:
        logger.registrar("ERROR", f"Op 3 capturada correctamente: {e}")
        print(f"[Op 3 ERROR CONTROLADO] {e}")

    # Operación 4: Creación válida de servicio ReservaSala
    try:
        s1 = ReservaSala("SRV-01", "Sala Ejecutiva Norte", 80000, capacidad=15, disponible=True)
        servicios.append(s1)
        logger.registrar("INFO", f"Op 4 exitosa: {s1.obtener_resumen()}")
        print(f"[Op 4 OK] {s1.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        logger.registrar("ERROR", f"Op 4 fallida: {e}")

    # Operación 5: Creación válida de servicio AlquilerEquipo
    try:
        s2 = AlquilerEquipo("SRV-02", "Portátiles Dell Core i7", 25000, cantidad_equipos=4, disponible=True)
        servicios.append(s2)
        logger.registrar("INFO", f"Op 5 exitosa: {s2.obtener_resumen()}")
        print(f"[Op 5 OK] {s2.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        logger.registrar("ERROR", f"Op 5 fallida: {e}")

    # Operación 6: Creación válida de servicio AsesoriaEspecializada (no disponible)
    try:
        s3 = AsesoriaEspecializada("SRV-03", "Arquitectura Cloud", 120000, "Nube", disponible=False)
        servicios.append(s3)
        logger.registrar("INFO", f"Op 6 exitosa: {s3.obtener_resumen()}")
        print(f"[Op 6 OK] {s3.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        logger.registrar("ERROR", f"Op 6 fallida: {e}")

    # Operación 7: Creación inválida de servicio (tarifa negativa)
    try:
        s_invalido = ReservaSala("SRV-04", "Sala Sur", -50000, capacidad=10)
        servicios.append(s_invalido)
    except ErrorSistemaFJ as e:
        logger.registrar("ERROR", f"Op 7 capturada correctamente: {e}")
        print(f"[Op 7 ERROR CONTROLADO] {e}")

    # Operación 8: Reserva exitosa con cálculo estándar (sobrecarga sin descuento)
    r1 = Reserva("RES-01", clientes[0], servicios[0], duracion_horas=4)
    try:
        r1.procesar_y_confirmar()
    except ErrorSistemaFJ as e:
        logger.registrar("ERROR", f"Op 8 fallida: {e}")
    else:
        reservas.append(r1)
        logger.registrar("INFO", f"Op 8 exitosa: {r1.obtener_resumen()}")
        print(f"[Op 8 OK] {r1.obtener_resumen()}")
    finally:
        logger.registrar("INFO", "Op 8 finalizada: verificación de estado completada.")

    # Operación 9: Reserva exitosa con descuento aplicado (sobrecarga con parámetros opcionales)
    r2 = Reserva("RES-02", clientes[1], servicios[1], duracion_horas=3)
    try:
        r2.procesar_y_confirmar(descuento=0.10, impuesto=0.19)
    except ErrorSistemaFJ as e:
        logger.registrar("ERROR", f"Op 9 fallida: {e}")
    else:
        reservas.append(r2)
        logger.registrar("INFO", f"Op 9 exitosa: {r2.obtener_resumen()}")
        print(f"[Op 9 OK] {r2.obtener_resumen()}")
    finally:
        logger.registrar("INFO", "Op 9 finalizada: cierre de transacción.")

    # Operación 10: Reserva fallida por servicio no disponible (encadenamiento de excepciones)
    r3 = Reserva("RES-03", clientes[0], servicios[2], duracion_horas=2)
    try:
        r3.procesar_y_confirmar()
    except ErrorSistemaFJ as e:
        detalle_causa = f" | Causa raíz: {e.__cause__}" if e.__cause__ else ""
        logger.registrar("ERROR", f"Op 10 capturada: {e}{detalle_causa}")
        print(f"[Op 10 ERROR CONTROLADO] {e}{detalle_causa}")

    # Operación 11: Reserva fallida por duración inválida en alquiler de equipos (< 2h)
    r4 = Reserva("RES-04", clientes[1], servicios[1], duracion_horas=1)
    try:
        r4.procesar_y_confirmar()
    except ErrorSistemaFJ as e:
        detalle_causa = f" | Causa raíz: {e.__cause__}" if e.__cause__ else ""
        logger.registrar("ERROR", f"Op 11 capturada: {e}{detalle_causa}")
        print(f"[Op 11 ERROR CONTROLADO] {e}{detalle_causa}")

    # Operación 12: Cancelación válida y segundo intento inválido de cancelación
    try:
        r1.cancelar()
        logger.registrar("INFO", f"Op 12a exitosa: {r1.obtener_resumen()}")
        print(f"[Op 12a OK] {r1.obtener_resumen()}")
        r1.cancelar()  # Debe fallar porque ya está cancelada
    except ErrorSistemaFJ as e:
        logger.registrar("ERROR", f"Op 12b capturada correctamente: {e}")
        print(f"[Op 12b ERROR CONTROLADO] {e}")

    logger.registrar("INFO", "=== Fin de simulación: sistema estable sin interrupciones ===")
    print("\nSimulación completada exitosamente. Revisa 'logs/sistema.log'.")


if __name__ == "__main__":
    ejecutar_simulacion()
