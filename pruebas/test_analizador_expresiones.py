import unittest
from aplicacion.evaluar_expresion_modular import EvaluarExpresionModular
from dominio.excepciones_dominio import ErrorCalculadora, ErrorExponenteInvalido

class PruebasExpresiones(unittest.TestCase):
    def test_precedencia_y_exponentes(self):
        caso = EvaluarExpresionModular()
        for expresion, esperado in [('2^8', 4), ('2^(3+5)', 4), ('2^(6/2)', 1),
                ('2^3^2', 1), ('-2^2', 3), ('(-2)^2', 4), ('3-8', 2),
                ('5*-2', 4), ('7    +    5', 5), ('2^(8-7)', 2)]:
            with self.subTest(expresion=expresion):
                self.assertEqual(caso.ejecutar(expresion, 7).resultado, esperado)
        for expresion in ('2^-3', '2^(2-5)', '2^(3/2)', '2^(1/0)'):
            with self.subTest(expresion=expresion), self.assertRaises(ErrorExponenteInvalido):
                caso.ejecutar(expresion, 7)

    def test_entradas_incorrectas(self):
        caso = EvaluarExpresionModular()
        for expresion in ('', '2+a', '(5+3', '5+()', '5**3', '7+4*', '*5+2',
                          '5/7', '10/(8-1)', '+5', '5/', '(3+)', '2(3+4)', '2 3', '3)(2'):
            with self.subTest(expresion=expresion), self.assertRaises(ErrorCalculadora):
                caso.ejecutar(expresion, 7)
