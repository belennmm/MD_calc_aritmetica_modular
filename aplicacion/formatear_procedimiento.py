"""Presentación del registro sin volver a evaluar la expresión."""
from aplicacion.resultado_evaluacion import ResultadoEvaluacion
from dominio.paso_calculo import PasoCalculo

class FormatearProcedimiento:
    def formatear(self, evaluacion: ResultadoEvaluacion) -> str:
        bloques = [f"Módulo utilizado: {evaluacion.modulo}",
                   f"Expresión original:\n{evaluacion.expresion}"]
        nombres = {"sumar": "Suma", "restar": "Resta", "multiplicar": "Multiplicación",
                   "elevar": "Potencia", "dividir": "División", "inverso": "Inverso multiplicativo",
                   "negativo": "Signo negativo"}
        numero = 0
        indice = 0
        while indice < len(evaluacion.pasos):
            paso = evaluacion.pasos[indice]
            indice += 1
            if (paso.tipo == "inverso" and indice + 1 < len(evaluacion.pasos)
                    and evaluacion.pasos[indice].tipo == "multiplicar"
                    and evaluacion.pasos[indice + 1].tipo == "dividir"):
                division = evaluacion.pasos[indice + 1]
                numero += 1
                contenido = self.formatear_inverso(paso) + "\n\n" + self.formatear_paso(division)
                bloques.append(f"{numero}. División modular\n{contenido}")
                indice += 2
                continue
            if paso.tipo == "reduccion":
                reducciones = [paso] if paso.izquierdo != paso.resultado else []
                while indice < len(evaluacion.pasos) and evaluacion.pasos[indice].tipo == "reduccion":
                    siguiente = evaluacion.pasos[indice]
                    if siguiente.izquierdo != siguiente.resultado:
                        reducciones.append(siguiente)
                    indice += 1
                if reducciones:
                    titulo = "Reducción" if len(reducciones) == 1 else "Reducciones"
                    lineas = "\n".join(self.formatear_paso(reduccion) for reduccion in reducciones)
                    bloques.append(f"{titulo} módulo {paso.modulo}:\n{lineas}")
                continue
            contenido = self.formatear_paso(paso)
            if paso.tipo == "exponente":
                bloques.append(contenido)
                continue
            numero += 1
            contexto = "modular" if paso.modulo is not None else "en el exponente"
            bloques.append(f"{numero}. {nombres[paso.tipo]} {contexto}\n{contenido}")
        bloques.append(f"Resultado final:\n{evaluacion.resultado} (mod {evaluacion.modulo})")
        return "\n\n".join(bloques)

    def formatear_paso(self, paso: PasoCalculo) -> str:
        a, b, resultado, modulo = paso.izquierdo, paso.derecho, paso.resultado, paso.modulo
        if paso.tipo == "inverso":
            return self.formatear_inverso(paso)
        if paso.tipo == "exponente":
            return f"Exponente utilizado: {resultado}"
        if paso.tipo == "reduccion":
            return f"{a} ≡ {resultado} (mod {modulo})" if a != resultado else ""
        if paso.tipo == "dividir" and modulo is not None:
            return (f"Entonces:\n{a} / {b}\n≡ {a} * {paso.divisor_reducido}^(-1)\n"
                    f"≡ {a} * {paso.inverso}\n≡ {resultado} (mod {modulo})")
        signos = {"sumar": "+", "restar": "-", "multiplicar": "*", "dividir": "/", "elevar": "^"}
        if paso.tipo == "negativo":
            operacion = f"-({a})"
        elif paso.tipo == "elevar":
            operacion = f"{a}^{b}"
        else:
            operacion = f"{a} {signos[paso.tipo]} {b}"
        if modulo is None:
            return f"Exponente, aritmética exacta: {operacion} = {resultado}"
        return f"{operacion} ≡ {resultado} (mod {modulo})"

    @staticmethod
    def combinacion(terminos: dict[int, int]) -> str:
        partes = []
        for valor, coeficiente in terminos.items():
            if not coeficiente:
                continue
            magnitud = abs(coeficiente)
            termino = str(valor) if magnitud == 1 else f"{magnitud}({valor})"
            prefijo = ("-" if coeficiente < 0 else "") if not partes else (" - " if coeficiente < 0 else " + ")
            partes.append(prefijo + termino)
        return "".join(partes) or "0"

    def formatear_inverso(self, paso: PasoCalculo) -> str:
        divisor, modulo = paso.divisor_reducido, paso.modulo
        lineas = [f"Se busca el inverso multiplicativo de {divisor} módulo {modulo}.",
                  "Algoritmo extendido de Euclides:"]
        lineas.extend(f"{p.dividendo} = {p.cociente}({p.divisor}) + {p.resto}"
                      for p in paso.pasos_euclides if p.resto != 0)
        lineas.append("Sustitución hacia atrás:")
        terminos = {1: 1}
        primera_sustitucion = True
        for division in reversed(paso.pasos_euclides):
            if division.resto == 0 or not terminos.get(division.resto):
                continue
            coeficiente = terminos[division.resto]
            if not primera_sustitucion:
                producto = (str(division.divisor) if division.cociente == 1
                            else f"{division.cociente}({division.divisor})")
                sustitucion = f"({division.dividendo} - {producto})"
                partes = []
                for valor, factor in terminos.items():
                    if not factor:
                        continue
                    if valor == division.resto:
                        termino = sustitucion if abs(factor) == 1 else f"{abs(factor)}{sustitucion}"
                    else:
                        termino = str(valor) if abs(factor) == 1 else f"{abs(factor)}({valor})"
                    signo = ("-" if factor < 0 else "") if not partes else (" - " if factor < 0 else " + ")
                    partes.append(signo + termino)
                lineas.append("1 = " + "".join(partes))
            terminos.pop(division.resto)
            terminos[division.dividendo] = terminos.get(division.dividendo, 0) + coeficiente
            terminos[division.divisor] = terminos.get(division.divisor, 0) - coeficiente * division.cociente
            lineas.append("1 = " + self.combinacion(terminos))
            primera_sustitucion = False
        if primera_sustitucion:
            lineas.append("1 = 1")
        coeficiente_visible = f"{paso.coeficiente} ≡ " if paso.coeficiente != paso.inverso else ""
        lineas.append(f"Por tanto:\n{divisor}^(-1) ≡ {coeficiente_visible}{paso.inverso} (mod {modulo})")
        return "\n".join(lineas)
