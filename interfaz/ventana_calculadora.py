"""Adaptador gráfico Tkinter del caso de uso."""
import tkinter as tk
from tkinter import ttk, messagebox
from aplicacion.evaluar_expresion_modular import EvaluarExpresionModular
from dominio.excepciones_dominio import ErrorCalculadora
from interfaz.componentes_calculadora import crear_teclado
from interfaz.ventana_procedimiento import VentanaProcedimiento
from interfaz.mensajes_usuario import INSTRUCCIONES

class VentanaCalculadora:
    def __init__(self, ventana: tk.Tk):
        self.ventana = ventana
        self.evaluacion = None
        self.ventana_procedimiento = None
        self.texto_modulo = tk.StringVar()
        self.texto_expresion = tk.StringVar()
        ventana.title("Calculadora de Aritmética Modular")
        ventana.minsize(540, 520)
        panel = ttk.Frame(ventana, padding=20)
        panel.pack(fill="both", expand=True)
        ttk.Label(panel, text="Calculadora de Aritmética Modular", font=("Segoe UI", 17, "bold")).pack(pady=(0, 16))
        self.resultado = tk.StringVar(value="")
        self.display_resultado = tk.Label(
            panel, textvariable=self.resultado, font=("Segoe UI", 18),
            background="#FAFBFC", foreground="#202830", anchor="e", justify="right",
            padx=14, pady=14, highlightthickness=1, highlightbackground="#CDD3DA",
            wraplength=470,
        )
        self.display_resultado.pack(fill="x", pady=(0, 14))
        ttk.Label(panel, text="Módulo primo p:", font=("Segoe UI", 12)).pack(anchor="w")
        self.modulo = ttk.Entry(panel, textvariable=self.texto_modulo, font=("Segoe UI", 13))
        self.modulo.pack(fill="x", pady=(4, 12))
        ttk.Label(panel, text="Expresión:", font=("Segoe UI", 12)).pack(anchor="w")
        self.expresion = ttk.Entry(panel, textvariable=self.texto_expresion, font=("Segoe UI", 16))
        self.expresion.pack(fill="x", pady=(4, 12))
        teclado = ttk.Frame(panel)
        teclado.pack(fill="x")
        crear_teclado(teclado, self.insertar, self.borrar, self.limpiar)
        marco_calcular = tk.Frame(panel, background="#0078D4", padx=1, pady=1)
        marco_calcular.pack(fill="x", pady=10)
        tk.Button(
            marco_calcular, text="Calcular", command=self.calcular,
            background="#CFE8FA", foreground="#20384B",
            activebackground="#BDDDF4", activeforeground="#20384B",
            relief="flat", borderwidth=1, font=("Segoe UI", 10),
        ).pack(fill="x", ipady=7)
        ttk.Button(panel, text="?", width=3, command=lambda: messagebox.showinfo("Instrucciones", INSTRUCCIONES, parent=ventana)).pack(anchor="e")
        self.boton_procedimiento = ttk.Button(panel, text="Ver procedimiento", state="disabled", command=self.ver_procedimiento)
        self.boton_procedimiento.pack(fill="x", pady=8)
        self.texto_modulo.trace_add("write", self.invalidar_procedimiento)
        self.texto_expresion.trace_add("write", self.invalidar_procedimiento)
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
        self.invalidar_procedimiento()
        self.expresion.delete(0, tk.END)
        self.resultado.set("")
        self.expresion.focus_set()

    def calcular(self):
        self.invalidar_procedimiento()
        try:
            resultado = EvaluarExpresionModular().ejecutar(self.expresion.get(), self.modulo.get())
            self.evaluacion = resultado
            self.boton_procedimiento.configure(state="normal")
            self.resultado.set(f"{resultado.resultado} (módulo {self.modulo.get().strip()})")
        except ErrorCalculadora as error:
            self.resultado.set("")
            messagebox.showerror("Error de cálculo", str(error), parent=self.ventana)
        except Exception:
            self.resultado.set("")
            messagebox.showerror("Error de cálculo", "No se pudo completar el cálculo. Revise la entrada.", parent=self.ventana)

    def invalidar_procedimiento(self, *argumentos):
        self.evaluacion = None
        self.boton_procedimiento.configure(state="disabled")
        if self.ventana_procedimiento is not None:
            if self.ventana_procedimiento.ventana.winfo_exists():
                self.ventana_procedimiento.ventana.destroy()
            self.ventana_procedimiento = None

    def ver_procedimiento(self):
        if self.evaluacion is None:
            return
        if self.ventana_procedimiento is not None and self.ventana_procedimiento.ventana.winfo_exists():
            self.ventana_procedimiento.ventana.lift()
            return
        self.ventana_procedimiento = VentanaProcedimiento(self.ventana, self.evaluacion)
