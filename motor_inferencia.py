from logica import *
from clausificacion import convertir_a_clausulas

class BaseConocimiento:
    def __init__(self):
        self.clausulas = set()
        self.contador_vars = 0

    def agregar_clausula(self, clausula):
        if not isinstance(clausula, Clausula):
            raise TypeError(f"Se esperaba una Clausula, se recibió {type(clausula)}")
        self.clausulas.add(clausula)
        print(f"Agregada cláusula: {clausula}")

    def agregar_formula(self, formula):
        print(f"\nAgregando fórmula a la base de conocimiento: {formula}")
        nuevas_clausulas = convertir_a_clausulas(formula)
        print(f"Cláusulas generadas: {len(nuevas_clausulas)}")
        for literales in nuevas_clausulas:
            try:
                clausula = Clausula([Literal(lit[1], lit[0] == "¬") for lit in literales])
                self.clausulas.add(clausula)
                print(f"  Agregada: {clausula}")
            except Exception as e:
                print(f"  [ERROR] No se pudo crear cláusula de {literales}: {str(e)}")

class MotorInferencia:
    def __init__(self):
        self.base_conocimiento = BaseConocimiento()

    def negar_consulta(self, consulta):
        """Niega la consulta y la convierte a forma clausal"""
        negacion = Negacion(consulta)
        return convertir_a_clausulas(negacion)

    def ocurre_en(self, var, termino):
        """Verifica si una variable ocurre en un término"""
        if isinstance(termino, Variable):
            return var.nombre == termino.nombre
        elif isinstance(termino, Funcion):
            return any(self.ocurre_en(var, arg) for arg in termino.argumentos)
        return False

    def unificar(self, termino1, termino2, sustitucion=None):
        """Unifica dos términos y retorna la sustitución más general si existe"""
        if sustitucion is None:
            sustitucion = {}
        
        # Si los términos son exactamente iguales
        if str(termino1) == str(termino2):
            return sustitucion

        if isinstance(termino1, Variable):
            if termino1.nombre in sustitucion:
                return self.unificar(sustitucion[termino1.nombre], termino2, sustitucion)
            elif isinstance(termino2, Variable) and termino2.nombre in sustitucion:
                return self.unificar(termino1, sustitucion[termino2.nombre], sustitucion)
            elif self.ocurre_en(termino1, termino2):
                return None
            else:
                sustitucion[termino1.nombre] = termino2
                return sustitucion
        
        elif isinstance(termino2, Variable):
            return self.unificar(termino2, termino1, sustitucion)
        
        # Si son predicados
        elif isinstance(termino1, Predicado) and isinstance(termino2, Predicado):
            if termino1.nombre != termino2.nombre:
                return None
            if len(termino1.argumentos) != len(termino2.argumentos):
                return None
            
            # Unificar argumentos
            for arg1, arg2 in zip(termino1.argumentos, termino2.argumentos):
                sustitucion = self.unificar(arg1, arg2, sustitucion)
                if sustitucion is None:
                    return None
            return sustitucion
        
        return None

    def aplicar_sustitucion(self, termino, sustitucion):
        """Aplica una sustitución a un término"""
        if isinstance(termino, Variable):
            return sustitucion.get(termino.nombre, termino)
        elif isinstance(termino, Funcion):
            nuevos_args = [self.aplicar_sustitucion(arg, sustitucion) for arg in termino.argumentos]
            return Funcion(termino.nombre, nuevos_args)
        return termino

    def resolver_clausulas(self, clausula1, clausula2):
        """Intenta resolver dos cláusulas y retorna las resolventes"""
        resolventes = []
        
        for lit1 in clausula1.literales:
            for lit2 in clausula2.literales:
                # Verificar si los literales son complementarios
                if lit1.negado != lit2.negado:
                    # Intentar unificar los predicados
                    sustitucion = self.unificar(lit1.predicado, lit2.predicado)
                    if sustitucion is not None:
                        # Crear nueva cláusula con los literales restantes
                        nuevos_literales = []
                        for lit in clausula1.literales + clausula2.literales:
                            if lit != lit1 and lit != lit2:
                                pred = self.aplicar_sustitucion(lit.predicado, sustitucion)
                                nuevos_literales.append(Literal(pred, lit.negado))
                        if nuevos_literales:
                            resolventes.append(Clausula(nuevos_literales))
                        else:
                            # Cláusula vacía - contradicción encontrada
                            return [Clausula([])]
        
        return resolventes

    def probar_por_refutacion(self, consulta, max_iteraciones=1000):
        """Intenta probar una consulta por refutación"""
        print("\nIniciando prueba por refutación")
        print(f"Base de conocimiento: {len(self.base_conocimiento.clausulas)} cláusulas")
        
        # Negar la consulta y agregarla a la base de conocimiento
        clausulas_negadas = self.negar_consulta(consulta)
        clausulas_trabajo = self.base_conocimiento.clausulas.copy()
        
        for literales in clausulas_negadas:
            clausula = Clausula([Literal(lit[1], lit[0] == "¬") for lit in literales])
            clausulas_trabajo.add(clausula)
            print(f"Agregada negación: {clausula}")

        # Verificación directa para hechos simples
        if isinstance(consulta, Predicado):
            consulta_literal = Literal(consulta, False)
            for clausula in self.base_conocimiento.clausulas:
                if len(clausula.literales) == 1:
                    literal_base = clausula.literales[0]
                    if (literal_base.predicado.nombre == consulta_literal.predicado.nombre and
                        len(literal_base.predicado.argumentos) == len(consulta_literal.predicado.argumentos)):
                        sustitucion = self.unificar(literal_base.predicado, consulta_literal.predicado)
                        if sustitucion is not None:
                            print(f"Coincidencia directa encontrada")
                            return True

        clausulas_nuevas = set()
        iteracion = 0

        while iteracion < max_iteraciones:
            iteracion += 1
            
            for c1 in clausulas_trabajo:
                for c2 in clausulas_trabajo:
                    if c1 != c2:
                        resolventes = self.resolver_clausulas(c1, c2)
                        for resolvente in resolventes:
                            if len(resolvente.literales) == 0:
                                print("Se encontró la cláusula vacía")
                                return True
                            if resolvente not in clausulas_trabajo and resolvente not in clausulas_nuevas:
                                clausulas_nuevas.add(resolvente)

            if not clausulas_nuevas:
                return False

            clausulas_trabajo.update(clausulas_nuevas)
            clausulas_nuevas = set()

        return None
