import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("COMPARACIÓN DE MODELOS PARA CLASIFICACIÓN DE LENGUAJE DE SEÑAS MEXICANO")
print("="*70)

# Cargar datos
print("\n1. Cargando dataset...")
df = pd.read_csv('datos_reales.csv', on_bad_lines='skip')
print(f"   ✓ Dataset cargado: {len(df)} muestras, {df['letra'].nunique()} clases")

# Preparar datos
print("\n2. Preparando datos...")
X = df[['dedo1', 'dedo2', 'dedo3', 'dedo4', 'dedo5', 'posicion_mano', 'movimiento']]
X['movimiento'] = X['movimiento'].astype(int)  # Convertir booleano a entero
y = df['letra']

# Codificar etiquetas
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Escalar características
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"   ✓ Características: {X.shape[1]}")
print(f"   ✓ Muestras de entrenamiento: {len(X)}")

# Dividir en train y test
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)
print(f"   ✓ Train: {len(X_train)} | Test: {len(X_test)}")

# Definir modelos a evaluar
print("\n3. Evaluando modelos con validación cruzada (5-fold)...")
print("-" * 70)

modelos = {
    'Random Forest': RandomForestClassifier(n_estimators=200, max_depth=20, random_state=42, n_jobs=-1),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=200, max_depth=5, random_state=42),
    'SVM (RBF)': SVC(kernel='rbf', C=10, gamma='scale', random_state=42),
    'SVM (Linear)': SVC(kernel='linear', C=1, random_state=42),
    'KNN (k=5)': KNeighborsClassifier(n_neighbors=5, weights='distance'),
    'KNN (k=3)': KNeighborsClassifier(n_neighbors=3, weights='distance'),
    'MLP Neural Network': MLPClassifier(hidden_layer_sizes=(128, 64, 32), max_iter=500, random_state=42, early_stopping=True),
    'Logistic Regression': LogisticRegression(max_iter=1000, C=1.0, random_state=42, multi_class='multinomial')
}

resultados = {}

for nombre, modelo in modelos.items():
    print(f"\n   Evaluando {nombre}...")
    
    # Validación cruzada
    cv_scores = cross_val_score(modelo, X_train, y_train, cv=5, scoring='accuracy', n_jobs=-1)
    
    # Entrenar con todo el conjunto de entrenamiento
    modelo.fit(X_train, y_train)
    
    # Evaluar en test
    y_pred = modelo.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    
    # Guardar resultados
    resultados[nombre] = {
        'modelo': modelo,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std(),
        'test_accuracy': test_accuracy,
        'y_pred': y_pred
    }
    
    print(f"      • CV Accuracy: {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
    print(f"      • Test Accuracy: {test_accuracy:.4f}")

# Mostrar resumen de resultados
print("\n" + "="*70)
print("4. RESUMEN DE RESULTADOS")
print("="*70)
print(f"{'Modelo':<25} {'CV Accuracy':<20} {'Test Accuracy':<15}")
print("-" * 70)

# Ordenar por test accuracy
resultados_ordenados = sorted(resultados.items(), key=lambda x: x[1]['test_accuracy'], reverse=True)

for nombre, res in resultados_ordenados:
    cv_str = f"{res['cv_mean']:.4f} (±{res['cv_std']:.4f})"
    print(f"{nombre:<25} {cv_str:<20} {res['test_accuracy']:.4f}")

# Identificar el mejor modelo
mejor_modelo_nombre = resultados_ordenados[0][0]
mejor_modelo_info = resultados_ordenados[0][1]

print("\n" + "="*70)
print(f"🏆 MEJOR MODELO: {mejor_modelo_nombre}")
print(f"   • Test Accuracy: {mejor_modelo_info['test_accuracy']:.4f}")
print("="*70)

# Mostrar reporte detallado del mejor modelo
print(f"\n5. Reporte Detallado del Mejor Modelo ({mejor_modelo_nombre}):")
print("-" * 70)
print("\nClassification Report:")
print(classification_report(y_test, mejor_modelo_info['y_pred'], 
                          target_names=le.classes_, zero_division=0))

# Matriz de confusión (solo mostrar si hay errores)
cm = confusion_matrix(y_test, mejor_modelo_info['y_pred'])
errores = np.sum(cm) - np.trace(cm)
if errores > 0:
    print(f"\nErrores de clasificación: {errores}/{len(y_test)}")
    print("\nLetras con más errores:")
    errores_por_clase = []
    for i, letra in enumerate(le.classes_):
        total = np.sum(cm[i, :])
        correctos = cm[i, i]
        incorrectos = total - correctos
        if incorrectos > 0:
            errores_por_clase.append((letra, incorrectos, total))
    
    errores_por_clase.sort(key=lambda x: x[1], reverse=True)
    for letra, incorrectos, total in errores_por_clase[:10]:
        print(f"   • '{letra}': {incorrectos}/{total} errores ({incorrectos/total*100:.1f}%)")
else:
    print("\n✓ ¡Clasificación perfecta en el conjunto de prueba!")

print("\n" + "="*70)
print("Evaluación completada. Mejor modelo identificado.")
print("="*70)

# Guardar información para el siguiente script
import pickle

# Guardar el mejor modelo
with open('mejor_modelo.pkl', 'wb') as f:
    pickle.dump(mejor_modelo_info['modelo'], f)

# Guardar el scaler y label encoder
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)

# Guardar info del mejor modelo
with open('info_mejor_modelo.txt', 'w', encoding='utf-8') as f:
    f.write(f"Mejor Modelo: {mejor_modelo_nombre}\n")
    f.write(f"Test Accuracy: {mejor_modelo_info['test_accuracy']:.4f}\n")
    f.write(f"CV Mean: {mejor_modelo_info['cv_mean']:.4f}\n")
    f.write(f"CV Std: {mejor_modelo_info['cv_std']:.4f}\n")

print("\n✓ Archivos guardados:")
print("   • mejor_modelo.pkl")
print("   • scaler.pkl")
print("   • label_encoder.pkl")
print("   • info_mejor_modelo.txt")
