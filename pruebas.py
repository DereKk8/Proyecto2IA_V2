from clausificacion import convertir_a_clausulas
from parser_logico import lenguaje_natural_a_logica
from motor_inferencia import MotorInferencia
from logica import Predicado, Variable, Disyuncion

def imprimir_base_conocimiento(motor):
    print("\nBase de Conocimiento:")
    for clausula in motor.base_conocimiento.clausulas:
        print(f"  {clausula}")

# Crear el motor de inferencia
motor = MotorInferencia()

# Lista de frases que forman nuestra base de conocimiento
frases = [
    "marco es humano",
    "marco es pompeyano",
    "todo pompeyano es humano",
    "cesar es gorbenante",
    "todos pompeyano son o leal a cesar o odia a cesar",
    "todo humano asesina a gobernante a que no es leal",
    "marco asesina a cesar"
]

# Primero, mostrar la conversión de cada frase a fórmula lógica y cláusulas
print("=== Conversión de frases a fórmulas y cláusulas ===")
for frase in frases:
    formula = lenguaje_natural_a_logica(frase)
    print("\nFrase:", frase)
    print("Fórmula lógica:", formula)
    clausulas = convertir_a_clausulas(formula)
    for c in clausulas:
        print("Cláusula:", c)
    # Agregar la fórmula a la base de conocimiento
    motor.base_conocimiento.agregar_formula(formula)

print("\n=== Base de Conocimiento Completa ===")
imprimir_base_conocimiento(motor)

# Definir algunas consultas de prueba
print("\n=== Pruebas de Inferencia ===")

def probar_consulta(motor, descripcion, consulta):
    print(f"\nConsulta: {descripcion}")
    print(f"Fórmula: {consulta}")
    resultado = motor.probar_por_refutacion(consulta)
    if resultado is True:
        print("Resultado: VERDADERO - La consulta se puede probar")
    elif resultado is False:
        print("Resultado: FALSO - La consulta no se puede probar")
    else:
        print("Resultado: INDETERMINADO - No se pudo determinar la verdad de la consulta")

# Prueba 1: ¿Es Marco un humano?
consulta1 = Predicado("Humano", [Variable("Marco")])
probar_consulta(motor, "¿Es Marco un humano?", consulta1)

# Prueba 2: ¿Es César un gobernante?
consulta2 = Predicado("Gobernante", [Variable("cesar")])
probar_consulta(motor, "¿Es César un gobernante?", consulta2)

# Prueba 3: ¿Marco asesina a César?
consulta3 = Predicado("Asesina", [Variable("marco"), Variable("cesar")])
probar_consulta(motor, "¿Marco asesina a César?", consulta3)

# Prueba 4: ¿Es Marco pompeyano?
consulta4 = Predicado("Pompeyano", [Variable("marco")])
probar_consulta(motor, "¿Es Marco pompeyano?", consulta4)

# Prueba 5: ¿Todo pompeyano es humano?
x = Variable("x")
consulta5 = Predicado("Humano", [x])
probar_consulta(motor, "¿Todo pompeyano es humano?", consulta5)

# Prueba 6: ¿Marco es leal a César o lo odia?
consulta6 = Disyuncion(
    Predicado("Leal", [Variable("marco"), Variable("cesar")]),
    Predicado("Odia", [Variable("marco"), Variable("cesar")])
)
probar_consulta(motor, "¿Marco es leal a César o lo odia?", consulta6)

print("\n=== Fin de las pruebas ===")