# Proyecto de Inferencia Lógica

## Ejemplos de Uso

### Ejemplo 1: Caso Pompeya
Base de conocimiento:

```shell-session
"marco es humano"
"marco es pompeyano"
"todo pompeyano es humano"
"cesar es gobernante"
"todos pompeyano son o leal a cesar o odia a cesar"
"todo humano asesina a gobernante a que no es leal"
"marco asesina a cesar"
```

Consulta de ejemplo:
- "¿Marco odia a César?"
```python
realizar_consulta_detallada(
    motor,
    "¿Marco odia a César?",
    Predicado("Odia", [Variable("marco"), Variable("cesar")])
)
```
Esta consulta requiere inferir si, dado que Marco es pompeyano y asesina a César, se puede deducir que lo odia.

### Ejemplo 2: Relaciones Familiares
Base de conocimiento:

```shell-session
"juan es padre de maria"
"maria es madre de pedro"
"todo padre es abuelo de los hijos de sus hijos"
```

Consulta de ejemplo:
- "¿Juan es abuelo de Pedro?"
```python
realizar_consulta_detallada(
    motor,
    "¿Es Juan abuelo de Pedro?",
    Predicado("Abuelo", [Variable("juan"), Variable("pedro")])
)
```
Esta consulta requiere inferir una relación de abuelo a través de la regla transitiva sobre relaciones padre/madre.

## Funcionamiento del Sistema

### Proceso General de Inferencia

El sistema sigue una serie de pasos estructurados para procesar el conocimiento y realizar inferencias:

1. **Entrada de Datos**
   - Recibe un conjunto de frases en lenguaje natural que conformarán la base de conocimiento
   - Acepta una consulta que puede estar en:
     * Lenguaje natural
     * Formato de cláusula lógica predefinida

2. **Transformación a Lógica de Primer Orden**
   - Analiza cada frase del lenguaje natural
   - Identifica predicados, variables y relaciones
   - Convierte las frases a fórmulas de lógica de primer orden

3. **Proceso de Clausificación**
   - Descompone fórmulas complejas en cláusulas más simples
   - Elimina implicaciones y cuantificadores
   - Normaliza las expresiones a forma clausal

4. **Gestión de la Base de Conocimiento**
   - Almacena las cláusulas resultantes
   - Mantiene un conjunto coherente de hechos y reglas

5. **Procesamiento de la Consulta**
   - Convierte la consulta a forma lógica (si está en lenguaje natural)
   - Prepara la consulta para el proceso de refutación

6. **Negación de la Consulta**
   - Niega la fórmula de la consulta
   - Prepara la negación para el proceso de clausificación

7. **Clausificación de la Consulta**
   - Aplica el proceso de clausificación a la consulta negada
   - Genera las cláusulas necesarias para la refutación

8. **Inferencia por Refutación**
   - Combina la base de conocimiento con la consulta negada
   - Aplica el algoritmo de resolución
   - Busca derivar la cláusula vacía para probar la validez

## Estructuras de Lógica de Primer Orden

El sistema implementa la lógica de primer orden mediante una jerarquía de clases que representan los diferentes elementos lógicos:

### Elementos Básicos

#### Término
- **Definición**: Clase base que representa los elementos más básicos de la lógica.
- **Implementación**: Clase abstracta con métodos para identificar el tipo de término.
- **Ejemplo**: 
```python
class Termino:
    def __init__(self, nombre):
        self.nombre = nombre
```

#### Constante
- **Definición**: Representa un objeto específico en el dominio del discurso.
- **Implementación**: Hereda de Término, representa valores fijos.
- **Ejemplo**: `Constante("marco")` → representa el individuo "marco"

#### Variable
- **Definición**: Representa un elemento no específico que puede tomar diferentes valores.
- **Implementación**: Hereda de Término, usado en cuantificadores y unificación.
- **Ejemplo**: `Variable("x")` → representa una variable que puede ser cualquier individuo

#### Función
- **Definición**: Mapea términos a otros términos.
- **Implementación**: Hereda de Término, contiene una lista de argumentos.
- **Ejemplo**: 
```python
Funcion("padre", [Constante("juan"), Constante("maria")])
```

#### Predicado
- **Definición**: Representa relaciones o propiedades sobre términos.
- **Implementación**: Contiene un nombre y una lista de argumentos.
- **Ejemplo**: `Predicado("Humano", [Constante("marco")])` → representa "marco es humano"

### Fórmulas Lógicas

