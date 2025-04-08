# pruebas_logica.py

from logica import *
from parser_logico import *

def ejemplo_marco():
    frases = [
        "Marco es feo",
        "Todo humano es mortal",
        "Marco odia a Cesar"
    ]
    print("=== Traducción del ejemplo ===")
    for frase in frases:
        f = lenguaje_natural_a_logica(frase)
        print(f"'{frase}' → {f}")

ejemplo_marco()