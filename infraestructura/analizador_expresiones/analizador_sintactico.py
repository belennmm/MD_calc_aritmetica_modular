"""Descenso recursivo: potencia asociativa a la derecha y menos unario.

Se construye un árbol antes de calcular. Las ramas usadas como exponentes se
interpretan con aritmética racional exacta; cada resultado debe ser entero no
negativo. El resto del árbol usa exclusivamente operaciones del dominio.
"""
from dataclasses import dataclass
from fractions import Fraction
from dominio.aritmetica_modular import AritmeticaModular
from dominio.excepciones_dominio import (
    ErrorExpresionInvalida, ErrorParentesisDesbalanceados,
    ErrorOperadorInvalido, ErrorExponenteInvalido,
)
from infraestructura.analizador_expresiones.token import Token

@dataclass
class Nodo:
    operador: str
    valor: int = 0
    izquierdo: 'Nodo | None' = None
    derecho: 'Nodo | None' = None

class AnalizadorSintactico:
    def evaluar(self, tokens: list[Token], aritmetica: AritmeticaModular) -> int:
        self.tokens, self.posicion = tokens, 0
        balance = 0
        for token in tokens:
            balance += (token.tipo == "(") - (token.tipo == ")")
            if balance < 0:
                raise ErrorParentesisDesbalanceados("Los paréntesis de la expresión no están balanceados.")
        if balance:
            raise ErrorParentesisDesbalanceados("Los paréntesis de la expresión no están balanceados.")
        if self.actual in ("+", "*", "/", "^"):
            raise ErrorOperadorInvalido("La expresión no puede comenzar con ese operador.")
        raiz = self.expresion()
        if self.actual != "fin":
            raise ErrorExpresionInvalida("Utilice * para indicar multiplicación.")
        return self.calcular(raiz, aritmetica)

    @property
    def actual(self) -> str:
        return self.tokens[self.posicion].tipo

    def consumir(self) -> str:
        texto = self.tokens[self.posicion].texto
        self.posicion += 1
        return texto

    def expresion(self) -> Nodo:
        nodo = self.producto()
        while self.actual in ("+", "-"):
            operador = self.consumir()
            nodo = Nodo(operador, izquierdo=nodo, derecho=self.producto())
        return nodo

    def producto(self) -> Nodo:
        nodo = self.unario()
        while self.actual in ("*", "/"):
            operador = self.consumir()
            nodo = Nodo(operador, izquierdo=nodo, derecho=self.unario())
        return nodo

    def unario(self) -> Nodo:
        if self.actual == "-":
            self.consumir()
            return Nodo("negativo", izquierdo=self.unario())
        return self.potencia()

    def potencia(self) -> Nodo:
        nodo = self.primario()
        if self.actual == "^":
            self.consumir()
            nodo = Nodo("^", izquierdo=nodo, derecho=self.unario())
        return nodo

    def primario(self) -> Nodo:
        if self.actual == "entero":
            return Nodo("entero", valor=int(self.consumir()))
        if self.actual == "(":
            self.consumir()
            if self.actual == ")":
                raise ErrorExpresionInvalida("No se permiten paréntesis vacíos.")
            nodo = self.expresion()
            if self.actual != ")":
                raise ErrorExpresionInvalida("Utilice * para indicar multiplicación.")
            self.consumir()
            return nodo
        if self.actual in ("fin", ")"):
            raise ErrorExpresionInvalida("La expresión está incompleta.")
        raise ErrorOperadorInvalido("La expresión contiene operadores consecutivos no válidos.")

    def exponente(self, nodo: Nodo) -> int:
        try:
            valor = self.calcular_entero(nodo)
        except ZeroDivisionError:
            raise ErrorExponenteInvalido("El exponente debe ser un número entero no negativo.") from None
        if valor.denominator != 1 or valor < 0:
            raise ErrorExponenteInvalido("El exponente debe ser un número entero no negativo.")
        return int(valor)

    def calcular_entero(self, nodo: Nodo) -> Fraction:
        if nodo.operador == "entero":
            return Fraction(nodo.valor)
        izquierdo = self.calcular_entero(nodo.izquierdo)
        if nodo.operador == "negativo":
            return -izquierdo
        if nodo.operador == "^":
            return izquierdo ** self.exponente(nodo.derecho)
        derecho = self.calcular_entero(nodo.derecho)
        if nodo.operador == "+": return izquierdo + derecho
        if nodo.operador == "-": return izquierdo - derecho
        if nodo.operador == "*": return izquierdo * derecho
        return izquierdo / derecho

    def calcular(self, nodo: Nodo, aritmetica: AritmeticaModular) -> int:
        if nodo.operador == "entero":
            return aritmetica.reducir(nodo.valor)
        izquierdo = self.calcular(nodo.izquierdo, aritmetica)
        if nodo.operador == "negativo":
            return aritmetica.restar(0, izquierdo)
        if nodo.operador == "^":
            return aritmetica.elevar(izquierdo, self.exponente(nodo.derecho))
        derecho = self.calcular(nodo.derecho, aritmetica)
        operaciones = {"+": aritmetica.sumar, "-": aritmetica.restar,
                       "*": aritmetica.multiplicar, "/": aritmetica.dividir}
        return operaciones[nodo.operador](izquierdo, derecho)
