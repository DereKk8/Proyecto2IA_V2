# logica.py

# ---------------------
# TÉRMINOS
# ---------------------

class Termino:
    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return self.nombre

    def es_variable(self):
        return False

    def es_funcion(self):
        return False

    def es_constante(self):
        return False


class Constante(Termino):
    def es_constante(self):
        return True


class Variable(Termino):
    def es_variable(self):
        return True


class Funcion(Termino):
    def __init__(self, nombre, argumentos):
        super().__init__(nombre)
        self.argumentos = argumentos  # lista de Terminos

    def __repr__(self):
        return f"{self.nombre}({', '.join(map(str, self.argumentos))})"

    def es_funcion(self):
        return True


# ---------------------
# PREDICADOS
# ---------------------

class Predicado:
    def __init__(self, nombre, argumentos):
        self.nombre = nombre
        self.argumentos = argumentos  # lista de Terminos

    def __repr__(self):
        return f"{self.nombre}({', '.join(map(str, self.argumentos))})"


# ---------------------
# FÓRMULAS LÓGICAS
# ---------------------

class Formula:
    pass


class Negacion(Formula):
    def __init__(self, operando):
        self.operando = operando

    def __repr__(self):
        return f"¬{self.operando}"


class Conjuncion(Formula):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def __repr__(self):
        return f"({self.izquierda} ∧ {self.derecha})"


class Disyuncion(Formula):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def __repr__(self):
        return f"({self.izquierda} ∨ {self.derecha})"


class Implicacion(Formula):
    def __init__(self, antecedente, consecuente):
        self.antecedente = antecedente
        self.consecuente = consecuente

    def __repr__(self):
        return f"({self.antecedente} → {self.consecuente})"


class Cuantificador(Formula):
    def __init__(self, variable, formula):
        self.variable = variable  # Variable
        self.formula = formula    # Formula


class ParaTodo(Cuantificador):
    def __repr__(self):
        return f"∀{self.variable}.{self.formula}"


class Existe(Cuantificador):
    def __repr__(self):
        return f"∃{self.variable}.{self.formula}"


# ---------------------
# LITERALES Y CLÁUSULAS
# ---------------------

class Literal:
    def __init__(self, predicado, negado=False):
        self.predicado = predicado  # Predicado
        self.negado = negado

    def __repr__(self):
        return f"¬{self.predicado}" if self.negado else str(self.predicado)

    def complemento(self):
        return Literal(self.predicado, not self.negado)


class Clausula:
    def __init__(self, literales):
        self.literales = literales  # lista de Literales

    def __repr__(self):
        return ' ∨ '.join(map(str, self.literales))