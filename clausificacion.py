#clausificacion.py

from logica import *

def eliminar_implicaciones(formula):
    if isinstance(formula, Implicacion):
        return Disyuncion(
            Negacion(eliminar_implicaciones(formula.antecedente)),
            eliminar_implicaciones(formula.consecuente)
        )
    elif isinstance(formula, Conjuncion):
        return Conjuncion(
            eliminar_implicaciones(formula.izquierda),
            eliminar_implicaciones(formula.derecha)
        )
    elif isinstance(formula, Implicacion):
        return Disyuncion(
            Negacion(eliminar_implicaciones(formula.antecedente)),
            eliminar_implicaciones(formula.consecuente)
        )
    elif isinstance(formula, Negacion):
        return Negacion(eliminar_implicaciones(formula.operando))
    elif isinstance(formula, ParaTodo) or isinstance(formula, Existe):
        return formula.__class__(formula.variable, eliminar_implicaciones(formula.formula))
    else:
        return formula
    

def mover_negaciones(formula):
    if isinstance(formula, Negacion):
        sub = formula.operando
        if isinstance(sub, Negacion):  # ¬(¬A) = A
            return mover_negaciones(sub.operando)
        elif isinstance(sub, Conjuncion):  # ¬(A ∧ B) = ¬A ∨ ¬B
            return Disyuncion(mover_negaciones(Negacion(sub.izquierda)), mover_negaciones(Negacion(sub.derecha)))
        elif isinstance(sub, Disyuncion):  # ¬(A ∨ B) = ¬A ∧ ¬B
            return Conjuncion(mover_negaciones(Negacion(sub.izquierda)), mover_negaciones(Negacion(sub.derecha)))
        elif isinstance(sub, ParaTodo):  # ¬∀x P = ∃x ¬P
            return Existe(sub.variable, mover_negaciones(Negacion(sub.formula)))
        elif isinstance(sub, Existe):  # ¬∃x P = ∀x ¬P
            return ParaTodo(sub.variable, mover_negaciones(Negacion(sub.formula)))
        else:
            return Negacion(mover_negaciones(sub))
    elif isinstance(formula, Conjuncion) or isinstance(formula, Disyuncion):
        return formula.__class__(mover_negaciones(formula.izquierda), mover_negaciones(formula.derecha))
    elif isinstance(formula, ParaTodo) or isinstance(formula, Existe):
        return formula.__class__(formula.variable, mover_negaciones(formula.formula))
    else:
        return formula
    

def estandarizar_variables(formula, mapping=None, contador=None):
    if mapping is None:
        mapping = {}
    if contador is None:
        contador = [0]

    if isinstance(formula, ParaTodo) or isinstance(formula, Existe):
        var_original = formula.variable.nombre
        nuevo_nombre = f"{var_original}_{contador[0]}"
        contador[0] += 1
        mapping[var_original] = nuevo_nombre
        nueva_var = Variable(nuevo_nombre)
        nueva_formula = estandarizar_variables(formula.formula, mapping, contador)
        mapping.pop(var_original)
        return formula.__class__(nueva_var, nueva_formula)
    elif isinstance(formula, Predicado):
        nuevos_argumentos = []
        for arg in formula.argumentos:
            if isinstance(arg, Variable) and arg.nombre in mapping:
                nuevos_argumentos.append(Variable(mapping[arg.nombre]))
            else:
                nuevos_argumentos.append(arg)
        return Predicado(formula.nombre, nuevos_argumentos)
    elif isinstance(formula, Negacion):
        return Negacion(estandarizar_variables(formula.operando, mapping, contador))
    elif isinstance(formula, Conjuncion) or isinstance(formula, Disyuncion):
        return formula.__class__(
            estandarizar_variables(formula.izquierda, mapping, contador),
            estandarizar_variables(formula.derecha, mapping, contador)
        )
    else:
        return formula
    

