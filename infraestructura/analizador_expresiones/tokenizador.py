"""Reconoce exclusivamente enteros, espacios y operadores permitidos."""
from infraestructura.analizador_expresiones.token import Token
from dominio.excepciones_dominio import ErrorOperadorInvalido, ErrorExpresionVacia

class Tokenizador:
    def tokenizar(self, expresion: str) -> list[Token]:
        if not expresion.strip():
            raise ErrorExpresionVacia("Debe ingresar una expresión.")
        tokens = []
        posicion = 0
        while posicion < len(expresion):
            caracter = expresion[posicion]
            if caracter.isspace():
                posicion += 1
                continue
            inicio = posicion
            if caracter in "0123456789":
                while posicion < len(expresion) and expresion[posicion] in "0123456789":
                    posicion += 1
                tokens.append(Token("entero", expresion[inicio:posicion], inicio))
                continue
            if caracter not in "+-*/^()":
                raise ErrorOperadorInvalido("La expresión contiene caracteres no permitidos.")
            tokens.append(Token(caracter, caracter, posicion))
            posicion += 1
        tokens.append(Token("fin", "", posicion))
        return tokens