#### Fórmula
- **Definición**: Clase base para todas las expresiones lógicas.
- **Implementación**: Clase abstracta de la que heredan todas las construcciones lógicas.

#### Negación
- **Definición**: Representa la negación lógica de una fórmula.
- **Implementación**: Contiene una fórmula como operando.
- **Ejemplo**: `Negacion(Predicado("Humano", [Variable("x")]))` → representa "no es humano(x)"

#### Conjunción
- **Definición**: Representa el "y" lógico entre dos fórmulas.
- **Implementación**: Contiene dos fórmulas (izquierda y derecha).
- **Ejemplo**: 
```python
Conjuncion(
    Predicado("Humano", [Variable("x")]),
    Predicado("Mortal", [Variable("x")])
)
```

#### Disyunción
- **Definición**: Representa el "o" lógico entre dos fórmulas.
- **Implementación**: Contiene dos fórmulas (izquierda y derecha).
- **Ejemplo**: 
```python
Disyuncion(
    Predicado("Leal", [Variable("x"), Constante("cesar")]),
    Predicado("Odia", [Variable("x"), Constante("cesar")])
)
```

#### Implicación
- **Definición**: Representa la implicación lógica (si-entonces).
- **Implementación**: Contiene antecedente y consecuente.
- **Ejemplo**: 
```python
Implicacion(
    Predicado("Humano", [Variable("x")]),
    Predicado("Mortal", [Variable("x")])
)
```

### Cuantificadores

#### Cuantificador
- **Definición**: Clase base para los cuantificadores.
- **Implementación**: Contiene una variable y una fórmula.

#### ParaTodo
- **Definición**: Representa el cuantificador universal (∀).
- **Implementación**: Hereda de Cuantificador.
- **Ejemplo**: 
```python
ParaTodo(
    Variable("x"),
    Implicacion(
        Predicado("Humano", [Variable("x")]),
        Predicado("Mortal", [Variable("x")])
    )
)
```

#### Existe
- **Definición**: Representa el cuantificador existencial (∃).
- **Implementación**: Hereda de Cuantificador.
- **Ejemplo**: 
```python
Existe(
    Variable("x"),
    Predicado("Humano", [Variable("x")])
)
```

### Elementos de Resolución

#### Literal
- **Definición**: Representa un predicado o su negación.
- **Implementación**: Contiene un predicado y un flag de negación.
- **Ejemplo**: 
```python
Literal(Predicado("Humano", [Constante("marco")]), negado=False)
```

#### Cláusula
- **Definición**: Conjunto de literales en disyunción.
- **Implementación**: Contiene una lista de literales.
- **Ejemplo**: 
```python
Clausula([
    Literal(Predicado("Humano", [Variable("x")]), negado=False),
    Literal(Predicado("Mortal", [Variable("x")]), negado=True)
])
```

### Combinación de Elementos

Las estructuras anteriores se combinan para formar expresiones complejas de lógica de primer orden:

1. Los términos (constantes, variables, funciones) son los bloques básicos.
2. Los predicados utilizan términos como argumentos.
3. Las fórmulas combinan predicados usando operadores lógicos.
4. Los cuantificadores vinculan variables en fórmulas.
5. Los literales y cláusulas se usan en el proceso de resolución.

**Ejemplo Completo**:
```python
# "Todo humano es mortal"
ParaTodo(
    Variable("x"),
    Implicacion(
        Predicado("Humano", [Variable("x")]),
        Predicado("Mortal", [Variable("x")])
    )
)
```

# Jerarquía de Elementos Lógicos

```plantuml
@startuml

class Término
class Constante
class Variable
class Función
class Predicado
class Fórmula
class Negación
class Conjunción
class Disyunción
class Implicación
class Cuantificador
class ParaTodo
class Existe
class Literal
class Cláusula

Término <|-- Constante
Término <|-- Variable
Término <|-- Función

Fórmula <|-- Negación
Fórmula <|-- Conjunción
Fórmula <|-- Disyunción
Fórmula <|-- Implicación
Fórmula <|-- Cuantificador

Cuantificador <|-- ParaTodo
Cuantificador <|-- Existe

Literal --> Cláusula

@enduml
```

