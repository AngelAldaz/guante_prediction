"""
Servidor Flask para predicción de Lenguaje de Señas Mexicano
Recibe datos de sensores y muestra las predicciones acumuladas
"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from predictor_lsm import PredictorLSM
import json

app = Flask(__name__)
CORS(app)  # Permitir peticiones desde cualquier origen

# Inicializar el predictor
print("Inicializando predictor LSM...")
predictor = PredictorLSM()
print("✓ Servidor listo\n")

# Variable global para acumular las letras predichas
letras_acumuladas = []

@app.route('/')
def index():
    """Página principal que muestra las letras acumuladas"""
    return render_template('index.html')

@app.route('/predecir', methods=['POST'])
def predecir():
    """
    Endpoint para recibir datos y hacer predicciones
    
    Formato esperado:
    {
        "datos": [
            "751,79,153,66,128,0.85,False",
            "999,0,0,0,0,0.0,false",
            ...
        ]
    }
    
    O simplemente un array:
    [
        "751,79,153,66,128,0.85,False",
        "999,0,0,0,0,0.0,false",
        ...
    ]
    """
    try:
        datos = request.json
        
        # Manejar diferentes formatos de entrada
        if isinstance(datos, dict) and 'datos' in datos:
            lineas = datos['datos']
        elif isinstance(datos, list):
            lineas = datos
        else:
            return jsonify({
                'error': 'Formato inválido. Enviar array de strings o {datos: [...]}'
            }), 400
        
        # Predecir cada línea
        predicciones = []
        for linea in lineas:
            try:
                letra = predictor.predecir_desde_csv_linea(linea)
                predicciones.append(letra)
                letras_acumuladas.append(letra)
            except Exception as e:
                print(f"Error procesando línea '{linea}': {e}")
                continue
        
        # Crear el párrafo completo (sin espacios)
        parrafo = ''.join(letras_acumuladas)
        
        return jsonify({
            'success': True,
            'predicciones': predicciones,
            'letras_nuevas': len(predicciones),
            'total_letras': len(letras_acumuladas),
            'parrafo': parrafo
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/obtener_texto', methods=['GET'])
def obtener_texto():
    """Obtiene el texto acumulado actual"""
    parrafo = ''.join(letras_acumuladas)
    return jsonify({
        'parrafo': parrafo,
        'total_letras': len(letras_acumuladas),
        'letras': letras_acumuladas
    })

@app.route('/limpiar', methods=['POST'])
def limpiar():
    """Limpia el texto acumulado"""
    global letras_acumuladas
    letras_acumuladas = []
    return jsonify({
        'success': True,
        'mensaje': 'Texto limpiado'
    })

@app.route('/borrar_ultima', methods=['POST'])
def borrar_ultima():
    """Borra la última letra del texto acumulado"""
    global letras_acumuladas
    if letras_acumuladas:
        letra_borrada = letras_acumuladas.pop()
        return jsonify({
            'success': True,
            'letra_borrada': letra_borrada,
            'parrafo': ''.join(letras_acumuladas)
        })
    else:
        return jsonify({
            'success': False,
            'mensaje': 'No hay letras para borrar'
        })

if __name__ == '__main__':
    print("="*70)
    print("SERVIDOR LSM - Predictor de Lenguaje de Señas Mexicano")
    print("="*70)
    print("\nEndpoints disponibles:")
    print("  • GET  /                  - Página principal")
    print("  • POST /predecir          - Hacer predicciones")
    print("  • GET  /obtener_texto     - Obtener texto actual")
    print("  • POST /limpiar           - Limpiar texto")
    print("  • POST /borrar_ultima     - Borrar última letra")
    print("\n" + "="*70)
    print("Servidor corriendo en: http://localhost:3000")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=3000, debug=True)
