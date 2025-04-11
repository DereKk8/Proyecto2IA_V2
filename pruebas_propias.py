from clausificacion import convertir_a_clausulas, eliminar_implicaciones, mover_negaciones, estandarizar_variables, skolemizar, eliminar_cuantificadores_universales, distribuir_or
from parser_logico import lenguaje_natural_a_logica
from motor_inferencia import MotorInferencia
from logica import Predicado, Variable, Disyuncion, Negacion

def mostrar_pasos_clausificacion(formula, descripcion=""):
    print(f"\n=== Pasos de Clausificación {descripcion} ===")
    print("1. Fórmula original:")
    print(f"   {formula}")
    
    print("\n2. Eliminar implicaciones:")
    formula = eliminar_implicaciones(formula)
    print(f"   {formula}")
    
    print("\n3. Mover negaciones hacia adentro:")
    formula = mover_negaciones(formula)
    print(f"   {formula}")
    
    print("\n4. Estandarizar variables:")
    formula = estandarizar_variables(formula)
    print(f"   {formula}")
    
    print("\n5. Skolemización:")
    formula = skolemizar(formula)
    print(f"   {formula}")
    
    print("\n6. Eliminar cuantificadores universales:")
    formula = eliminar_cuantificadores_universales(formula)
    print(f"   {formula}")
    
    print("\n7. Distribución de OR sobre AND:")
    formula = distribuir_or(formula)
    print(f"   {formula}")
    
    print("\n8. Forma clausal final:")
    clausulas = convertir_a_clausulas(formula)
    for i, c in enumerate(clausulas, 1):
        print(f"   Cláusula {i}: {c}")
    
    return clausulas

def realizar_consulta_detallada(motor, descripcion, consulta, frase_natural=None):
    print("\n" + "="*80)
    print(f"CONSULTA: {descripcion}")
    print("="*80)
    
    # Paso 1: Mostrar la base de conocimiento y su proceso de clausificación
    print("\nPASO 1: Base de Conocimiento")
    print("Frases en la base de conocimiento:")
    for i, frase in enumerate(frases, 1):
        print(f"\n--- Procesando frase {i}: '{frase}' ---")
        formula = lenguaje_natural_a_logica(frase)
        print("Fórmula lógica:", formula)
        clausulas = mostrar_pasos_clausificacion(formula, f"de frase {i}")
    
    # Paso 2: Transformación y clausificación de la consulta
    print("\nPASO 2: Procesamiento de la Consulta")
    if frase_natural:
        print(f"Frase de consulta: '{frase_natural}'")
        formula_consulta = lenguaje_natural_a_logica(frase_natural)
        print(f"Fórmula lógica de la consulta: {formula_consulta}")
    else:
        formula_consulta = consulta
        print(f"Fórmula lógica de la consulta: {consulta}")
    
    print("\nClausificación de la negación de la consulta:")
    negacion = Negacion(formula_consulta)
    clausulas_negadas = mostrar_pasos_clausificacion(negacion, "de la negación de la consulta")
    
    # Paso 3: Resolución por Refutación
    print("\nPASO 3: Resolución por Refutación")
    print("Estado actual de la base de conocimiento:")
    for i, c in enumerate(motor.base_conocimiento.clausulas, 1):
        print(f"  {i}. {c}")
    
    print("\nAgregando la negación de la consulta:")
    for c in clausulas_negadas:
        print(f"  + {c}")
    
    # Realizar la prueba
    resultado = motor.probar_por_refutacion(consulta)
    
    # Mostrar resultado final
    print("\nRESULTADO FINAL:")
    if resultado is True:
        print("✓ VERDADERO - La consulta se puede probar")
    elif resultado is False:
        print("✗ FALSO - La consulta no se puede probar")
    else:
        print("? INDETERMINADO - No se pudo determinar la verdad de la consulta")
    print("="*80)

# Crear el motor de inferencia
motor = MotorInferencia()

# Lista de frases para la base de conocimiento
frases = [
    "marco es humano",
    "marco es pompeyano",
    "todo pompeyano es humano",
    "cesar es gobernante",
    "todos pompeyano son o leal a cesar o odia a cesar",
    "todo humano asesina a gobernante a que no es leal",
    "marco asesina a cesar"
]

# Cargar la base de conocimiento
print("=== Cargando Base de Conocimiento ===")
for frase in frases:
    formula = lenguaje_natural_a_logica(frase)
    motor.base_conocimiento.agregar_formula(formula)

# Realizar consultas detalladas
print("\n=== Iniciando Consultas ===")

consulta = Disyuncion(
    Predicado("Leal", [Variable("marco"), Variable("cesar")]),
    Predicado("Odia", [Variable("marco"), Variable("cesar")])
)

pregunta = "¿Marco odia a cesar?";
realizar_consulta_detallada(motor, "¿Marco odia a cesar?", consulta)
print(pregunta)

