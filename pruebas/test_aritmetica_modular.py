import unittest
from dominio.aritmetica_modular import AritmeticaModular
from dominio.excepciones_dominio import ErrorExponenteInvalido

class PruebasAritmetica(unittest.TestCase):
    def test_operaciones(self):
        aritmetica = AritmeticaModular(7)
        self.assertEqual(aritmetica.sumar(6, 5), 4)
        self.assertEqual(aritmetica.restar(3, 8), 2)
        self.assertEqual(aritmetica.multiplicar(5, 6), 2)
        self.assertEqual(aritmetica.elevar(2, 8), 4)
        self.assertEqual(aritmetica.reducir(-1), 6)
        self.assertEqual(AritmeticaModular(5).dividir(1, 2), 3)
        with self.assertRaises(ErrorExponenteInvalido):
            aritmetica.elevar(2, -3)
