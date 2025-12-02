import pickle
import numpy as np
import pandas as pd

class PredictorLSM:
    """
    Predictor de Lenguaje de Señas Mexicano
    
    Uso:
        predictor = PredictorLSM()
        letra = predictor.predecir(dedo1=999, dedo2=0, dedo3=0, dedo4=0, dedo5=0, posicion_mano=0.0, movimiento=False)
    """
    
    def __init__(self, modelo_path='mejor_modelo.pkl', 
                 scaler_path='scaler.pkl', 
                 encoder_path='label_encoder.pkl'):
        """Inicializar el predictor cargando el modelo entrenado"""
        print("Cargando modelo de predicción LSM...")
        
        with open(modelo_path, 'rb') as f:
            self.modelo = pickle.load(f)
        
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        
        with open(encoder_path, 'rb') as f:
            self.label_encoder = pickle.load(f)
        
        print(f"✓ Modelo cargado exitosamente")
        # print(f"✓ Clases disponibles: {', '.join(self.label_encoder.classes_)}")
    
    def predecir(self, dedo1, dedo2, dedo3, dedo4, dedo5, posicion_mano, movimiento):
        """
        Predecir la letra basándose en los valores de los dedos y movimiento
        
        Args:
            dedo1-5: Valores de 0 (cerrado) a 999 (estirado)
            movimiento: True o False
        
        Returns:
            str: Letra predicha
        """
        # Convertir movimiento a entero
        movimiento_int = 1 if movimiento else 0
        
        # Crear DataFrame con nombres de características para evitar warnings
        import pandas as pd
        X = pd.DataFrame([[dedo1, dedo2, dedo3, dedo4, dedo5, posicion_mano, movimiento_int]], 
                columns=['dedo1', 'dedo2', 'dedo3', 'dedo4', 'dedo5', 'posicion_mano', 'movimiento'])
        
        # Escalar
        X_scaled = self.scaler.transform(X)
        
        # Predecir
        y_pred = self.modelo.predict(X_scaled)
        
        # Decodificar
        letra = self.label_encoder.inverse_transform(y_pred)[0]
        
        return letra
    
    def predecir_con_probabilidades(self, dedo1, dedo2, dedo3, dedo4, dedo5, posicion_mano, movimiento):
        """
        Predecir con probabilidades para cada clase
        
        Returns:
            tuple: (letra_predicha, dict_probabilidades)
        """
        # Convertir movimiento a entero
        movimiento_int = 1 if movimiento else 0
        
        # Crear DataFrame con nombres de características
        import pandas as pd
        X = pd.DataFrame([[dedo1, dedo2, dedo3, dedo4, dedo5, posicion_mano, movimiento_int]], 
                columns=['dedo1', 'dedo2', 'dedo3', 'dedo4', 'dedo5', 'posicion_mano', 'movimiento'])
        
        # Escalar
        X_scaled = self.scaler.transform(X)
        
        # Predecir
        y_pred = self.modelo.predict(X_scaled)
        letra = self.label_encoder.inverse_transform(y_pred)[0]
        
        # Obtener probabilidades si el modelo lo soporta
        if hasattr(self.modelo, 'predict_proba'):
            probabilidades = self.modelo.predict_proba(X_scaled)[0]
            prob_dict = {
                clase: prob 
                for clase, prob in zip(self.label_encoder.classes_, probabilidades)
            }
            # Ordenar por probabilidad
            prob_dict = dict(sorted(prob_dict.items(), key=lambda x: x[1], reverse=True))
        else:
            prob_dict = {letra: 1.0}
        
        return letra, prob_dict
    
    def predecir_desde_csv_linea(self, linea_csv):
        """
        Predecir desde una línea CSV
        
        Args:
            linea_csv: String en formato "dedo1,dedo2,dedo3,dedo4,dedo5,movimiento"
                      Ejemplo: "999,0,0,0,0,false"
        
        Returns:
            str: Letra predicha
        """
        valores = linea_csv.strip().rstrip(';').split(',')
        
        if len(valores) != 7:
            raise ValueError(f"Se esperan 7 valores (dedo1..dedo5,posicion_mano,movimiento), se recibieron {len(valores)}")
        
        dedo1 = int(valores[0])
        dedo2 = int(valores[1])
        dedo3 = int(valores[2])
        dedo4 = int(valores[3])
        dedo5 = int(valores[4])
        posicion_mano = float(valores[5])
        movimiento = valores[6].lower() in ['true', '1', 'yes', 'si', 'sí']
        
        return self.predecir(dedo1, dedo2, dedo3, dedo4, dedo5, posicion_mano, movimiento)


