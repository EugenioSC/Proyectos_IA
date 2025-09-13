import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import numpy as np
from Nodo3 import a_estrella, matriz_objetivo, matriz_inicial
from Tablero import Tablero


class App(tk.Tk):  
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)  
        self.geometry('800x800')
        self.container = tk.Frame(self, bg='red')
        self.container.place(relx=0, rely=0, relheight=1, relwidth=1)
        fTab = Frame_Tablero(self.container, self)
        fTab.tkraise()

class Ficha:
    contador = 0
    def __init__(self, r, c, n, frame):
        self.frame = frame
        self.r = r
        self.c = c
        self.n = n
        self.contador = Ficha.contador
        Ficha.contador += 1
        if n != 0:
            self.button = tk.Button(self.frame, text=str(self.n), font=("Impact", 100), 
                                command=lambda: frame.move(self.contador, self.r, self.c))  
        else:
            self.button = tk.Button(self.frame, text='', font=("Impact", 100), 
                                command=lambda: frame.move(self.contador, self.r, self.c))  
        self.button.place(relx=1/26+self.c*(4/13), rely=0.05+self.r*(1/4), relheight=1/4, relwidth=4/13)

class Frame_Tablero(tk.Frame):
    def __init__(self, parent, root):
        self.root = root
        tk.Frame.__init__(self, parent, bg='blue')
        self.place(relx=0, rely=0, relheight=1, relwidth=1)

        # Botón Resolver
        self.b_solve = tk.Button(self, text="Resolver", command=lambda: self.solve(), 
                            background='red', fg='white')
        self.b_solve.place(relx=0.3, rely=0.85, relheight=0.08, relwidth=0.4)

        # Botón Editar Inicial
        self.b_edit = tk.Button(self, text="Editar Inicial", command=lambda: self.modo_edicion("inicial"),
                           background='blue', fg='white')
        self.b_edit.place(relx=0.05, rely=0.90, relheight=0.05, relwidth=0.2)

        # Botón Aleatorio Inicial
        self.b_rand = tk.Button(self, text="Aleatorio Inicial", command=self.generar_aleatorio,
                           background='green', fg='white')
        self.b_rand.place(relx=0.05, rely=0.82, relheight=0.05, relwidth=0.2)

        # Botón Editar Objetivo
        self.b_goal = tk.Button(self, text="Editar Objetivo", command=lambda: self.modo_edicion("objetivo"),
                           background='purple', fg='white')
        self.b_goal.place(relx=0.75, rely=0.85, relheight=0.08, relwidth=0.2)

        # Estado inicial
        self.nums = matriz_inicial.tolist()
        self.aux_tablero = Tablero(self.nums)

        # Estado objetivo por defecto (ordenado)
        self.objetivo = [[1,2,3],[4,5,6],[7,8,0]]

        # Fichas
        self.fichas = []
        for ir, r in enumerate(self.nums): 
            for ic, c in enumerate(r):
                aux = Ficha(ir, ic, c, self)
                self.fichas.append(aux)

        self.modo = "normal"  
        self.seleccion = None
    
    def set_botones_estado(self, estado):
        if estado == "hidden":
            self.b_solve.place_forget()
            self.b_edit.place_forget()
            self.b_rand.place_forget()
            self.b_goal.place_forget()
        else:  # estado == "visible"
            self.b_solve.place(relx=0.3, rely=0.85, relheight=0.08, relwidth=0.4)
            self.b_edit.place(relx=0.05, rely=0.90, relheight=0.05, relwidth=0.2)
            self.b_rand.place(relx=0.05, rely=0.82, relheight=0.05, relwidth=0.2)
            self.b_goal.place(relx=0.75, rely=0.85, relheight=0.08, relwidth=0.2)
    
    def generar_aleatorio(self):
        lista = [i for i in range(9)]
        random.shuffle(lista)
        # Convertimos la lista en matriz 3x3
        self.nums = [lista[i:i+3] for i in range(0, 9, 3)]
        self.aux_tablero.nums = self.nums
        self.actualizar(self.nums)

    def modo_edicion(self, tipo):
        if tipo == "inicial":
            self.modo = "edicion_inicial"
            messagebox.showinfo("Modo edición", "Configura el estado INICIAL seleccionando casillas para intercambiar.")
        elif tipo == "objetivo":
            self.modo = "edicion_objetivo"
            self.actualizar(self.objetivo)
            messagebox.showinfo("Modo edición", "Configura el estado OBJETIVO seleccionando casillas para intercambiar.")
        self.seleccion = None

    def move(self, icontador, fr, fc):
        if self.modo in ["edicion_inicial", "edicion_objetivo"]:
            if self.seleccion is None:
                self.seleccion = (fr, fc)
                self.fichas[fr*3 + fc].button.config(bg="yellow")
            else:
                r1, c1 = self.seleccion
                if self.modo == "edicion_inicial":
                    self.nums[r1][c1], self.nums[fr][fc] = self.nums[fr][fc], self.nums[r1][c1]
                    self.aux_tablero.nums = self.nums
                    self.actualizar(self.nums)
                elif self.modo == "edicion_objetivo":
                    self.objetivo[r1][c1], self.objetivo[fr][fc] = self.objetivo[fr][fc], self.objetivo[r1][c1]
                    self.actualizar(self.objetivo)

                self.fichas[r1*3 + c1].button.config(bg="black")
                self.seleccion = None

    def solve(self):
        # Ocultar botones de control
        self.set_botones_estado("hidden")

        estado_inicial = np.array(self.nums)
        estado_objetivo = np.array(self.objetivo)

        solucion = a_estrella(estado_inicial, estado_objetivo)

        if not solucion:
            messagebox.showerror("Sin solución", "NO se encontró solución con este estado y objetivo.")
            self.set_botones_estado("visible")
            return

        # Reconstruir camino
        self.camino = []
        nodo_actual = solucion
        while nodo_actual:
            self.camino.append(nodo_actual.matriz.tolist())
            nodo_actual = nodo_actual.padre
        self.camino.reverse()

        # Iniciar animación
        self.animar_solucion(0)

    def animar_solucion(self, paso):
        if paso < len(self.camino):
            self.actualizar(self.camino[paso])
            self.after(500, lambda: self.animar_solucion(paso + 1))
        else:
            movimientos = len(self.camino) - 1
            messagebox.showinfo("¡Éxito!", f" ¡Se alcanzó el objetivo!\nCantidad de movimientos: {movimientos}")
            # Mostrar botones de nuevo
            self.set_botones_estado("visible")

    def actualizar(self, nums):
        aux = 0
        for ir, r in enumerate(nums):
            for ic, c in enumerate(r):
                if c != 0:
                    self.fichas[aux].button.config(text=str(c), background='orange', 
                                                   fg='blue', borderwidth=10, relief='raised')
                else:
                    self.fichas[aux].button.config(text='', background='white', 
                                                   bd=5, highlightcolor="white", borderwidth=5)
                aux += 1

if __name__ == "__main__":
    app = App()
    app.title("Puzzle 8 con IA A*")
    app.mainloop()
