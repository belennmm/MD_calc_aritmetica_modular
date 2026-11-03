"""Ventana de solo lectura para un procedimiento ya calculado."""
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from aplicacion.formatear_procedimiento import FormatearProcedimiento
from aplicacion.resultado_evaluacion import ResultadoEvaluacion

class VentanaProcedimiento:
    def __init__(self, padre, evaluacion: ResultadoEvaluacion):
        self.ventana = tk.Toplevel(padre)
        self.ventana.title("Procedimiento de cálculo")
        self.ventana.geometry("760x600")
        self.texto = ScrolledText(self.ventana, wrap="word", font=("Segoe UI", 12), padx=15, pady=15)
        self.texto.pack(fill="both", expand=True)
        self.texto.insert("1.0", FormatearProcedimiento().formatear(evaluacion))
        self.texto.configure(state="disabled")
