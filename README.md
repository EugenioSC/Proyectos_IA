# Repositorio de Proyectos - Inteligencia Artificial 🤖👽

## Descripción ✍️💻
Este repositorio contiene la implementación de proyectos desarrollados para la materia de **Inteligencia Artificial** (Horario: 9:00 a 10:00) en el **Instituto Tecnológico de Culiacán**.

Actualmente incluye:

---

### 1. Puzzle 8 con Algoritmo A* 🧩🎱
- Implementación del **algoritmo de búsqueda A\*** para resolver el juego del Puzzle 8.
- Cuenta con una **interfaz gráfica de usuario (GUI)** desarrollada con **Tkinter**, que permite a los usuarios:
  - Visualizar el proceso de solución paso a paso.
  - Establecer estados iniciales y objetivos personalizados.
  - Generar puzzles aleatorios.

---

### 2. Sistema de Recomendación de Sushi con Modelo Probabilístico 🍣🧠
- Implementación de un **sistema inteligente de recomendación** basado en **redes Bayesianas**, especializado en sugerir platillos de sushi según las preferencias de los usuarios.
- Desarrollado con **FastAPI**, **SQLite** y la librería **pgmpy** para el modelado probabilístico.
- Permite:
  - Calcular recomendaciones personalizadas a partir de gustos individuales.
  - Visualizar probabilidades de recomendación.
  - Aprender de las calificaciones dadas por los usuarios a los ingredientes.

---

### 3. Sistema Experto de Diagnóstico Respiratorio 🩺🧠🫁
- Implementación de un **Sistema Experto (SE)** basado en **reglas de producción**, diseñado para asistir en el diagnóstico de 9 enfermedades respiratorias.
- Desarrollado en **Python** con una arquitectura de 3 capas (Datos, Lógica, Presentación) y una **GUI** con **Tkinter**.
- Utiliza un motor de inferencia personalizado que **calcula dinámicamente el porcentaje de certeza** basándose en el promedio de los "pesos de evidencia" de los síntomas.
- Permite:
  - Guiar al usuario con un asistente "wizard" que omite preguntas irrelevantes.
  - Mostrar un diagnóstico principal, posibilidades secundarias y recomendaciones.
  - Almacenar el conocimiento (reglas, síntomas, pesos) en un archivo **JSON** desacoplado para fácil mantenimiento.

---

### 4. Sistema de Detección de Emociones Faciales 📸😊😡
- Implementación de un sistema de **Visión por Computadora** basado en **Deep Learning** para detectar y clasificar 4 estados emocionales en tiempo real: Felicidad, Enojo, Tristeza y Neutralidad.
- Desarrollado en **Python** utilizando **TensorFlow/Keras** para la red neuronal y **OpenCV** para el procesamiento de imagen.
- Utiliza una **Red Neuronal Convolucional (CNN)** personalizada entrenada desde cero con un dataset **RGB balanceado (~9,200 imágenes)** para mayor robustez en entornos reales.
- Características principales:
  - **Preprocesamiento inteligente:** Aplica ecualización de histograma para normalizar la iluminación.
  - **Lógica de inferencia avanzada:** Implementa umbrales de sensibilidad asimétricos para detectar micro-expresiones sutiles (como el enojo) y un filtro de estabilidad para evitar el parpadeo de etiquetas.
  - Precisión de validación superior al **87.5%**.

---

### Autor 👨‍💻🏆
- **Eugenio Soto Cortez**

Instituto Tecnológico de Culiacán 🏫  
Materia: **Inteligencia Artificial** (Horario: 9:00 - 10:00)  
Profesor: Zuriel Dathan Mora Felix
