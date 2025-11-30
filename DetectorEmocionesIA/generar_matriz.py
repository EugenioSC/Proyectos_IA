import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# --- Parámetros ---
NOMBRE_MODELO = 'modelo_rgb_final.h5' 
RUTA_DATOS = 'dataset'
BATCH_SIZE = 32

# Validaciones de archivos
if not os.path.exists(NOMBRE_MODELO):
    print(f"ERROR: No encuentro el archivo '{NOMBRE_MODELO}'")
    exit()

if not os.path.exists(RUTA_DATOS):
    print(f"ERROR: No encuentro la carpeta '{RUTA_DATOS}'")
    exit()

# Carga del modelo entrenado
print("Cargando modelo...")
model = load_model(NOMBRE_MODELO)

# Preparación de datos de prueba
# Usamos solo rescalado, sin aumentos ni rotaciones para la prueba
test_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2 
)

print("Generando datos para validación...")
test_generator = test_datagen.flow_from_directory(
    RUTA_DATOS,
    target_size=(48, 48),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    color_mode='rgb',
    subset='validation',
    shuffle=False        # OJO: Importante no barajar para que coincidan etiquetas y predicciones
)

# --- Generación de predicciones ---
print("Calculando predicciones...")
Y_pred = model.predict(test_generator, verbose=1)
y_pred = np.argmax(Y_pred, axis=1) # Convertimos probabilidades a etiquetas (0, 1, 2, 3)
y_true = test_generator.classes    # Etiquetas reales

class_labels = list(test_generator.class_indices.keys())

# --- Creación de la Matriz ---
cm = confusion_matrix(y_true, y_pred)

# Graficamos usando Seaborn para el mapa de calor
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=class_labels, 
            yticklabels=class_labels)

plt.title('Matriz de Confusión - RGB')
plt.ylabel('Verdadera Emoción')
plt.xlabel('Predicción del Modelo')
plt.tight_layout()

plt.savefig('matriz_confusion_rgb.png')
print("Imagen guardada correctamente.")

# Métrica detallada en consola
print("\n--- Reporte de Clasificación ---")
print(classification_report(y_true, y_pred, target_names=class_labels))