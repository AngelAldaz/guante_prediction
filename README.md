# Modelo de Clasificación de Lenguaje de Señas Mexicano (LSM)

Este proyecto implementa un modelo de machine learning para clasificar las 27 letras del abecedario mexicano basándose en la posición de los dedos y movimiento.

## 📁 Archivos del Proyecto

- `generar_datos_lsm.py` - Genera dataset sintético de 810 muestras (30 por letra)
- `comparar_modelos.py` - Compara 8 modelos diferentes de ML
- `predictor_lsm.py` - Sistema de predicción con interfaz interactiva
- `requirements.txt` - Dependencias del proyecto

## 🚀 Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt
```

## 📊 Uso del Sistema

### 1. Generar Datos de Entrenamiento

```bash
python generar_datos_lsm.py
```

Esto generará el archivo `datos_lsm.csv` con 810 muestras (30 por cada letra).

### 2. Entrenar y Comparar Modelos

```bash
python comparar_modelos.py
```

Este script:

- Evalúa 8 modelos diferentes:

  - Random Forest
  - Gradient Boosting
  - SVM (RBF y Linear)
  - KNN (k=3 y k=5)
  - Red Neuronal (MLP)
  - Regresión Logística

- Usa validación cruzada de 5-fold
- Identifica el mejor modelo automáticamente
- Guarda el modelo entrenado en `mejor_modelo.pkl`

### 3. Usar el Predictor

```bash
python predictor_lsm.py
```

## 💻 Ejemplos de Uso Programático

### Ejemplo Básico

```python
from predictor_lsm import PredictorLSM

# Inicializar predictor
predictor = PredictorLSM()

# Predecir letra "A" (puño cerrado)
letra = predictor.predecir(
    dedo1=0,    # pulgar cerrado
    dedo2=0,    # índice cerrado
    dedo3=0,    # medio cerrado
    dedo4=0,    # anular cerrado
    dedo5=0,    # meñique cerrado
    movimiento=False
)
print(f"Predicción: {letra}")  # Output: a
```

### Desde Formato CSV

```python
from predictor_lsm import PredictorLSM

predictor = PredictorLSM()

# Formato CSV: dedo1,dedo2,dedo3,dedo4,dedo5,posicion_mano,movimiento
linea = "999,0,0,0,0,0.0,false"
letra = predictor.predecir_desde_csv_linea(linea)
print(f"Predicción: {letra}")
```

### Con Probabilidades

```python
from predictor_lsm import PredictorLSM

predictor = PredictorLSM()

letra, probabilidades = predictor.predecir_con_probabilidades(
    dedo1=0, dedo2=999, dedo3=0, dedo4=0, dedo5=0,
    posicion_mano=0.0,
    movimiento=False
)

print(f"Letra predicha: {letra}")
print("\nTop 3 probabilidades:")
for clase, prob in list(probabilidades.items())[:3]:
    print(f"  {clase}: {prob*100:.1f}%")
```

## 📋 Formato de Datos

### Entrada

- **dedo1-5**: Valores de 0 (cerrado) a 999 (estirado)

  - 999 = dedo completamente estirado
  - 0 = dedo completamente cerrado
  - Valores intermedios = semi-flexionado

- **movimiento**: Boolean (True/False)
  - True: la letra requiere movimiento
  - False: la letra es estática

### Salida

- Una letra del abecedario mexicano (a-z + ñ)

## 🎯 Características del Dataset

- **Total de muestras**: 810 (30 por letra)
- **Número de clases**: 27 letras
- **Características**: 7 (5 dedos + posición_de_la_mano + movimiento)
- **Variabilidad**: ±50 unidades en cada medición para simular variabilidad real

## 🏆 Modelos Evaluados

El sistema compara automáticamente:

1. **Random Forest** - Ensemble de árboles de decisión
2. **Gradient Boosting** - Boosting secuencial
3. **SVM RBF** - Kernel radial
4. **SVM Linear** - Kernel lineal
5. **KNN (k=3)** - 3 vecinos más cercanos
6. **KNN (k=5)** - 5 vecinos más cercanos
7. **MLP Neural Network** - Red neuronal multicapa
8. **Logistic Regression** - Regresión logística multinomial

El mejor modelo se selecciona automáticamente basándose en accuracy en el conjunto de prueba.

## 📈 Métricas de Evaluación

- **Validación Cruzada (5-fold)**: Para evaluar la generalización
- **Test Accuracy**: Precisión en conjunto de prueba (20%)
- **Classification Report**: Precisión, recall y F1-score por clase
- **Confusion Matrix**: Para identificar errores entre clases similares

## 🔧 Personalización

### Ajustar Posiciones de Letras

Edita el diccionario `posiciones_lsm` en `generar_datos_lsm.py`:

```python
posiciones_lsm = {
    'a': [0, 0, 0, 0, 0],     # Tu configuración personalizada
    # ...
}
```

### Modificar Número de Muestras

En `generar_datos_lsm.py`, cambia el parámetro:

```python
muestras_letra = generar_muestras(letra, posicion, num_muestras=50)  # Era 30
```

### Agregar Más Modelos

En `comparar_modelos.py`, añade al diccionario `modelos`:

```python
modelos = {
    'Tu Modelo': TuClasificador(parametros),
    # ...
}
```

## 🛠️ Integración en Tiempo Real

### Ejemplo con Sensores

```python
from predictor_lsm import PredictorLSM
import serial  # Para Arduino/sensores

predictor = PredictorLSM()

# Leer desde puerto serial
ser = serial.Serial('COM3', 9600)

while True:
    linea = ser.readline().decode('utf-8').strip()
    # Formato esperado: "999,0,0,0,0,0.0,false"

    try:
        letra = predictor.predecir_desde_csv_linea(linea)
        print(f"Letra detectada: {letra}")
    except Exception as e:
        print(f"Error: {e}")
```

## 📊 Estructura de Archivos Generados

```
modelo_LSM/
├── generar_datos_lsm.py
├── comparar_modelos.py
├── predictor_lsm.py
├── requirements.txt
├── README.md
├── datos_lsm.csv              # Generado: Dataset
├── mejor_modelo.pkl           # Generado: Modelo entrenado
├── scaler.pkl                 # Generado: Escalador de datos
├── label_encoder.pkl          # Generado: Codificador de etiquetas
└── info_mejor_modelo.txt      # Generado: Info del modelo
```

## 🧪 Testing

Ejecuta el predictor con ejemplos predefinidos:

```bash
python predictor_lsm.py
```

Para modo interactivo, responde "si" cuando se solicite.

## ⚠️ Notas Importantes

1. **Datos Sintéticos**: Los datos son generados sintéticamente basándose en las posiciones típicas del LSM
2. **Variabilidad**: Se añade ruido gaussiano para simular lecturas reales de sensores
3. **Letras Similares**: Algunas letras (a, e, s) tienen posiciones idénticas - el modelo aprende a diferenciarlas por variaciones sutiles
4. **Movimiento**: Las letras j, z, ñ típicamente requieren movimiento en LSM

## 📝 Licencia

Proyecto educativo para Sistemas Programables - ITM

## 🤝 Contribuciones

Para mejorar las posiciones de las letras o agregar más características, modifica los archivos correspondientes y re-entrena el modelo.

---

**Desarrollado para**: ITM - Sistemas Programables (Noveno Semestre)
