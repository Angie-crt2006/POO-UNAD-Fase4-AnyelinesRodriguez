from abc import ABC, abstractmethod
from datetime import datetime
import os
from src.excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    CalculoInconsistenteError,
)


class RegistradorLogs:
    """Gestiona la escritura de eventos y errores en el archivo de logs."""

    def __init__(self, ruta_log: str = "logs/sistema.log"):
        self.ruta_log = ruta_log
        os.makedirs(os.path.dirname(self.ruta_log), exist_ok=True)

    def registrar(self, nivel: str, mensaje: str) -> None:
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{marca_tiempo}] [{nivel.upper()}] {mensaje}\n"
        with open(self.ruta_log, "a", encoding="utf-8") as archivo:
            archivo.write(linea)


class EntidadSistema(ABC):
    """Clase abstracta base que representa cualquier entidad del sistema."""

    def __init__(self, codigo: str):
        if not codigo or not codigo.strip():
            raise DatosInvalidosError("El código de la entidad no puede estar vacío.")
        self._codigo = codigo.strip()

    @property
    def codigo(self) -> str:
        return self._codigo

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Devuelve una descripción resumida de la entidad."""


class Cliente(EntidadSistema):
    """Representa un cliente de Software FJ con encapsulación y validaciones."""

    def __init__(self, codigo: str, nombre: str, correo: str, telefono: str):
        super().__init__(codigo)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or len(valor.strip()) < 3:
            raise DatosInvalidosError("El nombre del cliente debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not valor or "@" not in valor or "." not in valor:
            raise DatosInvalidosError(f"Correo electrónico inválido: '{valor}'.")
        self._correo = valor.strip()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not valor or not valor.isdigit() or len(valor) < 7:
            raise DatosInvalidosError("El teléfono debe contener solo dígitos (mínimo 7).")
        self._telefono = valor

    def obtener_resumen(self) -> str:
        return f"Cliente [{self.codigo}]: {self.nombre} | Correo: {self.correo}"


class Servicio(EntidadSistema, ABC):
    """Clase abstracta base para los servicios ofrecidos por Software FJ."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(codigo)
        if not nombre or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")
        if tarifa_base <= 0:
            raise DatosInvalidosError("La tarifa base debe ser mayor que cero.")
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @abstractmethod
    def validar_parametros(self, duracion_horas: int) -> None:
        """Valida condiciones específicas del servicio."""

    @abstractmethod
    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """Calcula el costo total aplicando sobrecarga mediante parámetros opcionales."""

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Servicio [{self.codigo}]: {self.nombre} (${self.tarifa_base:,.0f}/h) - {estado}"


class ReservaSala(Servicio):
    """Servicio especializado para reserva de salas de reuniones o capacitación."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, capacidad: int, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        if capacidad <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser mayor a cero.")
        self.capacidad = capacidad

    def validar_parametros(self, duracion_horas: int) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleError(f"La sala '{self.nombre}' no está disponible actualmente.")
        if duracion_horas < 1 or duracion_horas > 12:
            raise ServicioNoDisponibleError("La reserva de sala debe durar entre 1 y 12 horas.")

    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        self.validar_parametros(duracion_horas)
        if descuento < 0 or descuento >= 1:
            raise CalculoInconsistenteError("El descuento debe estar entre 0 y 0.99.")
        subtotal = self.tarifa_base * duracion_horas
        subtotal_con_descuento = subtotal * (1 - descuento)
        return round(subtotal_con_descuento * (1 + impuesto), 2)


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos tecnológicos."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, cantidad_equipos: int, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        if cantidad_equipos <= 0:
            raise DatosInvalidosError("Debe especificar al menos 1 equipo para alquilar.")
        self.cantidad_equipos = cantidad_equipos

    def validar_parametros(self, duracion_horas: int) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleError(f"El equipo '{self.nombre}' no se encuentra disponible.")
        if duracion_horas < 2:
            raise ServicioNoDisponibleError("El alquiler de equipos requiere un mínimo de 2 horas.")

    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        self.validar_parametros(duracion_horas)
        if descuento < 0 or descuento >= 1:
            raise CalculoInconsistenteError("El descuento aplicado no es válido.")
        subtotal = self.tarifa_base * duracion_horas * self.cantidad_equipos
        subtotal_con_descuento = subtotal * (1 - descuento)
        return round(subtotal_con_descuento * (1 + impuesto), 2)


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para consultoría y asesoría técnica."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, especialidad: str, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        if not especialidad or not especialidad.strip():
            raise DatosInvalidosError("La especialidad de la asesoría es obligatoria.")
        self.especialidad = especialidad.strip()

    def validar_parametros(self, duracion_horas: int) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleError(f"La asesoría '{self.nombre}' no tiene agenda disponible.")
        if duracion_horas <= 0:
            raise ServicioNoDisponibleError("La duración de la asesoría debe ser mayor a 0 horas.")

    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        self.validar_parametros(duracion_horas)
        if descuento < 0 or descuento >= 1:
            raise CalculoInconsistenteError("Porcentaje de descuento inconsistente.")
        recargo_especialidad = 1.10
        subtotal = (self.tarifa_base * duracion_horas) * recargo_especialidad
        subtotal_con_descuento = subtotal * (1 - descuento)
        return round(subtotal_con_descuento * (1 + impuesto), 2)


class Reserva(EntidadSistema):
    """Integra cliente, servicio, duración y estado con manejo y encadenamiento de excepciones."""

    def __init__(self, codigo: str, cliente: Cliente, servicio: Servicio, duracion_horas: int):
        super().__init__(codigo)
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("Se requiere un cliente válido para crear la reserva.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Se requiere un servicio válido para crear la reserva.")
        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = duracion_horas
        self.estado = "PENDIENTE"
        self.costo_total = 0.0

    def procesar_y_confirmar(self, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """Procesa y confirma la reserva aplicando encadenamiento de excepciones."""
        if self.estado == "CANCELADA":
            raise ReservaInvalidaError("No se puede confirmar una reserva que ya fue cancelada.")
        try:
            self.costo_total = self.servicio.calcular_costo(
                self.duracion_horas, descuento=descuento, impuesto=impuesto
            )
            self.estado = "CONFIRMADA"
            return self.costo_total
        except (ServicioNoDisponibleError, CalculoInconsistenteError) as error_origen:
            self.estado = "FALLIDA"
            raise ReservaInvalidaError(
                f"Fallo al procesar la reserva '{self.codigo}' para {self.cliente.nombre}."
            ) from error_origen

    def cancelar(self) -> None:
        if self.estado == "CANCELADA":
            raise ReservaInvalidaError(f"La reserva '{self.codigo}' ya estaba cancelada.")
        self.estado = "CANCELADA"

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.codigo}] | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Duración: {self.duracion_horas}h | "
            f"Estado: {self.estado} | Total: ${self.costo_total:,.2f}"
        )
