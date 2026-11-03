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
        for paso in evaluacion.pasos:
            if paso.tipo == "reduccion":
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
            return ""
        if paso.tipo == "dividir" and modulo is not None:
            return (f"Entonces: {a} / {b} ≡ {a} * {paso.divisor_reducido}^(-1) "
                    f"≡ {a} * {paso.inverso} ≡ {resultado} (mod {modulo})")
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
        lineas.extend(f"{p.dividendo} = {p.cociente}({p.divisor}) + {p.resto}" for p in paso.pasos_euclides)
        lineas.append("Sustitución hacia atrás:")
        terminos = {1: 1}
        lineas.append("1 = 1")
        for division in reversed(paso.pasos_euclides):
            if division.resto == 0 or division.resto not in terminos:
                continue
            coeficiente = terminos.pop(division.resto)
            if not coeficiente:
                continue
            sustitucion = f"({division.dividendo} - {division.cociente}({division.divisor}))"
            resto = self.combinacion(terminos)
            lineas.append(f"1 = ({resto}) + ({coeficiente}) * {sustitucion}")
            terminos[division.dividendo] = terminos.get(division.dividendo, 0) + coeficiente
            terminos[division.divisor] = terminos.get(division.divisor, 0) - coeficiente * division.cociente
            lineas.append("1 = " + self.combinacion(terminos))
        lineas.append(f"Por tanto: {divisor}^(-1) ≡ {paso.coeficiente} ≡ {paso.inverso} (mod {modulo})")
        return "\n".join(lineas)
