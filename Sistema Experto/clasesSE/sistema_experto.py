import json

class SistemaExperto:
    """
    Capa de Lógica (Backend).
    Implementa un motor de inferencia que CALCULA la certeza
    basándose en el promedio de los pesos de los antecedentes.
    """
    
    def __init__(self, archivo_json_reglas):
        """
        Carga las reglas desde el archivo JSON al inicializar.
        """
        try:
            with open(archivo_json_reglas, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                self.reglas = datos["reglas"]
            print(f"[Backend]: Se cargaron {len(self.reglas)} reglas desde {archivo_json_reglas}")
        except FileNotFoundError:
            print(f"[Backend Error]: No se encontró el archivo {archivo_json_reglas}")
            self.reglas = []
        except json.JSONDecodeError:
            print(f"[Backend Error]: El archivo {archivo_json_reglas} no es un JSON válido.")
            self.reglas = []

    def diagnosticar(self, datos_paciente):
        """
        Aplica encadenamiento hacia adelante.
        Calcula la certeza como el promedio de los pesos de los antecedentes.
        
        RETORNA: Una LISTA de diagnósticos ordenados del más alto al más bajo.
        """
        if not self.reglas:
             return [] 

        diagnosticos_encontrados = []
        
        # Iterar sobre cada regla en la Base de Conocimientos
        for regla in self.reglas:
            se_cumple_regla = True
            pesos_de_evidencia = [] # Lista para guardar los pesos de esta regla

            # Iterar sobre cada condición (antecedente) de la regla
            for condicion in regla["antecedents"]:
                # Extraer los 4 componentes de la nueva estructura
                hecho = condicion[0]
                operador = condicion[1]
                valor_regla = condicion[2]
                peso = condicion[3] # El peso de este síntoma (ej. 0.9)
                
                # --- 1. Verificar si el síntoma está en los datos del paciente ---
                if hecho not in datos_paciente:
                    se_cumple_regla = False
                    break 
                
                valor_paciente = datos_paciente[hecho]
                
                # --- 2. Comparar el valor del paciente con el de la regla ---
                try:
                    if operador == "==" and not (valor_paciente == valor_regla): se_cumple_regla = False; break
                    elif operador == ">" and not (valor_paciente > valor_regla): se_cumple_regla = False; break
                    elif operador == "<" and not (valor_paciente < valor_regla): se_cumple_regla = False; break
                    elif operador == ">=" and not (valor_paciente >= valor_regla): se_cumple_regla = False; break
                    elif operador == "<=" and not (valor_paciente <= valor_regla): se_cumple_regla = False; break
                    elif operador == "!=" and not (valor_paciente != valor_regla): se_cumple_regla = False; break
                except (TypeError, ValueError):
                    se_cumple_regla = False
                    break

                # --- 3. Si la condición se cumple, guardar su peso ---
                pesos_de_evidencia.append(peso)

            # --- 4. Si la regla se activó (TODAS las condiciones fueron True) ---
            if se_cumple_regla and pesos_de_evidencia:
                
                # --- AQUÍ ESTÁ LA LÓGICA DEL CÁLCULO ---
                certeza_calculada = sum(pesos_de_evidencia) / len(pesos_de_evidencia)
                # ----------------------------------------
                
                diagnosticos_encontrados.append({
                    "diagnostico": regla["conclusion"],
                    "fc": certeza_calculada,
                    "explicacion": f"({regla['id']}): {regla['explicacion']}",
                    "recomendacion": regla["recomendacion"] 
                })

        # --- 5. Ordenar los resultados ---
        if not diagnosticos_encontrados:
            return [] # Retorna lista vacía

        diagnosticos_ordenados = sorted(diagnosticos_encontrados, key=lambda x: x['fc'], reverse=True)
        
        return diagnosticos_ordenados