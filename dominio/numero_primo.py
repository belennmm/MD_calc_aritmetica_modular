"""Validación del módulo primo."""
from math import isqrt
from dominio.excepciones_dominio import ErrorModuloInvalido, ErrorModuloNoPrimo

class ValidadorNumeroPrimo:
    def validar(self, valor: str | int) -> int:
        if valor is None or str(valor).strip() == "":
            raise ErrorModuloInvalido("Debe ingresar un número primo para p.")
        if isinstance(valor, bool) or not isinstance(valor, (str, int)):
            raise ErrorModuloInvalido("El módulo p debe ser un número entero.")
        try:
            primo = int(valor)
        except ValueError:
            raise ErrorModuloInvalido("El módulo p debe ser un número entero.") from None
        if primo <= 1:
            raise ErrorModuloInvalido("El módulo p debe ser mayor que 1.")
        if not self.es_primo(primo):
            raise ErrorModuloNoPrimo("El valor de p debe ser un número primo.")
        return primo

    @staticmethod
    def es_primo(numero: int) -> bool:
        if numero < 2:
            return False
        if numero % 2 == 0:
            return numero == 2
        return all(numero % divisor for divisor in range(3, isqrt(numero) + 1, 2))
