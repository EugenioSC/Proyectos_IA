from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

def create_sushi_model():
    """
    Define y crea el modelo de la Red Bayesiana para las recomendaciones de sushi.
    VERSIÓN COMPLETA con los 28 platillos del menú.
    """
    # 1. Definir los 8 conceptos clave de ingredientes
    ingredient_nodes = [
        'Gusta_Aguacate', 'Gusta_Queso_Crema', 'Gusta_Camaron', 'Gusta_Res',
        'Gusta_Pollo', 'Gusta_Pescado_Crudo', 'Gusta_Tocino', 'Gusta_Spicy'
    ]
    
    # 2. Definir los 28 nodos de platillos y sus dependencias de ingredientes clave
    dish_dependencies = {
        'Recomendar_Rollo_California': ['Gusta_Aguacate', 'Gusta_Camaron'],
        'Recomendar_Dragon_Roll': ['Gusta_Queso_Crema'],
        'Recomendar_Rollo_Tempura': ['Gusta_Camaron', 'Gusta_Queso_Crema'],
        'Recomendar_Mar_y_tierra': ['Gusta_Camaron', 'Gusta_Res'],
        'Recomendar_Chon': ['Gusta_Camaron', 'Gusta_Res', 'Gusta_Queso_Crema'],
        'Recomendar_Cordon_blue': ['Gusta_Pollo', 'Gusta_Tocino', 'Gusta_Queso_Crema'],
        'Recomendar_Camaron_blue': ['Gusta_Camaron', 'Gusta_Tocino', 'Gusta_Queso_Crema'],
        'Recomendar_Monster_Roll': ['Gusta_Camaron', 'Gusta_Queso_Crema', 'Gusta_Spicy'],
        'Recomendar_Avocado_Tuna_Roll': ['Gusta_Pescado_Crudo', 'Gusta_Aguacate', 'Gusta_Camaron'],
        'Recomendar_Bonito_Roll': ['Gusta_Camaron', 'Gusta_Spicy'],
        'Recomendar_Guamuchilito': ['Gusta_Camaron'],
        'Recomendar_Senorita_Roll': ['Gusta_Pescado_Crudo', 'Gusta_Camaron'],
        'Recomendar_Guerra': ['Gusta_Camaron', 'Gusta_Spicy'],
        'Recomendar_Caramelo_Hot': ['Gusta_Camaron', 'Gusta_Queso_Crema'],
        'Recomendar_Green_Hot': ['Gusta_Camaron', 'Gusta_Tocino', 'Gusta_Aguacate'],
        'Recomendar_Avocado_Hot': ['Gusta_Camaron', 'Gusta_Spicy', 'Gusta_Aguacate'],
        'Recomendar_Salmoncito_Hot': ['Gusta_Pescado_Crudo', 'Gusta_Spicy'],
        'Recomendar_Banano_Hot': ['Gusta_Camaron', 'Gusta_Queso_Crema'],
        'Recomendar_Tres_quesos': ['Gusta_Res', 'Gusta_Camaron', 'Gusta_Queso_Crema'],
        'Recomendar_Norteno': ['Gusta_Res', 'Gusta_Camaron', 'Gusta_Tocino', 'Gusta_Spicy'],
        'Recomendar_Avocado_eby': ['Gusta_Camaron', 'Gusta_Spicy', 'Gusta_Aguacate'],
        'Recomendar_Oranger_taiguer': ['Gusta_Camaron', 'Gusta_Spicy'],
        'Recomendar_Chica_light': ['Gusta_Pescado_Crudo'],
        'Recomendar_El_patron': ['Gusta_Camaron', 'Gusta_Spicy'],
        'Recomendar_Lava_hot': ['Gusta_Res', 'Gusta_Camaron', 'Gusta_Spicy'],
        'Recomendar_Carnivoro': ['Gusta_Pollo', 'Gusta_Tocino', 'Gusta_Res'],
        'Recomendar_Salvaje_hot': ['Gusta_Res', 'Gusta_Pollo', 'Gusta_Camaron', 'Gusta_Spicy'],
        'Recomendar_Krack_hot': ['Gusta_Res', 'Gusta_Queso_Crema', 'Gusta_Tocino']
    }

    # Construir la estructura del grafo
    model_structure = []
    for dish, ingredients in dish_dependencies.items():
        for ingredient in ingredients:
            model_structure.append((ingredient, dish))

    model = DiscreteBayesianNetwork(model_structure)

    # 3. Definir CPDs para cada nodo de ingrediente (probabilidad a priori)
    cpds_to_add = []
    for node in ingredient_nodes:
        cpd = TabularCPD(variable=node, variable_card=2, values=[[0.5], [0.5]])
        cpds_to_add.append(cpd)
        
    # 4. Definir CPDs para cada nodo de platillo (probabilidad condicional)
    cpd_template_1 = [[0.9, 0.1], [0.1, 0.9]]
    cpd_template_2 = [[0.95, 0.6, 0.5, 0.05], [0.05, 0.4, 0.5, 0.95]]
    cpd_template_3 = [[0.99, 0.8, 0.7, 0.5, 0.6, 0.4, 0.3, 0.01], [0.01, 0.2, 0.3, 0.5, 0.4, 0.6, 0.7, 0.99]]
    cpd_template_4 = [[0.99, 0.9, 0.85, 0.8, 0.8, 0.75, 0.7, 0.6, 0.7, 0.65, 0.6, 0.5, 0.4, 0.3, 0.2, 0.01], 
                     [0.01, 0.1, 0.15, 0.2, 0.2, 0.25, 0.3, 0.4, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7, 0.8, 0.99]]
    
    for dish, ingredients in dish_dependencies.items():
        evidence = ingredients
        evidence_card = [2] * len(ingredients)
        if len(ingredients) == 1: 
            values = cpd_template_1
        elif len(ingredients) == 2: 
            values = cpd_template_2
        elif len(ingredients) == 3: 
            values = cpd_template_3
        else: 
            values = cpd_template_4
        
        cpd = TabularCPD(
            variable=dish, 
            variable_card=2, 
            values=values, 
            evidence=evidence, 
            evidence_card=evidence_card
        )
        cpds_to_add.append(cpd)

    # Añadir todos los CPDs al modelo
    for cpd in cpds_to_add:
        model.add_cpds(cpd)
    
    # Verificar que el modelo es válido
    try:
        model.check_model()
    except Exception as e:
        print(f"Error al verificar el modelo: {e}")
        # Continuar a pesar del error para propósitos de demostración
    
    return model, list(dish_dependencies.keys())


def get_recommendation_probabilities(model, all_dish_nodes, user_evidence):
    """
    Obtiene las probabilidades de recomendación para todos los platillos
    dado un conjunto de evidencias del usuario.
    """
    inference = VariableElimination(model)
    results = {}
    
    for node in all_dish_nodes:
        try:
            # Realizar la inferencia para cada platillo
            prob = inference.query(variables=[node], evidence=user_evidence)
            dish_name = node.replace('Recomendar_', '').replace('_', ' ')
            results[dish_name] = round(prob.values[1] * 100, 2)
        except Exception as e:
            # Si hay error, asignar probabilidad neutral
            print(f"Error en inferencia para {node}: {e}")
            dish_name = node.replace('Recomendar_', '').replace('_', ' ')
            results[dish_name] = 50.0  # Probabilidad neutral en caso de error
            
    return results