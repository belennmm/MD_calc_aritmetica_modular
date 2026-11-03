"""Unidad léxica con posición de origen."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Token:
    tipo: str
    texto: str
    posicion: int
