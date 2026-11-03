"""Estado del procedimiento en la interfaz Tkinter."""
import tkinter as tk
import unittest
from interfaz.ventana_calculadora import VentanaCalculadora

class PruebasInterfazProcedimiento(unittest.TestCase):
    def setUp(self):
        self.raiz = tk.Tk()
        self.raiz.withdraw()
        self.calculadora = VentanaCalculadora(self.raiz)

    def tearDown(self):
        self.raiz.destroy()

    def test_disponibilidad_y_ventana(self):
        calculadora = self.calculadora
        self.assertTrue(calculadora.boton_procedimiento.instate(['disabled']))
        calculadora.texto_modulo.set('37')
        calculadora.texto_expresion.set('(8*(13+5^2)-3^3)/(2^4+1)')
        calculadora.calcular()
        self.assertTrue(calculadora.boton_procedimiento.instate(['!disabled']))
        calculadora.ver_procedimiento()
        ventana = calculadora.ventana_procedimiento
        self.assertEqual(ventana.ventana.title(),'Procedimiento de cálculo')
        self.assertEqual(str(ventana.texto.cget('state')),'disabled')
        self.assertTrue(ventana.texto.vbar.winfo_exists())
        self.assertIn('Resultado final:\n25', ventana.texto.get('1.0','end'))
        calculadora.texto_expresion.set('1/37')
        self.assertTrue(calculadora.boton_procedimiento.instate(['disabled']))
        self.assertFalse(ventana.ventana.winfo_exists())
        calculadora.calcular()
        self.assertIsNone(calculadora.evaluacion)
        self.assertTrue(calculadora.boton_procedimiento.instate(['disabled']))
        calculadora.texto_expresion.set('1+2')
        calculadora.calcular()
        calculadora.texto_modulo.set('7')
        self.assertIsNone(calculadora.evaluacion)
        self.assertTrue(calculadora.boton_procedimiento.instate(['disabled']))
        calculadora.calcular()
        calculadora.limpiar()
        self.assertIsNone(calculadora.evaluacion)
        self.assertTrue(calculadora.boton_procedimiento.instate(['disabled']))