def skolemizar(formula, vars_universales=None, contador=None):
    if vars_universales is None:
        vars_universales = []
    if contador is None:
        contador = [0]

    if isinstance(formula, ParaTodo):
        nueva_var = formula.variable
        return ParaTodo(nueva_var, skolemizar(formula.formula, vars_universales + [nueva_var.nombre], contador))
    elif isinstance(formula, Existe):
        var = formula.variable
        if vars_universales:
            nombre_funcion = f"f{contador[0]}"
            contador[0] += 1
            argumentos = [Variable(v) for v in vars_universales]
            skolem_term = Funcion(nombre_funcion, argumentos)
        else:
            skolem_term = Constante(f"c{contador[0]}")
            contador[0] += 1
        return sustituir_variable(formula.formula, var.nombre, skolem_term)
    elif isinstance(formula, Conjuncion) or isinstance(formula, Disyuncion):
        return formula.__class__(
            skolemizar(formula.izquierda, vars_universales, contador),
            skolemizar(formula.derecha, vars_universales, contador)
        )
    elif isinstance(formula, Negacion):
        return Negacion(skolemizar(formula.operando, vars_universales, contador))
    else:
        return formula

def sustituir_variable(formula, nombre_variable, nuevo_valor):
    if isinstance(formula, Predicado):
        nuevos_argumentos = []
        for arg in formula.argumentos:
            if isinstance(arg, Variable) and arg.nombre == nombre_variable:
                nuevos_argumentos.append(nuevo_valor)
            else:
                nuevos_argumentos.append(arg)
        return Predicado(formula.nombre, nuevos_argumentos)
    elif isinstance(formula, Conjuncion) or isinstance(formula, Disyuncion):
        return formula.__class__(
            sustituir_variable(formula.izquierda, nombre_variable, nuevo_valor),
            sustituir_variable(formula.derecha, nombre_variable, nuevo_valor)
        )
    elif isinstance(formula, Negacion):
        return Negacion(sustituir_variable(formula.formula, nombre_variable, nuevo_valor))
    else:
        return formula
    
def eliminar_cuantificadores_universales(formula):
    if isinstance(formula, ParaTodo):
        return eliminar_cuantificadores_universales(formula.formula)
    elif isinstance(formula, Conjuncion) or isinstance(formula, Disyuncion):
        return formula.__class__(
            eliminar_cuantificadores_universales(formula.izquierda),
            eliminar_cuantificadores_universales(formula.derecha)
        )
    elif isinstance(formula, Negacion):
        return Negacion(eliminar_cuantificadores_universales(formula.operando))
    else:
        return formula
    

def distribuir_or(formula):
    if isinstance(formula, Disyuncion):
        A = distribuir_or(formula.izquierda)
        B = distribuir_or(formula.derecha)
        if isinstance(A, Conjuncion):
            return Conjuncion(
                distribuir_or(Disyuncion(A.izquierda, B)),
                distribuir_or(Disyuncion(A.derecha, B))
            )
        elif isinstance(B, Conjuncion):
            return Conjuncion(
                distribuir_or(Disyuncion(A, B.izquierda)),
                distribuir_or(Disyuncion(A, B.derecha))
            )
        else:
            return Disyuncion(A, B)
    elif isinstance(formula, Conjuncion):
        return Conjuncion(distribuir_or(formula.izquierda), distribuir_or(formula.derecha))
    else:
        return formula
    
def extraer_clausulas(formula):
    if isinstance(formula, Conjuncion):
        return extraer_clausulas(formula.izquierda) + extraer_clausulas(formula.derecha)
    else:
        return [extraer_literales(formula)]

def extraer_literales(formula):
    if isinstance(formula, Disyuncion):
        return extraer_literales(formula.izquierda) + extraer_literales(formula.derecha)
    elif isinstance(formula, Negacion):
        if isinstance(formula.operando, Predicado):
            return [("¬", formula.operando)]
    elif isinstance(formula, Predicado):
        return [("", formula)]
    return []


def convertir_a_clausulas(formula):
    f = eliminar_implicaciones(formula)
    f = mover_negaciones(f)
    f = estandarizar_variables(f)
    f = skolemizar(f)
    f = eliminar_cuantificadores_universales(f)
    f = distribuir_or(f)
    clausulas = extraer_clausulas(f)
    return clausulas