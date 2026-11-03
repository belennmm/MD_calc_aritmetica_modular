import unittest
from aplicacion.evaluar_expresion_modular import EvaluarExpresionModular

class PruebasCasosUso(unittest.TestCase):
    def test_ejemplos_obligatorios(self):
        ejemplos = [
            ('(7^3 + 4*5)*2', 23, 13),
            ('((15+7)*3-2^4)/5', 29, 10),
            ('(3^4*2+7)/(11-5^2)', 31, 30),
            ('(8*(13+5^2)-3^3)/(2^4+1)', 37, 25),
            ('((6^2*3+7)/(2^3-5))*(11+4^3)-9', 41, 37),
        ]
        for expresion, modulo, esperado in ejemplos:
            with self.subTest(expresion=expresion):
                self.assertEqual(EvaluarExpresionModular().ejecutar(expresion, modulo).resultado, esperado)
