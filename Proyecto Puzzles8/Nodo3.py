import numpy as np
import heapq
from pprint import pprint

class Nodo:
    def __init__(self, matriz, heuristica=None, costo_acumulado=0, padre=None):
        self.matriz = matriz
        self.heuristica = heuristica  # h(n): costo estimado desde este nodo al objetivo
        self.costo_acumulado = costo_acumulado  # g(n): costo desde el inicio hasta este nodo
        # f(n) = g(n) + h(n): costo total estimado
        self.f = self.costo_acumulado + self.heuristica if self.heuristica is not None else float('inf')
        self.hijos = []
        self.padre = padre

    def agregarHijo(self, hijo_matriz, heuristica, costo_acumulado):
        nuevo_hijo = Nodo(hijo_matriz, heuristica, costo_acumulado, self)
        self.hijos.append(nuevo_hijo)
        return nuevo_hijo
        
    def __lt__(self, other):
        return self.f < other.f

def heuristica_manhattan(estado, objetivo):
    distancia = 0
    for valor in range(1, 9):  # Itera sobre las fichas del 1 al 8
        pos_actual = np.argwhere(estado == valor)[0]
        pos_objetivo = np.argwhere(objetivo == valor)[0]
        distancia += abs(pos_actual[0] - pos_objetivo[0]) + abs(pos_actual[1] - pos_objetivo[1])
    return distancia

def Intercambiar(matriz, row1, col1, row2, col2): 
    nueva_matriz = matriz.copy()
    nueva_matriz[row1, col1], nueva_matriz[row2, col2] = nueva_matriz[row2, col2], nueva_matriz[row1, col1]
    return nueva_matriz

def a_estrella(inicio, objetivo):
    lista_abierta = []  # Cola de prioridad con los nodos por explorar
    lista_cerrada = set() # Conjunto de estados ya expandidos
    
    # Nodo inicial
    h_inicio = heuristica_manhattan(inicio, objetivo)
    nodo_inicial = Nodo(inicio, h_inicio, 0)
    heapq.heappush(lista_abierta, nodo_inicial)
    
    # Diccionario para rastrear el menor costo g para cada estado en la lista abierta
    costo_g_abierta = {tuple(map(tuple, inicio)): 0}
    
    while lista_abierta:
        # Obtener el nodo con el menor valor f de la lista abierta
        nodo_actual = heapq.heappop(lista_abierta)
        
        # Si es el objetivo, hemos terminado
        if np.array_equal(nodo_actual.matriz, objetivo):
            return nodo_actual # ¡Solución encontrada!
        
        # Mover el nodo actual a la lista cerrada
        estado_actual_tupla = tuple(map(tuple, nodo_actual.matriz))
        lista_cerrada.add(estado_actual_tupla)
        
        # Generar los sucesores (movimientos válidos)
        fila, col = np.argwhere(nodo_actual.matriz == 0)[0]
        movimientos = []
        if fila > 0: movimientos.append((fila - 1, col)) # Arriba
        if fila < 2: movimientos.append((fila + 1, col)) # Abajo
        if col > 0: movimientos.append((fila, col - 1)) # Izquierda
        if col < 2: movimientos.append((fila, col + 1)) # Derecha
        
        for nueva_fila, nueva_col in movimientos:
            nueva_matriz = Intercambiar(nodo_actual.matriz, fila, col, nueva_fila, nueva_col)
            nueva_matriz_tupla = tuple(map(tuple, nueva_matriz))
            
            # Si el sucesor ya está en la lista cerrada, lo ignoramos
            if nueva_matriz_tupla in lista_cerrada:
                continue
                
            # Calcular costos para el sucesor
            h = heuristica_manhattan(nueva_matriz, objetivo)
            g = nodo_actual.costo_acumulado + 1
            
            # Si el sucesor ya está en la lista abierta con un costo g menor o igual, lo ignoramos
            if nueva_matriz_tupla in costo_g_abierta and g >= costo_g_abierta[nueva_matriz_tupla]:
                continue
            
            # Agregar el sucesor a la lista abierta
            nodo_hijo = nodo_actual.agregarHijo(nueva_matriz, h, g)
            heapq.heappush(lista_abierta, nodo_hijo)
            costo_g_abierta[nueva_matriz_tupla] = g # Actualizamos el costo mínimo conocido

    return None # No se encontró solución

# Ejecución del Algoritmo

# Configuración inicial
matriz_inicial = np.array([
    [0, 6, 3],
    [2, 5, 4],
    [7, 1, 8]
])

matriz_objetivo = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
])

# Ejecutar A*
solucion = a_estrella(matriz_inicial, matriz_objetivo)

