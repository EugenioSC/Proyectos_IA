# Sistema de Detección de Emociones Faciales (CNN) 📸🧠😊
**Elaborado por:** Jesús Eugenio Soto Cortéz 🧑‍💻🎓

## 🔗 Enlaces del Proyecto (Descargas)
Aquí puedes encontrar los recursos completos del proyecto:

- 🎥 **Video Demostrativo:** [Ver Video en Google Drive](https://drive.google.com/file/d/1sCF24CGsE5-Uob3b0C95O7FqBBW8499Q/view?usp=sharing)
- 📦 **Proyecto Completo (Código + Dataset):** [Descargar ZIP completo](https://drive.google.com/file/d/1oGrCecfZr0OR7JZTeO-o4dUVsfdEXJj4/view?usp=sharing)

---

## 📝 Descripción
Este proyecto implementa un sistema de **Visión por Computadora** basado en **Deep Learning** para la detección y clasificación de emociones faciales en tiempo real.

A diferencia de los detectores genéricos, esta solución utiliza una **Red Neuronal Convolucional (CNN)** personalizada, entrenada "desde cero" con un dataset **RGB balanceado (~9,200 imágenes)**. El sistema integra una capa de **Lógica de Inferencia** diseñada para funcionar en entornos reales ("in-the-wild"), superando desafíos como la iluminación variable y oclusiones faciales (por ejemplo, el uso de ortodoncia).

### El sistema permite:
- **Detectar rostros** en flujo de video en vivo.
- **Preprocesar la imagen** automáticamente (Ecualización de Histograma) para mejorar el contraste.
- Clasificar 4 estados: **Felicidad, Enojo, Tristeza y Neutralidad**.
- Aplicar **umbrales de sensibilidad asimétricos** para detectar micro-expresiones de enojo y tristeza que suelen ser ignoradas por modelos estándar.

---

## 🛠️ Requisitos e Instalación
Para ejecutar este proyecto necesitas **Python 3.x** y las siguientes librerías.

### Librerías necesarias:
* **TensorFlow / Keras:** Para la carga y ejecución del modelo neuronal.
* **OpenCV (`opencv-python`):** Para el acceso a la cámara y procesamiento de imágenes.
* **NumPy:** Para manipulación de matrices numéricas.
* **Matplotlib & Seaborn:** Para generar las gráficas de validación y matrices de confusión.
* **Scikit-learn:** Para métricas de evaluación.

### ⚡ Comando de Instalación Rápida
Abre tu terminal en la carpeta del proyecto y ejecuta:

```bash
pip install tensorflow opencv-python numpy matplotlib seaborn scikit-learn
