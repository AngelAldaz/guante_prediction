# 🎯 GUÍA RÁPIDA DE IMPLEMENTACIÓN - Modelo LSM

## ✅ Sistema Completado

El modelo de clasificación de Lenguaje de Señas Mexicano está listo con **98.77% de precisión**.

---

## 🚀 Cómo Usar el Modelo

### 1. Instalación (Si no está instalado)

```bash
pip install -r requirements.txt
```

### 2. Uso Básico en Python

```python
from predictor_lsm import PredictorLSM

# Inicializar
predictor = PredictorLSM()

# Predecir una letra
letra = predictor.predecir(
    dedo1=100,    # pulgar (0-999)
    dedo2=0,      # índice
    dedo3=0,      # medio
    dedo4=0,      # anular
    dedo5=0,      # meñique
    movimiento=False
)
print(f"Letra: {letra}")  # Output: 'a'
```

### 3. Desde Formato CSV

```python
from predictor_lsm import PredictorLSM

predictor = PredictorLSM()

# Formato: "dedo1,dedo2,dedo3,dedo4,dedo5,movimiento"
linea_csv = "999,0,0,0,999,false"
letra = predictor.predecir_desde_csv_linea(linea_csv)
print(f"Letra: {letra}")  # Output: 'y'
```

### 4. Con Probabilidades

```python
from predictor_lsm import PredictorLSM

predictor = PredictorLSM()

letra, probabilidades = predictor.predecir_con_probabilidades(
    dedo1=0, dedo2=999, dedo3=999, dedo4=999, dedo5=999,
    movimiento=False
)

print(f"Predicción: {letra}")
print(f"Confianza: {list(probabilidades.values())[0]*100:.1f}%")

# Ver top 3 opciones
for i, (clase, prob) in enumerate(list(probabilidades.items())[:3], 1):
    print(f"{i}. '{clase}': {prob*100:.1f}%")
```

---

## 📊 Resultados de los Modelos Evaluados

| Modelo               | Test Accuracy | CV Accuracy   |
| -------------------- | ------------- | ------------- |
| 🏆 **Random Forest** | **98.77%**    | 98.46% ±0.49% |
| KNN (k=5)            | 97.53%        | 96.60% ±1.16% |
| SVM (RBF)            | 95.68%        | 90.74% ±2.08% |
| KNN (k=3)            | 95.68%        | 96.91% ±0.98% |
| Gradient Boosting    | 95.06%        | 93.21% ±1.22% |
| MLP Neural Network   | 90.74%        | 78.08% ±3.03% |
| SVM (Linear)         | 85.19%        | 79.79% ±1.77% |
| Logistic Regression  | 85.19%        | 82.87% ±1.87% |

**Random Forest** es el ganador con solo 2 errores en 162 predicciones.

---

## 🎮 Integración con Hardware (Arduino/Sensores)

### Ejemplo con Puerto Serial

```python
from predictor_lsm import PredictorLSM
import serial

predictor = PredictorLSM()

# Configurar puerto serial (ajusta el puerto según tu sistema)
ser = serial.Serial('COM3', 9600, timeout=1)

print("Escuchando señales...")

while True:
    if ser.in_waiting > 0:
        # Leer línea desde Arduino
        linea = ser.readline().decode('utf-8').strip()
        print(f"Recibido: {linea}")

        try:
            # Predecir
            letra = predictor.predecir_desde_csv_linea(linea)
            print(f"→ Letra detectada: {letra.upper()}\n")

            # Opcional: enviar respuesta al Arduino
            ser.write(f"{letra}\n".encode())

        except Exception as e:
            print(f"Error: {e}\n")
```

### Código Arduino Ejemplo

```cpp
void loop() {
    // Leer valores de sensores (0-999)
    int dedo1 = analogRead(A0);  // Escalar a rango 0-999
    int dedo2 = analogRead(A1);
    int dedo3 = analogRead(A2);
    int dedo4 = analogRead(A3);
    int dedo5 = analogRead(A4);
    bool movimiento = detectarMovimiento();  // Tu función

    // Enviar en formato CSV
    Serial.print(dedo1);
    Serial.print(",");
    Serial.print(dedo2);
    Serial.print(",");
    Serial.print(dedo3);
    Serial.print(",");
    Serial.print(dedo4);
    Serial.print(",");
    Serial.print(dedo5);
    Serial.print(",");
    Serial.println(movimiento ? "true" : "false");

    delay(500);
}
```

---

## 📁 Archivos del Sistema

- `datos_lsm.csv` - Dataset de 810 muestras
- `mejor_modelo.pkl` - Modelo Random Forest entrenado
- `scaler.pkl` - Escalador de características
- `label_encoder.pkl` - Codificador de etiquetas
- `predictor_lsm.py` - Sistema de predicción

---

## 🔧 Regenerar el Modelo

Si quieres entrenar con datos diferentes:

```bash
# 1. Generar nuevos datos (modifica posiciones_lsm en generar_datos_lsm.py)
python generar_datos_lsm.py

# 2. Comparar modelos y seleccionar el mejor
python comparar_modelos.py

# 3. Usar el nuevo modelo
python predictor_lsm.py
```

---

## 🎯 Configuración de Posiciones

En `generar_datos_lsm.py`, las posiciones están definidas como:

```python
posiciones_lsm = {
    'a': [100, 0, 0, 0, 0],         # Puño cerrado
    'b': [0, 999, 999, 999, 999],   # 4 dedos estirados
    'd': [50, 999, 0, 0, 0],        # Índice levantado
    'i': [0, 0, 0, 0, 999],         # Meñique levantado
    'y': [999, 0, 0, 0, 999],       # Pulgar y meñique
    # ... etc
}
```

Valores:

- **0-150**: Cerrado
- **150-800**: Semi-flexionado
- **800-999**: Estirado

---

## 🧪 Testing

```bash
# Demo rápida
python demo_predictor.py

# Ejemplos completos + modo interactivo
python predictor_lsm.py
```

---

## 📈 Características del Dataset

- **Total muestras**: 810 (30 por letra)
- **Clases**: 27 letras (a-z + ñ)
- **Features**: 6 (5 dedos + movimiento booleano)
- **Train/Test split**: 80/20
- **Validación**: 5-fold cross-validation

---

## ⚡ Optimización

El modelo actual ya tiene excelente rendimiento, pero si necesitas optimizar:

1. **Más datos**: Aumenta `num_muestras` en `generar_datos_lsm.py`
2. **Hiperparámetros**: Ajusta parámetros de Random Forest en `comparar_modelos.py`
3. **Reducir tamaño**: Usa `n_estimators=100` para un modelo más pequeño (trade-off: precisión)

---

## 🆘 Troubleshooting

**Problema**: Import errors

```bash
pip install -r requirements.txt
```

**Problema**: Archivo no encontrado

- Asegúrate de ejecutar desde la carpeta del proyecto
- Verifica que `mejor_modelo.pkl` exista (ejecuta `comparar_modelos.py`)

**Problema**: Baja precisión

- Regenera datos con `generar_datos_lsm.py`
- Verifica que las posiciones sean distintas entre letras similares

---

## 📞 Soporte

Para modificaciones o dudas sobre el modelo, revisa:

- `README.md` - Documentación completa
- Código comentado en cada archivo
- Classification report generado por `comparar_modelos.py`

---

**¡Modelo listo para producción! 🎉**
