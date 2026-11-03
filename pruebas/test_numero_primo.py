import unittest
from dominio.numero_primo import ValidadorNumeroPrimo
from dominio.excepciones_dominio import ErrorModuloInvalido

class PruebasPrimalidad(unittest.TestCase):
    def test_primos(self):
        validador = ValidadorNumeroPrimo()
        for primo in (2, 3, 23, 29, 31, 37, 41, 97):
            self.assertEqual(validador.validar(str(primo)), primo)
        for valor in (None, '', 'abc', 0, 1, -7, 4, 49, 91, 2.5, True):
            with self.subTest(valor=valor), self.assertRaises(ErrorModuloInvalido):
                validador.validar(valor)