def ejemplos_uso():
    """Ejemplos de uso del predictor"""
    print("="*70)
    print("EJEMPLOS DE USO DEL PREDICTOR LSM")
    print("="*70)
    
    # Inicializar predictor
    predictor = PredictorLSM()
    
    print("\n1. Predicciones con valores directos:")
    print("-" * 70)
    
    ejemplos = [
        {"dedo1": 0, "dedo2": 0, "dedo3": 0, "dedo4": 0, "dedo5": 0, "posicion_mano": 0.0, "movimiento": False, "esperada": "a"},
        {"dedo1": 0, "dedo2": 999, "dedo3": 999, "dedo4": 999, "dedo5": 999, "posicion_mano": 5.0, "movimiento": False, "esperada": "b"},
        {"dedo1": 0, "dedo2": 999, "dedo3": 0, "dedo4": 0, "dedo5": 0, "posicion_mano": -3.0, "movimiento": False, "esperada": "d"},
        {"dedo1": 0, "dedo2": 0, "dedo3": 0, "dedo4": 0, "dedo5": 999, "posicion_mano": 15.0, "movimiento": True, "esperada": "j"},
        {"dedo1": 999, "dedo2": 0, "dedo3": 0, "dedo4": 0, "dedo5": 999, "posicion_mano": 0.0, "movimiento": False, "esperada": "y"},
    ]
    
    for ej in ejemplos:
        letra = predictor.predecir(
            ej["dedo1"], ej["dedo2"], ej["dedo3"], 
            ej["dedo4"], ej["dedo5"], ej["posicion_mano"], ej["movimiento"]
        )
        correcto = "✓" if letra == ej["esperada"] else "✗"
        print(f"   {correcto} Entrada: dedos=[{ej['dedo1']},{ej['dedo2']},{ej['dedo3']},{ej['dedo4']},{ej['dedo5']}], "
              f"pos={ej['posicion_mano']}, mov={ej['movimiento']} → Predicción: '{letra}' (esperada: '{ej['esperada']}')")
    
    print("\n2. Predicciones desde formato CSV:")
    print("-" * 70)
    
    lineas_csv = [
        "999,000,000,000,000,0.0,false",  # a
        "0,999,999,999,999,5.0,false",    # b
        "999,999,0,0,0,-2.5,false",       # l
        "0,999,999,0,0,0.0,false",        # u/v
    ]
    
    for linea in lineas_csv:
        letra = predictor.predecir_desde_csv_linea(linea)
        print(f"   CSV: '{linea}' → Predicción: '{letra}'")
    
    print("\n3. Predicción con probabilidades:")
    print("-" * 70)
    
    letra, probs = predictor.predecir_con_probabilidades(0, 0, 0, 0, 0, 0.0, False)
    print(f"   Entrada: puño cerrado")
    print(f"   Predicción: '{letra}'")
    print(f"   Top 5 probabilidades:")
    for i, (clase, prob) in enumerate(list(probs.items())[:5], 1):
        print(f"      {i}. '{clase}': {prob:.4f} ({prob*100:.2f}%)")


def predecir_interactivo():
    """Modo interactivo para hacer predicciones"""
    print("\n" + "="*70)
    print("MODO INTERACTIVO - Ingresa valores para predecir")
    print("="*70)
    
    predictor = PredictorLSM()
    
    print("\nIngresa los valores (0-999) para cada dedo:")
    print("(999 = estirado, 0 = cerrado)")
    
    try:
        dedo1 = int(input("  Pulgar (dedo1): "))
        dedo2 = int(input("  Índice (dedo2): "))
        dedo3 = int(input("  Medio (dedo3): "))
        dedo4 = int(input("  Anular (dedo4): "))
        dedo5 = int(input("  Meñique (dedo5): "))
        posicion_input = input("  Posición de la mano (número real, puede ser negativo, ejemplo 0, -12.5, 30): ")
        posicion_mano = float(posicion_input)
        movimiento_input = input("  ¿Hay movimiento? (si/no): ").lower()
        movimiento = movimiento_input in ['si', 'sí', 's', 'yes', 'y', 'true', '1']
        
        letra, probs = predictor.predecir_con_probabilidades(
            dedo1, dedo2, dedo3, dedo4, dedo5, posicion_mano, movimiento
        )
        
        print(f"\n{'='*70}")
        print(f"🎯 PREDICCIÓN: '{letra.upper()}'")
        print(f"{'='*70}")
        print("\nTop 3 opciones más probables:")
        for i, (clase, prob) in enumerate(list(probs.items())[:3], 1):
            barra = "█" * int(prob * 30)
            print(f"   {i}. '{clase}': {barra} {prob*100:.1f}%")
        
    except ValueError as e:
        print(f"\n❌ Error: Ingresa valores numéricos válidos")
    except KeyboardInterrupt:
        print("\n\nSaliendo...")


if __name__ == "__main__":
    import sys
    
    # Ejecutar ejemplos por defecto
    ejemplos_uso()
    
    # Preguntar si desea modo interactivo
    print("\n" + "="*70)
    respuesta = input("\n¿Deseas probar el modo interactivo? (si/no): ").lower()
    if respuesta in ['si', 'sí', 's', 'yes', 'y']:
        predecir_interactivo()
    
    print("\n✓ Programa finalizado")
