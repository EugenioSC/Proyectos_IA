import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout, BatchNormalization, Activation
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import os

# --- Configuración Inicial ---
path_datos = 'dataset' 
BATCH_SIZE = 32
TARGET_SIZE = (48, 48) # Tamaño estándar para este tipo de redes

# Validación básica para no correr si faltan carpetas
if not os.path.exists(path_datos):
    print("ERROR: No encuentro la carpeta 'dataset'.")
    exit()

# --- Preprocesamiento y Data Augmentation ---
# Creamos variaciones de las imágenes para que el modelo no memorice, sino que aprenda
datagen = ImageDataGenerator(
    rescale=1./255,         # Normalizamos los pixeles de 0-255 a 0-1
    rotation_range=20,      # Rotación leve
    width_shift_range=0.1,
    height_shift_range=0.1, 
    zoom_range=0.1,
    horizontal_flip=True,   # Espejo (importante para caras)
    validation_split=0.2    # Usamos el 20% para validar
)

# Generador para entrenamiento (80% de los datos)
train_generator = datagen.flow_from_directory(
    path_datos, target_size=TARGET_SIZE, batch_size=BATCH_SIZE,
    class_mode='categorical', color_mode='rgb', subset='training', shuffle=True
)

# Generador para validación (20% restante)
validation_generator = datagen.flow_from_directory(
    path_datos, target_size=TARGET_SIZE, batch_size=BATCH_SIZE,
    class_mode='categorical', color_mode='rgb', subset='validation', shuffle=False
)

# Imprimimos esto para verificar qué número asignó a cada emoción
print(f"Diccionario: {train_generator.class_indices}")

# --- Arquitectura de la CNN ---
model = Sequential()

# Bloque 1: Extracción de características básicas
model.add(Conv2D(32, (3, 3), padding='same', input_shape=(48, 48, 3)))
model.add(BatchNormalization()) # Ayuda a estabilizar el aprendizaje
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25)) # Apagamos neuronas para evitar overfitting

# Bloque 2: Rasgos intermedios
model.add(Conv2D(64, (3, 3), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# Bloque 3: Rasgos complejos
model.add(Conv2D(128, (3, 3), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# Clasificación final
model.add(Flatten())
model.add(Dense(512))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.5)) # Dropout agresivo antes de la salida
model.add(Dense(4, activation='softmax')) # 4 neuronas para las 4 emociones

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# --- Callbacks ---
# Checkpoint: Guarda solo si el modelo mejora la precisión en validación
checkpoint = ModelCheckpoint(
    'modelo_rgb_final.h5', 
    monitor='val_accuracy', 
    verbose=1, 
    save_best_only=True, 
    mode='max'
)

# EarlyStopping: Detiene el entrenamiento si no mejora tras 5 épocas
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

print("--- Iniciando entrenamiento ---")
model.fit(
    train_generator,
    epochs=25, 
    validation_data=validation_generator,
    callbacks=[checkpoint, early_stop]
)

print("Entrenamiento finalizado. Modelo guardado.")