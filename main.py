"""Punto de entrada de la Calculadora de Aritmética Modular."""
import tkinter as tk
from interfaz.ventana_calculadora import VentanaCalculadora

def main():
    ventana = tk.Tk()
    VentanaCalculadora(ventana)
    ventana.mainloop()

if __name__ == "__main__":
    main()
