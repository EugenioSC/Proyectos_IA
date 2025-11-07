## Sistema Experto para Diagnóstico Respiratorio 🩺🧠🫁
Elaborado por: Eugenio Soto Cortez 🧑‍🎓🔬

## Descripción 💻✍️
Este proyecto implementa un **Sistema Experto (SE)** para el **diagnóstico asistido de enfermedades respiratorias**.
Utiliza una **Base de Conocimientos** y un **Motor de Inferencia** para simular el razonamiento de un médico especialista, calculando la probabilidad de un diagnóstico basándose en la evidencia sintomática.

El sistema está desarrollado en **Python** con una arquitectura limpia de 3 capas. Utiliza **Tkinter** para la interfaz gráfica de usuario y un motor de inferencia personalizado. El conocimiento experto se almacena de forma desacoplada en un archivo **JSON**.

El sistema permite:
- Guiar al usuario a través de un cuestionario dinámico (estilo asistente).
- **Calcular el porcentaje de certeza** de un diagnóstico basándose en el **promedio de la evidencia** (pesos de síntomas) encontrada.
- Mostrar un diagnóstico principal, posibilidades secundarias y recomendaciones de cuidado.

---

## Funcionalidades 🛠️🩺
- Motor de Inferencia con **Encadenamiento Hacia Adelante** (Forward Chaining).
- Base de Conocimientos (`reglas.json`) desacoplada que permite editar reglas sin tocar el código.
- Cálculo dinámico de certeza mediante el **promedio de pesos de evidencia** de los síntomas.
- Interfaz Gráfica de Usuario (GUI) con **Tkinter** en modo "asistente" (wizard) para una experiencia amigable.
- Lógica de cuestionario condicional (omite preguntas irrelevantes, ej. "temperatura" si "fiebre" es "no").
- Formato de resultados claro que incluye:
    - Diagnóstico Principal (el de mayor %).
    - Otras Posibilidades (si las hay).
    - Recomendaciones de cuidado.
    - Aviso legal de consultar a un médico.
- Script de validación (`validador.py`) para pruebas de precisión unitarias.

---

## Requisitos 🎯📋
El proyecto no requiere dependencias externas, ya que utiliza únicamente la biblioteca estándar de Python.
- Python 3.x
- Tkinter (normalmente incluido en la instalación estándar de Python)

---

## Ejecución ▶️⚙️
1. Asegúrate de tener los 3 archivos principales en la misma carpeta:
    - `reglas.json` (La base de conocimientos)
    - `sistema_experto.py` (El motor de lógica)
    - `main_wizard.py` (La aplicación gráfica)

2. Inicia la aplicación principal ejecutando:
   ```bash
   python main_wizard.py
   ```

3. (Opcional) Para verificar la lógica del motor, puedes ejecutar el script de validación:
   ```bash
   python validador.py
   ```
