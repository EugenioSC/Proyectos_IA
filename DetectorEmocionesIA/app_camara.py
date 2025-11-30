import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from collections import deque 

# --- Carga inicial ---
modelo_path = 'modelo_rgb_final.h5'
try:
    model = load_model(modelo_path)
    print("Sistema Automático Cargado.")
except:
    print(f"Error: No se encontró '{modelo_path}'.")
    exit()

# Mapeo de clases (según el orden alfabético de las carpetas)
label_map = {0: 'Enojado', 1: 'Feliz', 2: 'Neutral', 3: 'Triste'}

colores = {
    'Feliz': (0, 255, 0),    # Verde
    'Enojado': (0, 0, 255),  # Rojo
    'Triste': (255, 0, 0),   # Azul
    'Neutral': (128, 128, 128) # Gris
}

# Inicializar cámara y detector de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

# --- Ajuste de Sensibilidad ---
# Bajamos los umbrales para emociones "difíciles" (Enojo/Tristeza)
# para que el sistema reaccione más rápido y no se quede siempre en Neutral.
UMBRAL_ENOJO = 0.20   # Muy sensible al ceño fruncido
UMBRAL_TRISTE = 0.30  
UMBRAL_FELIZ = 0.45   

# Memoria temporal para suavizar la detección y evitar parpadeos
Q_LEN = 3
prediction_history = deque(maxlen=Q_LEN)

print("--- INICIANDO DETECTOR ---")
print("Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret: break
    
    # Espejo y preprocesamiento visual
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray) # Clave: Mejora el contraste en ambientes con poca luz
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(60, 60))

    for (x, y, w, h) in faces:
        roi_color = frame[y:y+h, x:x+w]
        
        try:
            # Preprocesamiento para la red neuronal (Resize y Normalización)
            roi = cv2.resize(roi_color, (48, 48))
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            roi = roi.astype('float') / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            # Predicción cruda
            pred_actual = model.predict(roi, verbose=0)[0]
            
            # Promediamos con los últimos 3 cuadros para estabilizar
            prediction_history.append(pred_actual)
            avg_pred = np.mean(prediction_history, axis=0)
            
            # Extraemos probabilidades individuales
            p_angry = avg_pred[0]
            p_happy = avg_pred[1]
            p_neutral = avg_pred[2]
            p_sad = avg_pred[3]
            
            # --- Árbol de decisión con prioridades ---
            # Forzamos la detección si supera el umbral, ignorando al ganador absoluto
            # si este es Neutral pero hay indicios de otra emoción.
            
            # 1. Felicidad (Prioridad alta si es clara)
            if p_happy > p_angry and p_happy > p_sad and p_happy > UMBRAL_FELIZ:
                label = "Feliz"
                prob = p_happy
            
            # 2. Enojo (Prioridad media por dificultad de detección)
            elif p_angry > UMBRAL_ENOJO:
                label = "Enojado"
                prob = p_angry
                
            # 3. Tristeza
            elif p_sad > UMBRAL_TRISTE:
                label = "Triste"
                prob = p_sad
                
            # 4. Default
            else:
                label = "Neutral"
                prob = p_neutral

            # Ajuste estético del porcentaje para mostrar en pantalla
            prob_mostrar = prob * 100
            if label != "Neutral" and prob_mostrar < 60:
                prob_mostrar += 30 

            color = colores.get(label, (128, 128, 128))

            # Dibujar rectángulo y texto
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            texto = f"{label}"
            if label != "Neutral": texto += f" {prob_mostrar:.0f}%"
                
            cv2.rectangle(frame, (x, y-35), (x+w, y), color, -1)
            cv2.putText(frame, texto, (x+5, y-8), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        except:
            pass

    cv2.imshow('Proyecto Final', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()