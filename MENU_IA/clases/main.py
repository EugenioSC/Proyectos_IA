import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

# Importar el módulo de modelo probabilístico
import probabilistic_model

# --- CONFIGURACIÓN ---
DATABASE_FILE = "restaurante.db"
app = FastAPI(
    title="Sistema de Recomendación de Sushi",
    description="Una API para obtener recomendaciones de platillos personalizadas."
)

# Solo montar static si el directorio existe
if os.path.exists("static"):
    from fastapi.staticfiles import StaticFiles
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo Pydantic para la calificación
class Calificacion(BaseModel):
    usuario_id: int
    ingrediente_id: int
    puntuacion: int

# Inicializar el modelo al iniciar la aplicación
try:
    sushi_model, ALL_DISH_NODES = probabilistic_model.create_sushi_model()
    print("Modelo probabilístico cargado correctamente")
except Exception as e:
    print(f"Error al cargar el modelo probabilístico: {e}")
    sushi_model = None
    ALL_DISH_NODES = []

# --- LÓGICA DE BASE DE DATOS ---
def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# --- LÓGICA DEL MODELO DE RECOMENDACIÓN (ACTUALIZADA) ---
def get_probabilistic_recommendations(user_id: int):
    # Si el modelo no se cargó correctamente, retornar None
    if sushi_model is None:
        print("Modelo no disponible")
        return None
        
    conn = get_db_connection()
    prefs_cursor = conn.execute(
        "SELECT i.nombre, pi.puntuacion FROM preferencias_ingredientes pi "
        "JOIN ingredientes i ON pi.ingrediente_id = i.id "
        "WHERE pi.usuario_id = ?",
        (user_id,)
    )
    user_preferences = {row['nombre'].lower(): row['puntuacion'] for row in prefs_cursor.fetchall()}
    conn.close()

    if not user_preferences:
        print(f"No se encontraron preferencias para el usuario {user_id}")
        return None

    evidence = {}
    
    # El "diccionario traductor" de ingredientes a conceptos del modelo
    ingredient_to_concept_map = {
        'Gusta_Aguacate': ['aguacate'],
        'Gusta_Queso_Crema': ['queso crema', 'philadelphia', 'queso americano', 'queso chihuahua', 'queso gouda', 'topping de queso gratinado', 'dedos de queso empanizados'],
        'Gusta_Camaron': ['camarón', 'camarones', 'camarón empanizado', 'camarones empanizados', 'camarones fritos', 'pasta de camarón', 'camarón spicy', 'camarones rellenos philadelphia'],
        'Gusta_Res': ['res', 'res frita'],
        'Gusta_Pollo': ['pollo'],
        'Gusta_Pescado_Crudo': ['atún', 'salmón', 'kanikama osaki', 'kanikama', 'surimi empanizado', 'pulpo'],
        'Gusta_Tocino': ['tocino'],
        'Gusta_Spicy': ['chile caribe', 'chiles', 'chile serrano', 'aderezo miso', 'tampico topping', 'salsa roja', 'green sauce', 'aderezo spicy', 'tampico', 'tampico spicy', 'aderezo volcánico', 'aderezo especial', 'salsa sriracha', 'spicy calamar capeado', 'callo spicy', 'rajitas']
    }

    # Calcular la evidencia para cada concepto promediando las puntuaciones
    for concept_node, keywords in ingredient_to_concept_map.items():
        scores = []
        for keyword in keywords:
            if keyword in user_preferences:
                scores.append(user_preferences[keyword])
        
        if scores:
            avg_score = sum(scores) / len(scores)
            if avg_score >= 4.0:
                evidence[concept_node] = 1  # Le gusta
            elif avg_score <= 2.0:
                evidence[concept_node] = 0  # No le gusta
            # Si está entre 2 y 4, no añadimos evidencia (valor neutral)

    print(f"Evidencia generada para el usuario {user_id}: {evidence}")
    
    try:
        # LA LLAMADA CORRECTA CON TRES ARGUMENTOS
        probabilities = probabilistic_model.get_recommendation_probabilities(
            sushi_model, ALL_DISH_NODES, evidence
        )
        
        recommendations = [
            {"nombre": name.title(), "probabilidad_recomendacion": prob} 
            for name, prob in probabilities.items()
        ]
        sorted_recs = sorted(recommendations, key=lambda x: x['probabilidad_recomendacion'], reverse=True)
        
        return sorted_recs
    except Exception as e:
        print(f"Error en la inferencia probabilística: {e}")
        return None

# --- ENDPOINTS DE LA API ---
@app.get("/")
def read_root():
    return {"message": "Bienvenido al Sistema de Recomendaciones"}

@app.get("/ingredientes")
def get_all_ingredientes():
    conn = get_db_connection()
    ingredientes_cursor = conn.execute("SELECT id, nombre FROM ingredientes ORDER BY nombre ASC")
    ingredientes = [dict(row) for row in ingredientes_cursor.fetchall()]
    conn.close()
    return {"ingredientes": ingredientes}

@app.post("/calificar_ingrediente")
def calificar_ingrediente(calificacion: Calificacion):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT OR REPLACE INTO preferencias_ingredientes (usuario_id, ingrediente_id, puntuacion) VALUES (?, ?, ?)",
            (calificacion.usuario_id, calificacion.ingrediente_id, calificacion.puntuacion)
        )
        conn.commit()
        return {"status": "exito", "message": "Calificación guardada correctamente."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar calificación: {str(e)}")
    finally:
        conn.close()

@app.get("/menu/{user_id}")
def get_full_menu_for_user(user_id: int):
    # Obtener recomendaciones
    recomendados = get_probabilistic_recommendations(user_id)
    if recomendados is None:
        recomendados = []
        print(f"No se pudieron generar recomendaciones para el usuario {user_id}")

    # Obtener menú completo
    conn = get_db_connection()
    try:
        menu_cursor = conn.execute(
            "SELECT p.id, p.nombre, p.descripcion, tp.nombre as tipo_preparacion "
            "FROM platos p JOIN tipos_preparacion tp ON p.tipo_id = tp.id "
            "ORDER BY p.nombre ASC"
        )
        menu_completo_list = [dict(row) for row in menu_cursor.fetchall()]

        # Añadir ingredientes a cada platillo
        for platillo in menu_completo_list:
            ingredientes_cursor = conn.execute(
                "SELECT i.id, i.nombre FROM ingredientes i "
                "JOIN plato_ingredientes pi ON i.id = pi.ingrediente_id "
                "WHERE pi.plato_id = ?",
                (platillo['id'],)
            )
            platillo['ingredientes'] = [dict(row) for row in ingredientes_cursor.fetchall()]

        return {
            "recomendados": recomendados,
            "menu_completo": menu_completo_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener menú: {str(e)}")
    finally:
        conn.close()

@app.get("/health")
def health_check():
    """Endpoint para verificar el estado del servicio y del modelo"""
    model_status = "cargado" if sushi_model is not None else "error"
    return {
        "status": "servicio activo",
        "modelo": model_status,
        "total_platillos": len(ALL_DISH_NODES)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)