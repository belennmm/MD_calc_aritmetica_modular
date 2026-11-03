"""Textos de ayuda de la aplicación."""
INSTRUCCIONES = """1. Ingrese un número primo en el campo p.
2. Escriba la expresión utilizando números enteros.
3. Puede utilizar +, -, *, /, ^ y paréntesis.
4. Utilice * para indicar multiplicación.
5. La división se realiza mediante inversos modulares.
6. Los resultados están entre 0 y p - 1.
7. Presione Calcular o Enter para obtener el resultado.

Los exponentes se calculan sin reducir módulo p.
Deben dar un entero no negativo; las divisiones en ellos son exactas.
La potencia se asocia a la derecha: 2^3^2 = 2^(3^2).
El menos tiene menor prioridad que la potencia: -2^2 = -(2^2).

Escape: limpiar expresión. Retroceso: borrar carácter.
Ejemplo: p = 23; expresión = (7^3 + 4*5)*2."""
