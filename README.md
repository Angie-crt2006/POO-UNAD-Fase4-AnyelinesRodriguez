# Fase 4 – Prácticas Simuladas: Sistema Integral de Gestión (Software FJ)

**Universidad Nacional Abierta y a Distancia (UNAD)**  
**Vicerrectoría Académica y de Investigación**  
**Unidad Gestora:** Escuela de Ciencias Básicas, Tecnología e Ingeniería (ECBTI)  
**Programa:** Ingeniería de Sistemas  
**Curso:** Programación (Código: 213023)  
**Estudiante:** Anyelines Rodríguez Alvernia (`@Angie-crt2006`)  
**Modalidad:** Entrega Individual – Práctica Simulada  
**Fecha de entrega:** 22 de noviembre de 2026  

---

## 1. Descripción del Proyecto
Este repositorio contiene el desarrollo del **Ejercicio 1: Sistema Integral de Gestión de Clientes, Servicios y Reservas** para la empresa **Software FJ**. La aplicación está construida íntegramente bajo el paradigma de **Programación Orientada a Objetos (POO)** en Python, sin motores de bases de datos, gestionando toda la información en memoria mediante objetos y listas internas, y registrando la trazabilidad de eventos y errores en un archivo de logs.

El objetivo principal es garantizar la **estabilidad, modularidad y tolerancia a fallos** del sistema ante entradas inválidas, parámetros faltantes, servicios no disponibles o operaciones inconsistentes.

---

## 2. Arquitectura y Principios de POO Aplicados
* **Abstracción:** Implementación de las clases base abstractas `EntidadSistema` y `Servicio` mediante el módulo `abc`, estableciendo contratos obligatorios para todas las entidades del dominio.
* **Encapsulación:** Protección de atributos internos (`_codigo`, `_nombre`, `_correo`, `_telefono`, `_tarifa_base`, `_disponible`) mediante propiedades (`@property`) y *setters* con validaciones estrictas de formato y dominio.
* **Herencia y Polimorfismo:** Especialización de la clase abstracta `Servicio` en tres servicios concretos (`ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada`), cada uno con reglas propias de validación (`validar_parametros`) y cálculo tarifario (`calcular_costo`).
* **Sobrecarga de Métodos:** El método `calcular_costo(duracion_horas, descuento=0.0, impuesto=0.19)` admite múltiples variantes de invocación (tarifa estándar, aplicación de descuentos promocionales y ajuste de impuestos).

---

## 3. Manejo Avanzado de Excepciones y Logs
El sistema implementa una jerarquía de excepciones personalizadas en `src/excepciones.py` derivadas de `ErrorSistemaFJ`:
* `DatosInvalidosError`: Validación de nombres, correos electrónicos, teléfonos, tarifas negativas o capacidades inválidas.
* `ServicioNoDisponibleError`: Control de disponibilidad y restricciones de duración mínima o máxima por tipo de servicio.
* `ReservaInvalidaError`: Gestión de errores en creación, confirmación y cancelación de reservas.
* `CalculoInconsistenteError`: Verificación de rangos válidos en descuentos y cálculos financieros.

Además, se aplican:
* Bloques **`try / except / else / finally`** para controlar el flujo sin detener la ejecución.
* **Encadenamiento de excepciones (`raise ... from ...`)** en la clase `Reserva` para conservar la causa raíz del fallo.
* **Registro persistente (`logs/sistema.log`)** mediante la clase `RegistradorLogs`, documentando cada evento informativo (`INFO`) y error capturado (`ERROR`).

---

## 4. Estructura del Repositorio
```text
POO-UNAD-Fase4-AnyelinesRodriguez/
├── src/
│   ├── excepciones.py   # Jerarquía de excepciones personalizadas
│   └── modelos.py       # Clases abstractas, clientes, servicios, reservas y logger
├── logs/
│   └── sistema.log      # Historial generado automáticamente durante la ejecución
├── main.py              # Script principal con 12 operaciones simuladas
└── LÉAME.md             # Documentación técnica del proyecto
