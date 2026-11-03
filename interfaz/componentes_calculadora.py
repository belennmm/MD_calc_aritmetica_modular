"""Construcción del teclado sin lógica matemática."""
from tkinter import ttk
from collections.abc import Callable

def crear_teclado(contenedor, insertar: Callable, borrar: Callable, limpiar: Callable):
    filas = (("7", "8", "9", "/", "^"), ("4", "5", "6", "*", "("),
             ("1", "2", "3", "-", ")"), ("0", "Borrar", "Limpiar", "+", "="))
    for fila, valores in enumerate(filas):
        for columna, texto in enumerate(valores):
            accion = borrar if texto == "Borrar" else limpiar if texto == "Limpiar" else lambda valor=texto: insertar(valor)
            ttk.Button(contenedor, text=texto, command=accion).grid(row=fila, column=columna, sticky="nsew", padx=3, pady=3, ipady=8)
    for columna in range(5):
        contenedor.columnconfigure(columna, weight=1)
