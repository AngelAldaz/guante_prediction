"""
Prueba del predictor con datos reales del CSV
"""
from predictor_lsm import PredictorLSM
import pandas as pd

print("="*70)
print("PRUEBA CON DATOS REALES")
print("="*70)

# Inicializar predictor
predictor = PredictorLSM()

# Cargar datos reales
df = pd.read_csv('datos_reales.csv')

print(f"\n✓ Dataset cargado: {len(df)} muestras")
print(f"✓ Distribución por letra:")
print(df['letra'].value_counts().sort_index())

# Probar con algunas muestras aleatorias
print("\n" + "="*70)
print("PROBANDO PREDICCIONES CON MUESTRAS REALES")
print("="*70)

import random
random.seed(42)

# Tomar 5 muestras aleatorias de cada letra
letras_prueba = ['a', 'b', 'c', 'd', 'e', 'i', 'j', 'l', 's', 'y']
correctas = 0
total = 0

for letra in letras_prueba:
    muestras = df[df['letra'] == letra].sample(min(3, len(df[df['letra'] == letra])))
    
    print(f"\n--- Letra '{letra.upper()}' ---")
    for idx, row in muestras.iterrows():
        prediccion = predictor.predecir(
            row['dedo1'], row['dedo2'], row['dedo3'], 
            row['dedo4'], row['dedo5'], row['posicion_mano'], 
            row['movimiento']
        )
        
        es_correcta = prediccion == row['letra']
        correctas += 1 if es_correcta else 0
        total += 1
        
        resultado = "✓" if es_correcta else "✗"
        print(f"  {resultado} Predicción: '{prediccion}' | Real: '{row['letra']}' | "
              f"Dedos=[{row['dedo1']},{row['dedo2']},{row['dedo3']},{row['dedo4']},{row['dedo5']}] "
              f"Pos={row['posicion_mano']:.2f} Mov={row['movimiento']}")

print("\n" + "="*70)
print(f"RESULTADOS: {correctas}/{total} correctas ({correctas/total*100:.1f}%)")
print("="*70)

# Probar con formato CSV directo
print("\n" + "="*70)
print("PRUEBA CON FORMATO CSV")
print("="*70)

# Tomar la primera fila de cada letra
print("\nPrimera muestra de cada letra (formato CSV):")
for letra in df['letra'].unique()[:10]:
    fila = df[df['letra'] == letra].iloc[0]
    linea_csv = f"{fila['dedo1']},{fila['dedo2']},{fila['dedo3']},{fila['dedo4']},{fila['dedo5']},{fila['posicion_mano']},{fila['movimiento']}"
    
    prediccion = predictor.predecir_desde_csv_linea(linea_csv)
    resultado = "✓" if prediccion == letra else "✗"
    
    print(f"  {resultado} '{letra}': {prediccion}")

print("\n✓ Pruebas completadas")
