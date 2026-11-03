"""Operaciones sobre el cuerpo de residuos de un primo."""
from dominio.paso_calculo import PasoCalculo
from dominio.numero_primo import ValidadorNumeroPrimo
from dominio.inverso_modular import CalculadorInversoModular
from dominio.excepciones_dominio import ErrorExponenteInvalido

class AritmeticaModular:
    def __init__(self, p: int, pasos: list[PasoCalculo] | None = None):
        self.pasos = pasos
        self.p = ValidadorNumeroPrimo().validar(p)

    def registrar(self, tipo: str, a: int, b: int | None, resultado: int) -> int:
        if self.pasos is not None:
            self.pasos.append(PasoCalculo(tipo, a, b, self.p, resultado))
        return resultado

    def reducir(self, valor: int) -> int:
        return self.registrar("reduccion", valor, None, valor % self.p)

    def sumar(self, a: int, b: int) -> int:
        return self.registrar("sumar", a, b, (a + b) % self.p)

    def restar(self, a: int, b: int) -> int:
        return self.registrar("restar", a, b, (a - b) % self.p)

    def multiplicar(self, a: int, b: int) -> int:
        return self.registrar("multiplicar", a, b, (a * b) % self.p)

    def dividir(self, a: int, b: int) -> int:
        inverso = CalculadorInversoModular(self.pasos).calcular(b, self.p)
        resultado = self.multiplicar(a, inverso)
        if self.pasos is not None:
            self.pasos.append(PasoCalculo("dividir", a, b, self.p, resultado,
                divisor_reducido=b % self.p, inverso=inverso))
        return resultado

    def elevar(self, base: int, exponente: int) -> int:
        if isinstance(exponente, bool) or not isinstance(exponente, int) or exponente < 0:
            raise ErrorExponenteInvalido("El exponente debe ser un número entero no negativo.")
        return self.registrar("elevar", base, exponente, pow(base, exponente, self.p))
