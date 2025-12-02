"""
EJEMPLO COMPLETO DE USO DEL MODELO LSM
======================================

Este script demuestra todas las formas de usar el predictor
"""

from predictor_lsm import PredictorLSM

def ejemplo_1_basico():
    """Ejemplo 1: Uso básico del predictor"""
    print("\n" + "="*70)
    print("EJEMPLO 1: Predicción Básica")
    print("="*70)
    
    predictor = PredictorLSM()
    
    # Predecir letra A (puño cerrado)
    letra = predictor.predecir(
        dedo1=100,  # pulgar ligeramente extendido
        dedo2=0,    # índice cerrado
        dedo3=0,    # medio cerrado
        dedo4=0,    # anular cerrado
        dedo5=0,    # meñique cerrado
        movimiento=False
    )
    
    print(f"\n✓ Predicción: '{letra.upper()}'")
    print(f"  Input: puño cerrado (todos los dedos en 0)")


def ejemplo_2_csv():
    """Ejemplo 2: Predicción desde formato CSV"""
    print("\n" + "="*70)
    print("EJEMPLO 2: Predicción desde CSV")
    print("="*70)
    
    predictor = PredictorLSM()
    
    # Simular datos que vendrían de Arduino/sensores
    lecturas = [
        "100,0,0,0,0,false",       # letra a
        "0,999,999,999,999,false", # letra b
        "50,999,0,0,0,false",      # letra d
        "0,0,0,0,999,false",       # letra i
        "999,0,0,0,999,false",     # letra y
    ]
    
    print("\nProcesando lecturas de sensores:\n")
    
    for linea in lecturas:
        letra = predictor.predecir_desde_csv_linea(linea)
        print(f"  Sensor: {linea:<30} → '{letra.upper()}'")


def ejemplo_3_probabilidades():
    """Ejemplo 3: Predicción con probabilidades"""
    print("\n" + "="*70)
    print("EJEMPLO 3: Predicción con Probabilidades")
    print("="*70)
    
    predictor = PredictorLSM()
    
    # Predecir con confianza
    letra, probs = predictor.predecir_con_probabilidades(
        dedo1=0, dedo2=999, dedo3=999, dedo4=0, dedo5=0,
        movimiento=False
    )
    
    print(f"\n🎯 Predicción: '{letra.upper()}'")
    print(f"\nTop 5 opciones más probables:")
    
    for i, (clase, prob) in enumerate(list(probs.items())[:5], 1):
        barra = "█" * int(prob * 40)
        print(f"  {i}. '{clase.upper()}': {barra} {prob*100:.2f}%")


def ejemplo_4_batch():
    """Ejemplo 4: Procesamiento en lote"""
    print("\n" + "="*70)
    print("EJEMPLO 4: Procesamiento por Lotes")
    print("="*70)
    
    predictor = PredictorLSM()
    
    # Múltiples lecturas
    lecturas = [
        {"nombre": "Letra A", "valores": (100, 0, 0, 0, 0, False)},
        {"nombre": "Letra B", "valores": (0, 999, 999, 999, 999, False)},
        {"nombre": "Letra D", "valores": (50, 999, 0, 0, 0, False)},
        {"nombre": "Letra I", "valores": (0, 0, 0, 0, 999, False)},
        {"nombre": "Letra Y", "valores": (999, 0, 0, 0, 999, False)},
    ]
    
    print("\nProcesando múltiples señas:\n")
    resultados = []
    
    for lectura in lecturas:
        letra = predictor.predecir(*lectura["valores"])
        resultados.append(letra)
        correcto = "✓" if letra == lectura["nombre"].split()[-1].lower() else "✗"
        print(f"  {correcto} {lectura['nombre']}: predicción='{letra.upper()}'")
    
    print(f"\nPalabra formada: {''.join(resultados).upper()}")


