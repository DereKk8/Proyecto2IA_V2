from clausificacion import convertir_a_clausulas
from parser_logico import lenguaje_natural_a_logica

frases = [
    "marco es humano",
    "marco es pompeyano",
    "todo pompeyano es humano",
    "cesar es gorbenante",
    "todos pompeyano son o leal a cesar o odia a cesar",
    "todo humano asesina a gobernante a que no es leal",
    "marco asesina a cesar"
    
]

for frase in frases:
    formula = lenguaje_natural_a_logica(frase)
    print("Frase:", frase)
    print("Fórmula lógica:", formula)
    clausulas = convertir_a_clausulas(formula)
    for c in clausulas:
        print("Cláusula:", c)
    print("---")