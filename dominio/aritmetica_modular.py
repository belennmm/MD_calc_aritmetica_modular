"""Operaciones sobre el cuerpo de residuos de un primo."""
from dominio.numero_primo import ValidadorNumeroPrimo
from dominio.inverso_modular import CalculadorInversoModular
from dominio.excepciones_dominio import ErrorExponenteInvalido

class AritmeticaModular:
    def __init__(self, p: int):
        self.p = ValidadorNumeroPrimo().validar(p)

    def reducir(self, valor: int) -> int:
        return valor % self.p

    def sumar(self, a: int, b: int) -> int:
        return (a + b) % self.p

    def restar(self, a: int, b: int) -> int:
        return (a - b) % self.p

    def multiplicar(self, a: int, b: int) -> int:
        return (a * b) % self.p

    def dividir(self, a: int, b: int) -> int:
        return self.multiplicar(a, CalculadorInversoModular().calcular(b, self.p))

    def elevar(self, base: int, exponente: int) -> int:
        if isinstance(exponente, bool) or not isinstance(exponente, int) or exponente < 0:
            raise ErrorExponenteInvalido("El exponente debe ser un número entero no negativo.")
        return pow(base, exponente, self.p)
