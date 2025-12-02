import pandas as pd
import numpy as np
import random

# Configuración de semilla para reproducibilidad
np.random.seed(42)
random.seed(42)

def generar_variacion(valor_base, variacion=30):
    """Genera una variación aleatoria alrededor de un valor base"""
    if valor_base >= 900:
        return min(999, max(850, valor_base + np.random.randint(-variacion, variacion+1)))
    elif valor_base <= 100:
        return max(0, min(150, valor_base + np.random.randint(-variacion, variacion+1)))
    else:
        return max(0, min(999, valor_base + np.random.randint(-variacion, variacion+1)))

# Definición de posiciones de dedos para cada letra del LSM (Lenguaje de Señas Mexicano)
# Formato: [pulgar, índice, medio, anular, meñique]
# 999 = estirado, 0 = cerrado, valores intermedios = semi-flexionado
posiciones_lsm = {
    'a': [999, 0, 0, 0, 0],         # Pulgar estirado, resto cerrado
    'b': [0, 999, 999, 999, 999],   # Todos los dedos estirados excepto pulgar
    'c': [600, 600, 600, 600, 600], # Mano en forma de C
    'd': [50, 999, 0, 0, 0],        # Solo índice levantado
    'e': [0, 50, 50, 50, 50],       # Puño cerrado con dedos ligeramente doblados
    'f': [999, 100, 999, 999, 999], # Pulgar toca índice, otros estirados
    'g': [999, 999, 50, 0, 0],      # Pulgar e índice estirados horizontalmente
    'h': [999, 999, 999, 50, 0],    # Pulgar, índice y medio estirados
    'i': [0, 0, 0, 0, 999],         # Solo meñique levantado
    'j': [0, 0, 0, 50, 999],        # Meñique levantado (con movimiento)
    'k': [999, 999, 999, 100, 50],  # Similar a H pero con variación
    'l': [999, 999, 100, 0, 0],     # Pulgar e índice en L
    'm': [150, 350, 350, 350, 50],  # Tres dedos doblados sobre pulgar
    'n': [150, 350, 350, 50, 0],    # Dos dedos doblados sobre pulgar
    'o': [400, 400, 400, 400, 400], # Mano en forma de O (diferente de C)
    'p': [999, 999, 600, 0, 0],     # Índice y medio apuntando abajo
    'q': [999, 999, 100, 50, 0],    # Pulgar e índice apuntando abajo
    'r': [50, 999, 999, 50, 0],     # Índice y medio cruzados
    's': [50, 100, 100, 100, 100],  # Puño cerrado diferenciado
    't': [200, 400, 0, 0, 0],       # Pulgar entre índice y medio
    'u': [0, 999, 999, 100, 0],     # Índice y medio juntos estirados
    'v': [0, 999, 999, 200, 100],   # Índice y medio separados (similar a U)
    'w': [50, 999, 999, 999, 50],   # Índice, medio y anular estirados
    'x': [0, 600, 0, 0, 0],         # Índice doblado (diferente de d)
    'y': [999, 0, 0, 0, 999],       # Pulgar y meñique estirados
    'z': [50, 999, 100, 50, 0],     # Índice hace Z en el aire
    'ñ': [100, 999, 999, 999, 999], # Similar a B pero con variación
}

# Letras que típicamente tienen movimiento en LSM
letras_con_movimiento = ['j', 'z', 'ñ']

def generar_muestras(letra, posicion_base, num_muestras=30):
    """Genera muestras con variaciones para una letra específica"""
    muestras = []
    tiene_movimiento = letra in letras_con_movimiento
    
    for i in range(num_muestras):
        # Generar variaciones en los valores de los dedos
        dedo1 = generar_variacion(posicion_base[0])
        dedo2 = generar_variacion(posicion_base[1])
        dedo3 = generar_variacion(posicion_base[2])
        dedo4 = generar_variacion(posicion_base[3])
        dedo5 = generar_variacion(posicion_base[4])
        # Generar una posición de la mano (valor real, puede ser negativo o positivo)
        # Rango elegido: -90.0 a 90.0 grados (puede adaptarse según necesidades)
        posicion_mano = round(np.random.uniform(-90.0, 90.0), 2)
        
        # Para letras con movimiento, alternar entre True y False
        if tiene_movimiento:
            movimiento = i % 2 == 0
        else:
            # Para otras letras, ocasionalmente agregar movimiento para variabilidad
            movimiento = random.random() < 0.2
        
        muestras.append({
            'dedo1': dedo1,
            'dedo2': dedo2,
            'dedo3': dedo3,
            'dedo4': dedo4,
            'dedo5': dedo5,
            'posicion_mano': posicion_mano,
            'movimiento': movimiento,
            'letra': letra
        })
    
    return muestras

# Generar dataset completo
print("Generando dataset de Lenguaje de Señas Mexicano...")
todas_las_muestras = []

for letra, posicion in posiciones_lsm.items():
    muestras_letra = generar_muestras(letra, posicion)
    todas_las_muestras.extend(muestras_letra)
    print(f"Letra '{letra}': {len(muestras_letra)} muestras generadas")

# Crear DataFrame
df = pd.DataFrame(todas_las_muestras)

# Mezclar el dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Guardar a CSV
output_file = 'datos_lsm.csv'
df.to_csv(output_file, index=False, sep=',')

print(f"\n✓ Dataset generado exitosamente: {output_file}")
print(f"  Total de muestras: {len(df)}")
print(f"  Número de clases (letras): {df['letra'].nunique()}")
print(f"\nDistribución de clases:")
print(df['letra'].value_counts().sort_index())
print(f"\nPrimeras filas del dataset:")
print(df.head(10))
