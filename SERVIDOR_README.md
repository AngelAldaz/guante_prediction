# 🤟 Servidor LSM - Predictor en Tiempo Real

Servidor Flask para predicción de Lenguaje de Señas Mexicano con interfaz web en tiempo real.

## 🚀 Inicio Rápido

### 1. Iniciar el servidor

```powershell
python servidor.py
```

El servidor se iniciará en `http://localhost:5000`

### 2. Abrir la interfaz web

Abre tu navegador y ve a: `http://localhost:5000`

### 3. Enviar predicciones

El servidor recibirá datos automáticamente y los mostrará en tiempo real en la interfaz web.

## 📡 API Endpoints

### POST /predecir

Recibe datos de sensores y hace predicciones.

**Formato de entrada (JSON):**

```json
[
  "751,79,153,66,128,0.85,False",
  "999,0,0,0,0,0.0,false",
  "751,79,153,66,128,0.85,False"
]
```

O con formato de objeto:

```json
{
  "datos": ["751,79,153,66,128,0.85,False", "999,0,0,0,0,0.0,false"]
}
```

**Formato de valores en cada string:**

```
dedo1,dedo2,dedo3,dedo4,dedo5,posicion_mano,movimiento
```

**Respuesta:**

```json
{
  "success": true,
  "predicciones": ["a", "q", "a"],
  "letras_nuevas": 3,
  "total_letras": 3,
  "parrafo": "aqa"
}
```

### GET /obtener_texto

Obtiene el texto acumulado actual.

**Respuesta:**

```json
{
  "parrafo": "holamundo",
  "total_letras": 9,
  "letras": ["h", "o", "l", "a", "m", "u", "n", "d", "o"]
}
```

### POST /limpiar

Limpia todo el texto acumulado.

**Respuesta:**

```json
{
  "success": true,
  "mensaje": "Texto limpiado"
}
```

### POST /borrar_ultima

Borra la última letra del texto acumulado.

**Respuesta:**

```json
{
  "success": true,
  "letra_borrada": "o",
  "parrafo": "holamund"
}
```

## 🧪 Pruebas

Ejecuta el script de prueba incluido:

```powershell
python test_servidor.py
```

Este script:

1. Envía datos de prueba al servidor
2. Verifica las predicciones
3. Obtiene el texto acumulado
4. Prueba la secuencia completa "holamundo"

## 📝 Ejemplo con cURL

### Enviar predicciones:

```bash
curl -X POST http://localhost:5000/predecir \
  -H "Content-Type: application/json" \
  -d '["751,79,153,66,128,0.85,False","0,825,999,999,826,0.74,False"]'
```

### Obtener texto:

```bash
curl http://localhost:5000/obtener_texto
```

### Limpiar texto:

```bash
curl -X POST http://localhost:5000/limpiar
```

## 📝 Ejemplo con Python (requests)

```python
import requests

# Enviar datos
datos = [
    "751,79,153,66,128,0.85,False",  # a
    "0,825,999,999,826,0.74,False",  # b
    "999,244,854,297,724,1.00,False" # c
]

response = requests.post(
    'http://localhost:5000/predecir',
    json=datos
)

print(response.json())
# {'success': True, 'predicciones': ['a', 'b', 'c'], ...}
```

## 🌐 Interfaz Web

La interfaz web muestra:

- ✅ **Texto reconocido en tiempo real** (actualización cada 2 segundos)
- ✅ **Total de letras acumuladas**
- ✅ **Última actualización**
- ✅ **Botones de control:**
  - 🔄 Actualizar manualmente
  - ⌫ Borrar última letra
  - 🗑️ Limpiar todo el texto

### Características:

- Diseño responsivo (funciona en móviles)
- Actualización automática cada 2 segundos
- Animaciones visuales
- Indicador de estado del sistema
- Interfaz moderna con gradientes

## 🔧 Configuración

### Cambiar puerto

Edita `servidor.py`:

```python
app.run(host='0.0.0.0', port=5000, debug=True)
#                             ↑ Cambia este número
```

### Cambiar intervalo de actualización

Edita `templates/index.html`:

```javascript
let intervalo = setInterval(actualizarTexto, 2000);
//                                            ↑ Milisegundos
```

## 📊 Formato de Datos

Cada string debe contener exactamente 7 valores separados por comas:

1. **dedo1** (0-999): Pulgar
2. **dedo2** (0-999): Índice
3. **dedo3** (0-999): Medio
4. **dedo4** (0-999): Anular
5. **dedo5** (0-999): Meñique
6. **posicion_mano** (float): Posición/ángulo de la mano
7. **movimiento** (True/False): Si hay movimiento

## 🛠️ Tecnologías Utilizadas

- **Backend:** Flask 3.0+
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **ML:** Scikit-learn (Random Forest)
- **CORS:** Flask-CORS para peticiones cross-origin

## 📦 Dependencias

```
flask>=3.0.0
flask-cors>=4.0.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
requests>=2.31.0
```

Instalar con:

```powershell
pip install -r requirements.txt
```

## 🎯 Casos de Uso

1. **Integración con Arduino/ESP32:**
   - Sensores envían datos al servidor
   - Servidor procesa y muestra letras en tiempo real
2. **Sistema de traducción LSM:**
   - Captura gestos de la mano
   - Traduce a texto en pantalla
3. **Aplicación educativa:**
   - Enseñar LSM de forma interactiva
   - Feedback inmediato de gestos

## ⚠️ Notas Importantes

- El servidor mantiene el estado en memoria (las letras se pierden al reiniciar)
- Para producción, considera usar una base de datos
- El modelo debe estar entrenado (`mejor_modelo.pkl`, `scaler.pkl`, `label_encoder.pkl`)
- El servidor acepta peticiones de cualquier origen (CORS habilitado)

## 🐛 Solución de Problemas

### El servidor no inicia

- Verifica que el puerto 5000 no esté en uso
- Asegúrate de tener instaladas las dependencias
- Verifica que los archivos `.pkl` existan

### Las predicciones no aparecen

- Verifica que el formato de datos sea correcto (7 valores)
- Revisa la consola del servidor para errores
- Asegúrate de que el servidor esté corriendo

### Error de CORS

- Ya está configurado Flask-CORS
- Si persiste, verifica la configuración de tu navegador

## 📞 Integración con Hardware

Ejemplo de envío desde Arduino/ESP32:

```cpp
#include <WiFi.h>
#include <HTTPClient.h>

void enviarPrediccion(String datos) {
    HTTPClient http;
    http.begin("http://192.168.1.100:5000/predecir");
    http.addHeader("Content-Type", "application/json");

    String payload = "[\"" + datos + "\"]";
    int httpCode = http.POST(payload);

    if (httpCode == 200) {
        String response = http.getString();
        Serial.println(response);
    }

    http.end();
}
```

---

**Desarrollado para:** ITM - Sistemas Programables (Noveno Semestre)
**Fecha:** Diciembre 2025
