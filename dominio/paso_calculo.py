"""Datos inmutables de las operaciones realizadas, sin presentación."""
from dataclasses import dataclass
from fractions import Fraction

@dataclass(frozen=True)
class PasoEuclides:
    dividendo: int
    divisor: int
    cociente: int
    resto: int

@dataclass(frozen=True)
class PasoCalculo:
    tipo: str
    izquierdo: int | Fraction
    derecho: int | Fraction | None
    modulo: int | None
    resultado: int | Fraction
    pasos_euclides: tuple[PasoEuclides, ...] = ()
    coeficiente: int | None = None
    divisor_reducido: int | None = None
    inverso: int | None = None
