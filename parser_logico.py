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

    # Manejo de relaciones binarias del tipo "X es Y de Z"
    if " es " in frase and " de " in frase:
        # Dividir la frase en sus componentes
        antes_es = frase.split(" es ")[0].strip()  # X
        entre_es_y_de = frase.split(" es ")[1].split(" de ")[0].strip()  # Y
        despues_de = frase.split(" de ")[1].strip()  # Z
        
        # Crear el predicado usando la palabra entre "es" y "de" como nombre de la relación
        return Predicado(
            entre_es_y_de.capitalize(),  # Nombre de la relación
            [
                Constante(antes_es.capitalize()),  # Primera constante
                Constante(despues_de.capitalize())  # Segunda constante
            ]
        )

    # Regla para inferir relaciones transitivas
    if "todo" in frase and " es " in frase and " de los " in frase:
        x = Variable("x")
        y = Variable("y")
        z = Variable("z")
        # Extraer el tipo de relación
        relacion1 = frase.split(" es ")[1].split(" de ")[0].strip()
        relacion2 = frase.split(" de los ")[1].split(" de ")[0].strip()
        return ParaTodo(x, ParaTodo(y, ParaTodo(z, 
            Implicacion(
                Conjuncion(
                    Predicado(relacion1.capitalize(), [x, y]),
                    Predicado(relacion1.capitalize(), [y, z])
                ),
                Predicado(relacion2.capitalize(), [x, z])
            )
        )))

    # Caso de "todos X son Y o Z"
    if " son o " in frase and " o " in frase.split(" son o ")[-1]:
        sujeto = frase.split("son")[0].replace("todos los", "").replace("todos", "").strip()
        resto = frase.split(" son o ", 1)[1].strip()
        parte1, parte2 = map(str.strip, resto.split(" o "))

        x = Variable("x")

        def interpretar_relacion(parte):
            if " a " in parte:
                accion, obj = map(str.strip, parte.split(" a "))
                return Predicado(accion.capitalize(), [x, Constante(obj.capitalize())])
            else:
                return Predicado(parte.capitalize(), [x])

        pred1 = interpretar_relacion(parte1)
        pred2 = interpretar_relacion(parte2)

        return ParaTodo(x, Implicacion(
            Predicado(sujeto.capitalize(), [x]),
            Disyuncion(pred1, pred2)
        ))

    # Caso de "todo humano asesina a gobernante que no es leal"
    if "asesina a" in frase and "que no es" in frase:
        partes = frase.split("asesina a")
        sujeto = partes[0].replace("todo", "").strip()
        objeto = partes[1].split("que")[0].strip()
        x = Variable("x")
        y = Variable("y")

        return ParaTodo(x, ParaTodo(y, Implicacion(
            Conjuncion(
                Predicado(sujeto.capitalize(), [x]),
                Conjuncion(
                    Predicado(objeto.capitalize(), [y]),
                    Negacion(Predicado("Leal", [x, y]))
                )
            ),
            Predicado("Asesina", [x, y])
        )))

    # Caso simple: todos los X son Y
    if "todo" in frase and " es " in frase and " de " not in frase:
        if " es " in frase:
            partes = frase.split("es")
        elif " son " in frase:
            partes = frase.split("son")
        else:
            return None

        sujeto = partes[0].replace("todos los", "").replace("todo", "").replace("todos", "").strip()
        predicado = partes[1].strip()
        x = Variable("x")
        return ParaTodo(x, Implicacion(
            Predicado(sujeto.capitalize(), [x]),
            Predicado(predicado.capitalize(), [x])
        ))

    # Caso de asesina simple
    if "asesina a" in frase:
        partes = frase.split("asesina a")
        sujeto = partes[0].strip().capitalize()
        objeto = partes[1].strip().capitalize()
        return Predicado("Asesina", [Constante(sujeto), Constante(objeto)])

    # Casos de existenciales
    if "alguien" in frase or "algún" in frase:
        if "odia" in frase:
            partes = frase.split("odia")
            x = Variable("x")
            objeto = partes[1].strip().capitalize()
            return Existe(x, Predicado("Odia", [x, Constante(objeto)]))

    # Caso de odia simple
    if "odia" in frase:
        partes = frase.split("odia")
        sujeto = partes[0].strip().capitalize()
        objeto = partes[1].strip().capitalize()
        return Predicado("Odia", [Constante(sujeto), Constante(objeto)])

    # Predicados unarios simples
    if " es " in frase and " de " not in frase:
        partes = frase.split(" es ")
        sujeto = partes[0].strip().capitalize()
        predicado = partes[1].strip().capitalize()
        return Predicado(predicado, [Constante(sujeto)])

    return None

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