"""Orquesta validación, análisis y evaluación."""
from aplicacion.resultado_evaluacion import ResultadoEvaluacion
from aplicacion.validar_solicitud_calculo import ValidarSolicitudCalculo
from dominio.aritmetica_modular import AritmeticaModular
from dominio.excepciones_dominio import ErrorExpresionInvalida
from infraestructura.analizador_expresiones.tokenizador import Tokenizador
from infraestructura.analizador_expresiones.analizador_sintactico import AnalizadorSintactico

class EvaluarExpresionModular:
    def ejecutar(self, expresion: str, modulo: str | int) -> ResultadoEvaluacion:
        primo = ValidarSolicitudCalculo().validar(expresion, modulo)
        try:
            tokens = Tokenizador().tokenizar(expresion)
            pasos = []
            resultado = AnalizadorSintactico().evaluar(tokens, AritmeticaModular(primo, pasos))
            return ResultadoEvaluacion(resultado, tuple(pasos), expresion, primo)
        except (RecursionError, OverflowError, MemoryError):
            raise ErrorExpresionInvalida("La expresión es demasiado compleja para calcularla.") from None
        except ValueError as error:
            from dominio.excepciones_dominio import ErrorCalculadora
            if isinstance(error, ErrorCalculadora):
                raise
            raise ErrorExpresionInvalida("Los números de la expresión son demasiado grandes.") from None
