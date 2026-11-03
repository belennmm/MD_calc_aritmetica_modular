"""Errores controlados de la calculadora."""
class ErrorCalculadora(ValueError):
    """Error que puede presentarse directamente al usuario."""

class ErrorModuloInvalido(ErrorCalculadora): pass
class ErrorModuloNoPrimo(ErrorModuloInvalido): pass
class ErrorExpresionVacia(ErrorCalculadora): pass
class ErrorExpresionInvalida(ErrorCalculadora): pass
class ErrorParentesisDesbalanceados(ErrorExpresionInvalida): pass
class ErrorOperadorInvalido(ErrorExpresionInvalida): pass
class ErrorDivisionModular(ErrorCalculadora): pass
class ErrorExponenteInvalido(ErrorCalculadora): pass
