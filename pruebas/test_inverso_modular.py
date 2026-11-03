import unittest
from dominio.inverso_modular import CalculadorInversoModular
from dominio.excepciones_dominio import ErrorDivisionModular

class PruebasInverso(unittest.TestCase):
    def test_euclides(self):
        calculador = CalculadorInversoModular()
        for primo in (2, 5, 7, 23):
            for numero in range(1, primo):
                self.assertEqual(numero * calculador.calcular(numero, primo) % primo, 1)
        self.assertEqual(calculador.calcular(-2, 5), 2)
        with self.assertRaises(ErrorDivisionModular):
            calculador.calcular(14, 7)
