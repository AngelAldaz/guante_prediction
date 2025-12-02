"""
Script de prueba para enviar datos al servidor LSM
"""
import requests
import json
import time

# URL del servidor
URL_BASE = "http://localhost:5000"

def test_predecir():
    """Envía datos de prueba al servidor"""
    
    print("="*70)
    print("PRUEBA DE SERVIDOR LSM")
    print("="*70)
    
    # Datos de ejemplo (mezcla de diferentes letras)
    datos_prueba = [
        "751,79,153,66,128,0.85,False",      # a
        "0,825,999,999,826,0.74,False",      # b
        "999,244,854,297,724,1.00,False",    # c
        "256,825,497,184,141,0.89,False",    # d
        "0,74,51,41,72,0.99,False",          # e
    ]
    
    print(f"\n📤 Enviando {len(datos_prueba)} muestras al servidor...")
    print("-" * 70)
    
    try:
        response = requests.post(
            f"{URL_BASE}/predecir",
            json=datos_prueba,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            resultado = response.json()
            print("✓ Respuesta exitosa:")
            print(f"  • Predicciones: {resultado['predicciones']}")
            print(f"  • Letras nuevas: {resultado['letras_nuevas']}")
            print(f"  • Total de letras: {resultado['total_letras']}")
            print(f"  • Párrafo actual: '{resultado['parrafo']}'")
            print("\n✓ Prueba completada exitosamente")
        else:
            print(f"✗ Error {response.status_code}: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("✗ Error: No se pudo conectar al servidor")
        print("  Asegúrate de que el servidor esté corriendo en http://localhost:5000")
    except Exception as e:
        print(f"✗ Error inesperado: {e}")

def test_obtener_texto():
    """Obtiene el texto actual del servidor"""
    
    print("\n" + "="*70)
    print("OBTENER TEXTO ACTUAL")
    print("="*70)
    
    try:
        response = requests.get(f"{URL_BASE}/obtener_texto")
        
        if response.status_code == 200:
            resultado = response.json()
            print(f"\n📝 Párrafo completo: '{resultado['parrafo']}'")
            print(f"📊 Total de letras: {resultado['total_letras']}")
            print(f"📋 Letras individuales: {resultado['letras']}")
        else:
            print(f"✗ Error {response.status_code}: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("✗ Error: No se pudo conectar al servidor")
    except Exception as e:
        print(f"✗ Error inesperado: {e}")

def test_secuencia_completa():
    """Prueba enviando varias secuencias de letras"""
    
    print("\n" + "="*70)
    print("PRUEBA DE SECUENCIA COMPLETA")
    print("="*70)
    
    # Limpiar primero
    print("\n1. Limpiando texto anterior...")
    try:
        response = requests.post(f"{URL_BASE}/limpiar")
        if response.status_code == 200:
            print("   ✓ Texto limpiado")
    except:
        print("   ✗ Error al limpiar")
    
    time.sleep(1)
    
    # Enviar primera secuencia: "hola"
    print("\n2. Enviando primera secuencia (H-O-L-A)...")
    secuencia1 = [
        "999,874,999,854,366,0.73,False",    # h
        "149,95,211,79,199,1.01,False",      # o
        "923,665,95,70,204,1.02,False",      # l
        "751,79,153,66,128,0.85,False",      # a
    ]
    
    try:
        response = requests.post(f"{URL_BASE}/predecir", json=secuencia1)
        if response.status_code == 200:
            resultado = response.json()
            print(f"   ✓ Predicciones: {resultado['predicciones']}")
            print(f"   ✓ Párrafo: '{resultado['parrafo']}'")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    time.sleep(2)
    
    # Enviar segunda secuencia: "mundo"
    print("\n3. Enviando segunda secuencia (M-U-N-D-O)...")
    secuencia2 = [
        "184,687,999,569,244,0.95,False",    # m
        "30,947,999,62,289,1.02,False",      # u
        "11,999,999,86,219,1.10,False",      # n
        "256,825,497,184,141,0.89,False",    # d
        "149,95,211,79,199,1.01,False",      # o
    ]
    
    try:
        response = requests.post(f"{URL_BASE}/predecir", json=secuencia2)
        if response.status_code == 200:
            resultado = response.json()
            print(f"   ✓ Predicciones: {resultado['predicciones']}")
            print(f"   ✓ Párrafo completo: '{resultado['parrafo']}'")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    time.sleep(1)
    
    # Obtener texto final
    print("\n4. Obteniendo texto final...")
    test_obtener_texto()
    
    print("\n" + "="*70)
    print("✓ Prueba de secuencia completada")
    print("="*70)

if __name__ == "__main__":
    print("\n🚀 Iniciando pruebas del servidor LSM...\n")
    
    # Prueba 1: Predicción simple
    test_predecir()
    
    time.sleep(2)
    
    # Prueba 2: Obtener texto
    test_obtener_texto()
    
    time.sleep(2)
    
    # Prueba 3: Secuencia completa
    test_secuencia_completa()
    
    print("\n" + "="*70)
    print("🎉 TODAS LAS PRUEBAS COMPLETADAS")
    print("="*70)
    print("\nAhora puedes:")
    print("  • Abrir http://localhost:5000 en tu navegador")
    print("  • Ver el texto acumulado en tiempo real")
    print("  • Usar los botones para limpiar o borrar letras")
    print("="*70 + "\n")
