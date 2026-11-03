"""Inversos mediante el algoritmo extendido de Euclides."""
from dominio.excepciones_dominio import ErrorDivisionModular

class CalculadorInversoModular:
    def calcular(self, valor: int, modulo: int) -> int:
        resto_anterior, resto = modulo, valor % modulo
        coeficiente_anterior, coeficiente = 0, 1
        while resto:
            cociente = resto_anterior // resto
            resto_anterior, resto = resto, resto_anterior - cociente * resto
            coeficiente_anterior, coeficiente = coeficiente, coeficiente_anterior - cociente * coeficiente
        if resto_anterior != 1:
            raise ErrorDivisionModular("No es posible dividir entre cero en aritmética modular.")
        return coeficiente_anterior % modulo
