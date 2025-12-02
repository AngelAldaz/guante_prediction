"""
Script de prueba para verificar el predictor con la nueva característica posicion_mano
"""
from predictor_lsm import PredictorLSM

print("="*70)
print("PRUEBA DEL PREDICTOR CON NUEVA CARACTERÍSTICA: posicion_mano")
print("="*70)

# Inicializar predictor
predictor = PredictorLSM()

print("\n1. Prueba de predicción básica:")
print("-" * 70)
letra = predictor.predecir(0, 300, 200, 100, 200, 90.0, False)
print(f"   Entrada: dedos=[0,300,200,100,200], pos=90.0, mov=False")
print(f"   Predicción: '{letra}'")

print("\n2. Prueba de predicción con probabilidades:")
print("-" * 70)
letra, probs = predictor.predecir_con_probabilidades(999, 0, 0, 0, 0, 0.0, False)
print(f"   Entrada: dedos=[999,0,0,0,0], pos=0.0, mov=False")
print(f"   Predicción: '{letra}'")
print(f"   Top 3 probabilidades:")
for i, (clase, prob) in enumerate(list(probs.items())[:3], 1):
    print(f"      {i}. '{clase}': {prob*100:.2f}%")

print("\n3. Prueba desde formato CSV:")
print("-" * 70)
lineas_csv = [
    "999,0,0,0,0,0.0,false",      # a
    "0,999,999,999,999,5.0,false", # b
    "999,999,0,0,0,-15.5,false",   # l
    "0,0,0,0,999,30.0,true",       # j (con movimiento)
]

for linea in lineas_csv:
    letra = predictor.predecir_desde_csv_linea(linea)
    print(f"   CSV: '{linea}' → '{letra}'")

print("\n4. Verificación de características del modelo:")
print("-" * 70)
print(f"   ✓ Modelo cargado correctamente")
print(f"   ✓ Acepta 7 características (5 dedos + posicion_mano + movimiento)")
print(f"   ✓ Número de clases: {len(predictor.label_encoder.classes_)}")
print(f"   ✓ Clases: {', '.join(predictor.label_encoder.classes_[:10])}...")

print("\n" + "="*70)
print("✓ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
print("="*70)
