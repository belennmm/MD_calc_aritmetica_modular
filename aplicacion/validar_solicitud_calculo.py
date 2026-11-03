"""Validaciones de entrada del caso de uso."""
from dominio.numero_primo import ValidadorNumeroPrimo
from dominio.excepciones_dominio import ErrorExpresionVacia

class ValidarSolicitudCalculo:
    def validar(self, expresion: str, modulo: str | int) -> int:
        primo = ValidadorNumeroPrimo().validar(modulo)
        if not isinstance(expresion, str) or not expresion.strip():
            raise ErrorExpresionVacia("Debe ingresar una expresión.")
        return primo
