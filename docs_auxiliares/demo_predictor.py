from predictor_lsm import PredictorLSM

print("="*70)
print("DEMO RÁPIDA DEL PREDICTOR LSM")
print("="*70)

# Inicializar predictor
predictor = PredictorLSM()

print("\n📊 Ejemplos de Predicción:\n")

ejemplos = [
    {"dedo1": 100, "dedo2": 0, "dedo3": 0, "dedo4": 0, "dedo5": 0, "movimiento": False, "nombre": "Letra A (puño cerrado)"},
    {"dedo1": 0, "dedo2": 999, "dedo3": 999, "dedo4": 999, "dedo5": 999, "movimiento": False, "nombre": "Letra B (4 dedos estirados)"},
    {"dedo1": 50, "dedo2": 999, "dedo3": 0, "dedo4": 0, "dedo5": 0, "movimiento": False, "nombre": "Letra D (índice arriba)"},
    {"dedo1": 0, "dedo2": 0, "dedo3": 0, "dedo4": 0, "dedo5": 999, "movimiento": False, "nombre": "Letra I (meñique arriba)"},
    {"dedo1": 999, "dedo2": 0, "dedo3": 0, "dedo4": 0, "dedo5": 999, "movimiento": False, "nombre": "Letra Y (pulgar y meñique)"},
]

for ej in ejemplos:
    letra, probs = predictor.predecir_con_probabilidades(
        ej["dedo1"], ej["dedo2"], ej["dedo3"], 
        ej["dedo4"], ej["dedo5"], ej["movimiento"]
    )
    confianza = list(probs.values())[0]
    print(f"✓ {ej['nombre']}")
    print(f"  → Predicción: '{letra.upper()}' (confianza: {confianza*100:.1f}%)")
    print()

print("="*70)
print("Modelo listo para uso. Ejecuta 'python predictor_lsm.py' para más ejemplos.")
print("="*70)
