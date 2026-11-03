"""Resultado completo de una evaluación correcta."""
from dataclasses import dataclass
from dominio.paso_calculo import PasoCalculo

@dataclass(frozen=True)
class ResultadoEvaluacion:
    resultado: int
    pasos: tuple[PasoCalculo, ...]
    expresion: str
    modulo: int
