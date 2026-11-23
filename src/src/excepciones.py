# 2. `src/excepciones.py`
```python
class ErrorSistemaFJ(Exception):
    """Excepción base para todos los errores del sistema Software FJ."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje)
        self.mensaje = mensaje


class DatosInvalidosError(ErrorSistemaFJ):
    """Se lanza cuando los datos personales o parámetros son inválidos o faltantes."""


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando un servicio no cumple condiciones de disponibilidad o parámetros."""


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza cuando ocurre un error en la creación, confirmación o cancelación de una reserva."""


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando el cálculo de costos o tarifas produce un valor inválido."""
