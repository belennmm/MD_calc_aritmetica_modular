"""Comprobaciones del registro y su presentación sin reevaluar."""
import unittest
import re
from unittest.mock import patch
from aplicacion.evaluar_expresion_modular import EvaluarExpresionModular
from aplicacion.formatear_procedimiento import FormatearProcedimiento
from dominio.aritmetica_modular import AritmeticaModular
from dominio.excepciones_dominio import ErrorDivisionModular

class PruebasProcedimiento(unittest.TestCase):
    def evaluar(self, expresion, modulo):
        return EvaluarExpresionModular().ejecutar(expresion, modulo)

    def test_cinco_ejemplos_con_registro(self):
        ejemplos = [('(7^3+4*5)*2',23,13), ('((15+7)*3-2^4)/5',29,10),
                    ('(3^4*2+7)/(11-5^2)',31,30),
                    ('(8*(13+5^2)-3^3)/(2^4+1)',37,25),
                    ('((6^2*3+7)/(2^3-5))*(11+4^3)-9',41,37)]
        for expresion, modulo, esperado in ejemplos:
            with self.subTest(expresion=expresion):
                evaluacion = self.evaluar(expresion, modulo)
                self.assertEqual(evaluacion.resultado, esperado)
                self.assertEqual(evaluacion.pasos[-1].resultado, esperado)
                self.assertEqual(evaluacion.expresion, expresion)
                self.assertEqual(evaluacion.modulo, modulo)

    def test_euclides_y_orden_real(self):
        evaluacion = self.evaluar('(8*(13+5^2)-3^3)/(2^4+1)',37)
        inverso = next(p for p in evaluacion.pasos if p.tipo == 'inverso')
        self.assertEqual((inverso.divisor_reducido, inverso.coeficiente, inverso.inverso), (17,-13,24))
        self.assertEqual([(p.dividendo,p.divisor,p.cociente,p.resto) for p in inverso.pasos_euclides],
                         [(37,17,2,3),(17,3,5,2),(3,2,1,1),(2,1,2,0)])
        self.assertEqual([p.tipo for p in evaluacion.pasos[-3:]], ['inverso','multiplicar','dividir'])
        self.assertEqual((evaluacion.pasos[-2].izquierdo,evaluacion.pasos[-2].derecho), (18,24))
        texto = FormatearProcedimiento().formatear(evaluacion)
        self.assertIn('17^(-1) ≡ -13 ≡ 24 (mod 37)', texto)
        # Comprobar la identidad de Bézout sin imponer el orden de los términos.
        igualdad = [linea for linea in texto.splitlines() if linea.startswith('1 = ')][-1]
        expresion = igualdad.partition('=')[2].replace(' ', '')
        terminos = re.findall(r'([+-]?\d+)\((\d+)\)', expresion)
        self.assertEqual(''.join(f'{coeficiente}({valor})' for coeficiente, valor in terminos),
                         expresion.lstrip('+'))
        coeficientes = {int(valor): int(coeficiente) for coeficiente, valor in terminos}
        self.assertEqual(coeficientes, {17: -13, 37: 6})
        self.assertEqual(sum(valor * coeficiente for valor, coeficiente in coeficientes.items()), 1)

    def test_varias_divisiones_e_inversos(self):
        evaluacion = self.evaluar('1/2+3/4',7)
        self.assertEqual(evaluacion.resultado,3)
        inversos = [p for p in evaluacion.pasos if p.tipo == 'inverso']
        self.assertEqual([(p.divisor_reducido,p.inverso) for p in inversos], [(2,4),(4,2)])
        self.assertEqual([p.tipo for p in evaluacion.pasos if p.tipo not in ('reduccion',)],
            ['inverso','multiplicar','dividir','inverso','multiplicar','dividir','sumar'])
        for primo in (2,5,7,23,37):
            for divisor in range(1,primo):
                registro = []
                resultado = AritmeticaModular(primo,registro).dividir(1,divisor)
                inverso = registro[0]
                self.assertEqual(divisor*resultado % primo,1)
                for paso in inverso.pasos_euclides:
                    self.assertEqual(paso.dividendo,paso.cociente*paso.divisor+paso.resto)
                FormatearProcedimiento().formatear_paso(inverso)

    def test_negativos_exponentes_y_parentesis(self):
        evaluacion = self.evaluar('((-2)^((3+5))+(3-8))',7)
        self.assertEqual(evaluacion.resultado,6)
        potencia = next(p for p in evaluacion.pasos if p.tipo == 'elevar' and p.modulo == 7)
        self.assertEqual(potencia.derecho,8)
        entero = next(p for p in evaluacion.pasos if p.tipo == 'sumar' and p.modulo is None)
        self.assertEqual((entero.izquierdo,entero.derecho,entero.resultado),(3,5,8))
        texto = FormatearProcedimiento().formatear(evaluacion)
        self.assertIn('Exponente utilizado: 8', texto)
        self.assertIn('0 - 2 ≡ 5 (mod 7)', texto)
        self.assertEqual(self.evaluar('2^(6/2)',7).resultado,1)

    def test_denominador_cero(self):
        with self.assertRaises(ErrorDivisionModular):
            self.evaluar('10/(8-1)',7)

    def test_formatear_no_recalcula(self):
        evaluacion = self.evaluar('1/2+2^(3+5)',7)
        with patch.object(AritmeticaModular, 'dividir', side_effect=AssertionError('Reevaluación')):
            texto = FormatearProcedimiento().formatear(evaluacion)
        self.assertIn('Resultado final:\n1 (mod 7)',texto)

    def test_presentacion_division_agrupada(self):
        evaluacion = self.evaluar('33/3', 41)
        texto = FormatearProcedimiento().formatear(evaluacion)
        self.assertIn('1. División modular', texto)
        self.assertNotIn('Multiplicación modular', texto)
        self.assertNotIn('Inverso multiplicativo modular', texto)
        self.assertIn('41 = 13(3) + 2', texto)
        self.assertIn('1 = 3 - 2', texto)
        self.assertIn('1 = 3 - (41 - 13(3))', texto)
        self.assertIn('1 = 14(3) - 41', texto)
        self.assertIn('3^(-1) ≡ 14 (mod 41)', texto)
        self.assertNotIn('(0)', texto)
        self.assertIn('≡ 33 * 14\n≡ 11 (mod 41)', texto)
        self.assertEqual(FormatearProcedimiento().formatear(self.evaluar('1/2+3/4',7)).count('División modular'),2)

    def test_congruencias_y_exponentes_visibles(self):
        texto = FormatearProcedimiento().formatear(self.evaluar('6^2*3+1-2',41))
        self.assertIn('6^2 ≡ 36 (mod 41)', texto)
        self.assertIn('36 * 3 ≡ 26 (mod 41)', texto)
        self.assertIn('26 + 1 ≡ 27 (mod 41)', texto)
        self.assertIn('27 - 2 ≡ 25 (mod 41)', texto)
        self.assertIn('Exponente utilizado: 2', texto)
        for linea in texto.splitlines():
            if '(mod ' in linea:
                self.assertNotIn(' = ', linea)
