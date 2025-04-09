from clausificacion import convertir_a_clausulas
from parser_logico import lenguaje_natural_a_logica
from motor_inferencia import MotorInferencia
from logica import Predicado, Variable, Disyuncion

def imprimir_base_conocimiento(motor):
    print("\nBase de Conocimiento:")
    if not motor.base_conocimiento.clausulas:
        print("  [ADVERTENCIA] La base de conocimiento está vacía!")
    else:
        for clausula in motor.base_conocimiento.clausulas:
            print(f"  {clausula}")
    print(f"Total de cláusulas: {len(motor.base_conocimiento.clausulas)}")

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
for i, frase in enumerate(frases, 1):
    print(f"\nProcesando frase {i}: '{frase}'")
    try:
        formula = lenguaje_natural_a_logica(frase)
        print("Fórmula lógica:", formula)
        
        clausulas = convertir_a_clausulas(formula)
        print("Cláusulas generadas:")
        if not clausulas:
            print("  [ADVERTENCIA] No se generaron cláusulas!")
        for j, c in enumerate(clausulas, 1):
            print(f"  {j}. {c}")
        
        # Agregar la fórmula a la base de conocimiento
        motor.base_conocimiento.agregar_formula(formula)
        print(f"Estado de la base después de agregar: {len(motor.base_conocimiento.clausulas)} cláusulas totales")
    except Exception as e:
        print(f"[ERROR] Error al procesar la frase: {str(e)}")

print("\n=== Base de Conocimiento Final ===")
imprimir_base_conocimiento(motor)

# Función mejorada para probar consultas
def probar_consulta(motor, descripcion, consulta):
    print(f"\n=== Consulta: {descripcion} ===")
    print(f"Fórmula de consulta: {consulta}")
    
    # Mostrar la negación de la consulta y sus cláusulas
    clausulas_negadas = motor.negar_consulta(consulta)
    print("Cláusulas de la negación de la consulta:")
    for c in clausulas_negadas:
        print(f"  {c}")
    
    # Realizar la prueba
    resultado = motor.probar_por_refutacion(consulta)
    
    # Mostrar resultado
    print("\nResultado:", end=" ")
    if resultado is True:
        print("✓ VERDADERO - La consulta se puede probar")
    elif resultado is False:
        print("✗ FALSO - La consulta no se puede probar")
    else:
        print("? INDETERMINADO - No se pudo determinar la verdad de la consulta")

print("\n=== Iniciando Pruebas de Inferencia ===")

# Pruebas básicas de hechos directos
print("\n--- Pruebas de Hechos Directos ---")

# Prueba 1: ¿Es Marco un humano?
consulta1 = Predicado("Humano", [Variable("marco")])
probar_consulta(motor, "¿Es Marco un humano?", consulta1)


print("\n--- Pruebas de Inferencia Simple ---")

# Prueba 3: ¿Marco asesina a César?
consulta3 = Predicado("Asesina", [Variable("marco"), Variable("cesar")])
probar_consulta(motor, "¿Marco asesina a César?", consulta3)

# Prueba 4: ¿Es Marco pompeyano?
consulta4 = Predicado("Pompeyano", [Variable("marco")])
probar_consulta(motor, "¿Es Marco pompeyano?", consulta4)

print("\n--- Pruebas de Inferencia Compleja ---")

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