def ejemplo_5_validacion():
    """Ejemplo 5: Validación con umbral de confianza"""
    print("\n" + "="*70)
    print("EJEMPLO 5: Validación con Umbral de Confianza")
    print("="*70)
    
    predictor = PredictorLSM()
    
    # Configurar umbral mínimo de confianza
    UMBRAL_CONFIANZA = 0.80  # 80%
    
    casos_prueba = [
        (100, 0, 0, 0, 0, False),       # Caso claro
        (500, 500, 500, 500, 500, False), # Caso ambiguo (c u o)
        (0, 999, 999, 999, 999, False), # Caso claro
    ]
    
    print(f"\nValidando predicciones (umbral: {UMBRAL_CONFIANZA*100:.0f}%)\n")
    
    for i, valores in enumerate(casos_prueba, 1):
        letra, probs = predictor.predecir_con_probabilidades(*valores)
        confianza = list(probs.values())[0]
        
        if confianza >= UMBRAL_CONFIANZA:
            estado = "✓ ACEPTADA"
            color = ""
        else:
            estado = "⚠ REVISAR"
            color = " (baja confianza)"
        
        print(f"  Caso {i}: '{letra.upper()}' - {confianza*100:.1f}% {estado}{color}")
        
        if confianza < UMBRAL_CONFIANZA:
            print(f"    Top alternativas: ", end="")
            alts = list(probs.items())[:3]
            print(", ".join([f"'{c}':{p*100:.0f}%" for c, p in alts]))


def ejemplo_6_stream():
    """Ejemplo 6: Simulación de stream en tiempo real"""
    print("\n" + "="*70)
    print("EJEMPLO 6: Simulación de Stream en Tiempo Real")
    print("="*70)
    
    import time
    
    predictor = PredictorLSM()
    
    # Simular lecturas continuas
    stream = [
        "100,0,0,0,0,false",       # a
        "0,999,999,999,999,false", # b
        "600,600,600,600,600,false", # c
        "50,999,0,0,0,false",      # d
    ]
    
    print("\n🔴 Iniciando captura en tiempo real...\n")
    
    palabra = []
    for i, linea in enumerate(stream, 1):
        time.sleep(0.5)  # Simular delay de lectura
        
        letra = predictor.predecir_desde_csv_linea(linea)
        palabra.append(letra)
        
        print(f"  [{i}/4] Detectado: '{letra.upper()}' | Palabra actual: {''.join(palabra).upper()}")
    
    print(f"\n✓ Captura completa: {' '.join(palabra).upper()}")


def menu():
    """Menú interactivo"""
    print("\n" + "="*70)
    print("🎓 EJEMPLOS DE USO DEL MODELO LSM")
    print("="*70)
    print("\nSelecciona un ejemplo:")
    print("\n  1. Predicción Básica")
    print("  2. Desde Formato CSV")
    print("  3. Con Probabilidades")
    print("  4. Procesamiento por Lotes")
    print("  5. Validación con Umbral")
    print("  6. Stream en Tiempo Real")
    print("  7. Ejecutar TODOS los ejemplos")
    print("  0. Salir")
    
    return input("\nOpción: ").strip()


if __name__ == "__main__":
    while True:
        opcion = menu()
        
        if opcion == "1":
            ejemplo_1_basico()
        elif opcion == "2":
            ejemplo_2_csv()
        elif opcion == "3":
            ejemplo_3_probabilidades()
        elif opcion == "4":
            ejemplo_4_batch()
        elif opcion == "5":
            ejemplo_5_validacion()
        elif opcion == "6":
            ejemplo_6_stream()
        elif opcion == "7":
            ejemplo_1_basico()
            ejemplo_2_csv()
            ejemplo_3_probabilidades()
            ejemplo_4_batch()
            ejemplo_5_validacion()
            ejemplo_6_stream()
        elif opcion == "0":
            print("\n✓ Saliendo...\n")
            break
        else:
            print("\n❌ Opción inválida")
        
        input("\nPresiona ENTER para continuar...")
