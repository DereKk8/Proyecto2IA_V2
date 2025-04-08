# parser_logico.py

from logica import *

def parse_termino(texto):
    texto = texto.strip()
    if '(' in texto and texto.endswith(')'):
        nombre_funcion = texto[:texto.index('(')]
        argumentos_texto = texto[texto.index('(')+1:-1]
        argumentos = [parse_termino(arg.strip()) for arg in argumentos_texto.split(',')]
        return Funcion(nombre_funcion, argumentos)
    elif texto[0].islower():
        return Variable(texto)
    else:
        return Constante(texto)


def parse_predicado(texto):
    nombre = texto[:texto.index('(')]
    args_str = texto[texto.index('(')+1: texto.index(')')]
    argumentos = [parse_termino(a.strip()) for a in args_str.split(',')]
    return Predicado(nombre, argumentos)


def parse_literal(texto):
    texto = texto.strip()
    if texto.startswith("¬") or texto.startswith("~"):
        pred = parse_predicado(texto[1:].strip())
        return Literal(pred, negado=True)
    else:
        pred = parse_predicado(texto)
        return Literal(pred)


def parse_formula(texto):
    texto = texto.strip()

    if texto.startswith("¬") or texto.startswith("~"):
        return Negacion(parse_formula(texto[1:].strip()))

    if texto.startswith("∀") or texto.lower().startswith("forall"):
        partes = texto.split('.', 1)
        var = Variable(partes[0][1:].strip())  # ∀x.
        subformula = parse_formula(partes[1])
        return ParaTodo(var, subformula)

    if texto.startswith("∃") or texto.lower().startswith("exists"):
        partes = texto.split('.', 1)
        var = Variable(partes[0][1:].strip())  # ∃x.
        subformula = parse_formula(partes[1])
        return Existe(var, subformula)

    # Operadores binarios
    if '→' in texto:
        izq, der = map(str.strip, texto.split('→', 1))
        return Implicacion(parse_formula(izq), parse_formula(der))

    if '∧' in texto:
        izq, der = map(str.strip, texto.split('∧', 1))
        return Conjuncion(parse_formula(izq), parse_formula(der))

    if '∨' in texto:
        izq, der = map(str.strip, texto.split('∨', 1))
        return Disyuncion(parse_formula(izq), parse_formula(der))

    return parse_predicado(texto)

def lenguaje_natural_a_logica(frase):
    frase = frase.lower().strip()

    if "todo" in frase or "todos" in frase:
        partes = frase.split("es")
        sujeto = partes[0].replace("todo", "").replace("todos", "").strip()
        predicado = partes[1].strip()
        x = Variable("x")
        return ParaTodo(x, Implicacion(
            Predicado(sujeto.capitalize(), [x]),
            Predicado(predicado.capitalize(), [x])
        ))

    if "alguien" in frase or "algún" in frase:
        if "odia" in frase:
            partes = frase.split("odia")
            x = Variable("x")
            objeto = partes[1].strip().capitalize()
            return Existe(x, Predicado("Odia", [x, Constante(objeto)]))

    if "odia" in frase:
        partes = frase.split("odia")
        sujeto = partes[0].strip().capitalize()
        objeto = partes[1].strip().capitalize()
        return Predicado("Odia", [Constante(sujeto), Constante(objeto)])

    if "es" in frase:
        partes = frase.split("es")
        sujeto = partes[0].strip().capitalize()
        predicado = partes[1].strip().capitalize()
        return Predicado(predicado, [Constante(sujeto)])

    return None  # se puede extender luego

def entrada_premisas():
    premisas = []
    print("Ingrese premisas (una por línea). Vacío para terminar:")
    while True:
        linea = input("> ").strip()
        if linea == "":
            break
        formula = lenguaje_natural_a_logica(linea)
        if formula is None:
            try:
                formula = parse_formula(linea)
            except:
                print("No pude interpretar:", linea)
                continue
        premisas.append(formula)
    return premisas