Puedes visualizar este diagrama en [PlantText](https://www.planttext.com/)

## Parser Lógico

### Estructura y Funcionamiento

El parser lógico está diseñado para transformar dos tipos de entrada:
1. Fórmulas en notación lógica formal
2. Frases en lenguaje natural restringido

#### Parser de Fórmulas Formales

Procesa expresiones lógicas con la siguiente sintaxis:
- Predicados: `Predicado(arg1, arg2, ...)`
- Negación: `¬` o `~`
- Conectivos: `∧` (and), `∨` (or), `→` (implica)
- Cuantificadores: `∀` (para todo), `∃` (existe)

Ejemplo:
```python
# Salida: "∀x.(Humano(x) → Mortal(x))"
ParaTodo(
    Variable("x"),
    Implicacion(
        Predicado("Humano", [Variable("x")]),
        Predicado("Mortal", [Variable("x")])
    )
)
```

#### Parser de Lenguaje Natural

Maneja varios patrones de frases:

1. **Relaciones Binarias**:
```python
# "Juan es padre de María"
Predicado("Padre", [Constante("Juan"), Constante("Maria")])
```

2. **Reglas Universales**:
```python
# "Todo humano es mortal"
ParaTodo(
    Variable("x"),
    Implicacion(
        Predicado("Humano", [Variable("x")]),
        Predicado("Mortal", [Variable("x")])
    )
)
```

3. **Disyunciones**:
```python
# "Todos pompeyano son o leal a cesar o odia a cesar"
ParaTodo(
    Variable("x"),
    Implicacion(
        Predicado("Pompeyano", [Variable("x")]),
        Disyuncion(
            Predicado("Leal", [Variable("x"), Constante("Cesar")]),
            Predicado("Odia", [Variable("x"), Constante("Cesar")])
        )
    )
)
```

### Proceso de Parsing

1. **Tokenización**: Divide la entrada en componentes significativos
```python
# Ejemplo: "juan es padre de maria"
frase = frase.lower().strip()
if " es " in frase and " de " in frase:
    antes_es = frase.split(" es ")[0].strip()      # "juan"
    entre_es_y_de = frase.split(" es ")[1].split(" de ")[0].strip()  # "padre"
    despues_de = frase.split(" de ")[1].strip()    # "maria"
```

2. **Identificación de Patrones**: Detecta estructuras sintácticas conocidas
```python
# Identifica diferentes patrones en el texto
if " es " in frase and " de " in frase:
    # Patrón de relación binaria: "X es Y de Z"
    tipo = "relacion_binaria"
elif "todo" in frase and " es " in frase:
    # Patrón de regla universal: "todo X es Y"
    tipo = "regla_universal"
elif "asesina a" in frase:
    # Patrón de acción: "X asesina a Y"
    tipo = "predicado_accion"
```

3. **Construcción del AST**: Genera el predicado
```python
# Para una relación binaria: "juan es padre de maria"
def construir_ast_relacion_binaria(antes_es, relacion, despues_de):
    return Predicado(
        relacion.capitalize(),  # Nodo raíz: predicado "Padre"
        [
            Constante(antes_es.capitalize()),    # Hijo izquierdo: "Juan"
            Constante(despues_de.capitalize())   # Hijo derecho: "Maria"
        ]
    )

```

### Ejemplo Completo de Transformación

```python
# Entrada: "todo humano asesina a gobernante que no es leal"
def procesar_regla_compleja(frase):
    # 1. Tokenización
    partes = frase.split("asesina a")
    sujeto = partes[0].replace("todo", "").strip()
    objeto = partes[1].split("que")[0].strip()
    
    # 2. Identificación del patrón
    # Detecta patrón de regla condicional con negación
    
    # 3. Construcción del AST
    x = Variable("x")
    y = Variable("y")
    
    # 4. Transformación a fórmula lógica
    return ParaTodo(x, ParaTodo(y, 
        Implicacion(
            Conjuncion(
                Predicado(sujeto.capitalize(), [x]),
                Conjuncion(
                    Predicado(objeto.capitalize(), [y]),
                    Negacion(Predicado("Leal", [x, y]))
                )
            ),
            Predicado("Asesina", [x, y])
        )
    ))

# Resultado:
# ∀x.∀y.(Humano(x) ∧ (Gobernante(y) ∧ ¬Leal(x,y)) → Asesina(x,y))
```

¿Te gustaría que expanda algún ejemplo específico o que muestre más casos de transformación?

### Patrones Principales de Lenguaje Natural

- `"X es Y"` → Predicados unarios
- `"X es Y de Z"` → Relaciones binarias
- `"todo X es Y"` → Cuantificación universal
- `"X verbo a Y"` → Predicados de acción
- `"todos X son o Y o Z"` → Disyunciones universales



