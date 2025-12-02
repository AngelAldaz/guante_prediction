# ⚡ INICIO RÁPIDO - Modelo LSM

## 🎯 Ejecuta esto para empezar:

```bash
# 1. Instalar dependencias
pip install pandas numpy scikit-learn

# 2. Generar datos sintéticos
python generar_datos_lsm.py

# 3. Entrenar y comparar modelos
python comparar_modelos.py

# 4. Probar el sistema
python demo_predictor.py
```

## 🚀 Tu primer predicción en 3 líneas:

```python
from predictor_lsm import PredictorLSM
predictor = PredictorLSM()
print(predictor.predecir(100, 0, 0, 0, 0, False))  # Output: 'a'
```

## 📊 Resultados Esperados:

- ✅ Dataset: 810 muestras (27 letras × 30)
- ✅ Mejor Modelo: **Random Forest** con **98.77%** de precisión
- ✅ Solo 2 errores de 162 predicciones

## 🎮 Formato de Entrada:

```python
predictor.predecir(
    dedo1=999,    # 0-999: Pulgar
    dedo2=0,      # 0-999: Índice
    dedo3=0,      # 0-999: Medio
    dedo4=0,      # 0-999: Anular
    dedo5=999,    # 0-999: Meñique
    movimiento=False  # True/False
)
# Output: 'y'
```

## 📋 Valores de Referencia:

| Letra | Pulgar | Índice | Medio | Anular | Meñique | Movimiento |
| ----- | ------ | ------ | ----- | ------ | ------- | ---------- |
| A     | 100    | 0      | 0     | 0      | 0       | ✗          |
| B     | 0      | 999    | 999   | 999    | 999     | ✗          |
| D     | 50     | 999    | 0     | 0      | 0       | ✗          |
| I     | 0      | 0      | 0     | 0      | 999     | ✗          |
| Y     | 999    | 0      | 0     | 0      | 999     | ✗          |

## 🔌 Integración con Arduino:

### Python:

```python
from predictor_lsm import PredictorLSM
import serial

predictor = PredictorLSM()
ser = serial.Serial('COM3', 9600)

while True:
    linea = ser.readline().decode().strip()
    letra = predictor.predecir_desde_csv_linea(linea)
    print(f"Letra: {letra}")
```

### Arduino:

```cpp
// Enviar en formato CSV
Serial.print(dedo1); Serial.print(",");
Serial.print(dedo2); Serial.print(",");
Serial.print(dedo3); Serial.print(",");
Serial.print(dedo4); Serial.print(",");
Serial.print(dedo5); Serial.print(",");
Serial.println(movimiento ? "true" : "false");
```

## 📖 Más Información:

- **Documentación completa**: `README.md`
- **Guía de implementación**: `GUIA_IMPLEMENTACION.md`
- **Ejemplos avanzados**: `ejemplos_uso.py`
- **Análisis del sistema**: `analisis_resultados.py`

## ❓ Resolución de Problemas:

**Error de imports:**

```bash
pip install -r requirements.txt
```

**Modelo no encontrado:**

```bash
python comparar_modelos.py
```

**Baja precisión:**

- Verifica que los valores estén en rango 0-999
- Revisa que el dataset se generó correctamente
- Re-entrena el modelo

## 🎓 Sistema Completado:

✅ 810 muestras generadas  
✅ 8 modelos comparados  
✅ 98.77% de precisión  
✅ Listo para producción

---

**¡Empieza a predecir señas ahora!** 🤟
