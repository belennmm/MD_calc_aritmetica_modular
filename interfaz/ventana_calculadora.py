"""Adaptador gráfico Tkinter del caso de uso."""
import tkinter as tk
from tkinter import ttk, messagebox
from aplicacion.evaluar_expresion_modular import EvaluarExpresionModular
from dominio.excepciones_dominio import ErrorCalculadora
from interfaz.componentes_calculadora import crear_teclado
from interfaz.mensajes_usuario import INSTRUCCIONES

class VentanaCalculadora:
    def __init__(self, ventana: tk.Tk):
        self.ventana = ventana
        ventana.title("Calculadora de Aritmética Modular")
        ventana.minsize(540, 520)
        panel = ttk.Frame(ventana, padding=20)
        panel.pack(fill="both", expand=True)
        ttk.Label(panel, text="Calculadora de Aritmética Modular", font=("Segoe UI", 17, "bold")).pack(pady=(0, 16))
        ttk.Label(panel, text="Módulo primo p:").pack(anchor="w")
        self.modulo = ttk.Entry(panel, font=("Segoe UI", 13))
        self.modulo.pack(fill="x", pady=(4, 12))
        ttk.Label(panel, text="Expresión:").pack(anchor="w")
        self.expresion = ttk.Entry(panel, font=("Segoe UI", 16))
        self.expresion.pack(fill="x", pady=(4, 12))
        teclado = ttk.Frame(panel)
        teclado.pack(fill="x")
        crear_teclado(teclado, self.insertar, self.borrar, self.limpiar)
        ttk.Button(panel, text="Calcular", command=self.calcular).pack(fill="x", pady=10, ipady=7)
        self.resultado = tk.StringVar(value="Resultado: —")
        ttk.Label(panel, textvariable=self.resultado, font=("Segoe UI", 13), wraplength=490).pack(fill="x", pady=8)
        ttk.Button(panel, text="Instrucciones", command=lambda: messagebox.showinfo("Instrucciones", INSTRUCCIONES, parent=ventana)).pack(anchor="e")
        ventana.bind("<Return>", lambda evento: self.calcular())
        ventana.bind("<Escape>", lambda evento: self.limpiar())
        self.modulo.focus_set()

    def insertar(self, texto: str):
        if texto == "=":
            self.calcular()
            return
        self.expresion.insert(tk.INSERT, texto)
        self.expresion.focus_set()

    def borrar(self):
        if self.expresion.selection_present():
            self.expresion.delete(tk.SEL_FIRST, tk.SEL_LAST)
        else:
            posicion = self.expresion.index(tk.INSERT)
            if posicion:
                self.expresion.delete(posicion - 1, posicion)
        self.expresion.focus_set()

    def limpiar(self):
        self.expresion.delete(0, tk.END)
        self.resultado.set("Resultado: —")
        self.expresion.focus_set()

    def calcular(self):
        try:
            resultado = EvaluarExpresionModular().ejecutar(self.expresion.get(), self.modulo.get())
            self.resultado.set(f"Resultado: {resultado} (módulo {self.modulo.get().strip()})")
        except ErrorCalculadora as error:
            self.resultado.set(str(error))
        except Exception:
            self.resultado.set("No se pudo completar el cálculo. Revise la entrada.")
