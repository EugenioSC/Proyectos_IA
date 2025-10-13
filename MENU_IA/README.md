## Sistema de Recomendación de Sushi con Modelo Probabilístico 🍣🧠  
Elaborado por: Eugenio Soto Cortez y Jose Enrique Espíndola Leyva 😼🏆  

## Descripción 💻✍️  
Este proyecto implementa un **sistema inteligente de recomendación en la industria restaurantera**, especializado en **platillos de sushi**.  
Utiliza una **Red Bayesiana** (modelo probabilístico) para predecir qué platillos podrían gustarle a cada usuario según sus preferencias de ingredientes.  

El sistema está desarrollado con **FastAPI** y una base de datos **SQLite**, integrando un modelo de inferencia probabilística creado con **pgmpy**.  

El sistema permite:  
- Calcular recomendaciones personalizadas según gustos individuales.  
- Aprender automáticamente de las calificaciones que los usuarios asignan a los ingredientes.  
- Visualizar la probabilidad de recomendación de cada platillo.  

---

## Funcionalidades 🛠️🍱  
- Cálculo de recomendaciones usando inferencia probabilística con **pgmpy**.  
- API REST construida con **FastAPI** para interactuar con el modelo.  
- Base de datos relacional en **SQLite** con tablas para usuarios, ingredientes y preferencias.  
- Conversión automática de puntuaciones (1–5) en evidencia binaria (gusta/no gusta).  
- Generación ordenada de platillos recomendados según su probabilidad estimada.  
- Validación automática de consistencia del modelo antes de ejecutar inferencias.  

---

## Requisitos 🎯🔏  
Vienen incluidos en el documento **“Tutorial de dependencias”**, donde se explica paso a paso cómo instalar:  
- Python 3.10 o superior  
- FastAPI  
- Uvicorn  
- pgmpy  
- SQLite3  

---

## Ejecución ▶️⚙️  
1. Ejecuta el archivo `database.py` para crear la base de datos y cargar los datos iniciales.  
2. Inicia el servidor de la API con:  
   ```bash
   uvicorn main:app --reload
