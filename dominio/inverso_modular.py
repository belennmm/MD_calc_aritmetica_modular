"""Inversos mediante el algoritmo extendido de Euclides."""
from dominio.paso_calculo import PasoCalculo, PasoEuclides
from dominio.excepciones_dominio import ErrorDivisionModular

class CalculadorInversoModular:
    def __init__(self, pasos: list[PasoCalculo] | None = None):
        self.pasos = pasos

    def calcular(self, valor: int, modulo: int) -> int:
        pasos_euclides = []
        resto_anterior, resto = modulo, valor % modulo
        coeficiente_anterior, coeficiente = 0, 1
        while resto:
            cociente = resto_anterior // resto
            pasos_euclides.append(PasoEuclides(resto_anterior, resto, cociente, resto_anterior - cociente * resto))
            resto_anterior, resto = resto, resto_anterior - cociente * resto
            coeficiente_anterior, coeficiente = coeficiente, coeficiente_anterior - cociente * coeficiente
        if resto_anterior != 1:
            raise ErrorDivisionModular("No es posible dividir entre cero en aritmética modular.")
        inverso = coeficiente_anterior % modulo
        if self.pasos is not None:
            self.pasos.append(PasoCalculo("inverso", valor, None, modulo, inverso,
                tuple(pasos_euclides), coeficiente_anterior, valor % modulo, inverso))
        return inverso
