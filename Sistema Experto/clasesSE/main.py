import tkinter as tk
from tkinter import ttk, messagebox
from sistema_experto import SistemaExperto 

# --- 1. Definimos las preguntas ---
PREGUNTAS = [
    {'id': 'edad', 'texto': '¿Cuál es la edad del paciente?', 'tipo': 'num'},
    {'id': 'sexo', 'texto': '¿Cuál es el sexo del paciente?', 'tipo': 'opcion', 'opciones': ['Masculino', 'Femenino'], 'valores_json': ['m', 'f']},
    {'id': 'tos', 'texto': '¿El paciente tiene tos?', 'tipo': 'si/no'},
    {'id': 'tos_tipo', 'texto': '¿El tipo de tos es seca o productiva?', 'tipo': 'opcion', 'opciones': ['Seca', 'Productiva'], 'valores_json': ['seca', 'productiva'], 'depende_de': 'tos'},
    {'id': 'tos_duracion_dias', 'texto': '¿Cuántos días ha durado la tos?', 'tipo': 'num', 'depende_de': 'tos'},
    {'id': 'fiebre', 'texto': '¿El paciente tiene fiebre?', 'tipo': 'si/no'},
    {'id': 'fiebre_grados', 'texto': '¿Cuál es su temperatura (°C)?', 'tipo': 'num', 'depende_de': 'fiebre'},
    {'id': 'disnea', 'texto': '¿Tiene disnea (dificultad para respirar)?', 'tipo': 'si/no'},
    {'id': 'sibilancias', 'texto': '¿Tiene sibilancias (silbidos en el pecho)?', 'tipo': 'si/no'},
    {'id': 'fatiga', 'texto': '¿Siente fatiga o cansancio extremo?', 'tipo': 'si/no'},
    {'id': 'anosmia', 'texto': '¿Ha perdido el olfato o el gusto?', 'tipo': 'si/no'},
    {'id': 'dolor_muscular', 'texto': '¿El paciente tiene dolor muscular o corporal general?', 'tipo': 'si/no'},
    {'id': 'dolor_garganta', 'texto': '¿El paciente tiene un dolor de garganta intenso?', 'tipo': 'si/no'},
    {'id': 'ganglios_inflamados', 'texto': '¿Tiene los ganglios del cuello inflamados?', 'tipo': 'si/no'},
    {'id': 'congestion_nasal', 'texto': '¿El paciente tiene congestión o escurrimiento nasal?', 'tipo': 'si/no'},
    {'id': 'dolor_facial', 'texto': '¿Siente dolor o presión en la cara (mejillas, frente)?', 'tipo': 'si/no', 'depende_de': 'congestion_nasal'},
    {'id': 'estornudos', 'texto': '¿El paciente tiene estornudos frecuentes?', 'tipo': 'si/no'},
    {'id': 'picor_ojos', 'texto': '¿El paciente tiene picor o lagrimeo en los ojos?', 'tipo': 'si/no'},
    {'id': 'fumador', 'texto': '¿Tiene antecedentes de tabaquismo?', 'tipo': 'si/no'},
    {'id': 'alergias', 'texto': '¿Tiene antecedentes de alergias?', 'tipo': 'si/no'},
    {'id': 'crepitantes', 'texto': '¿Se escuchan crepitantes en la auscultación?', 'tipo': 'si/no'},
]

# --- 2. La Clase Principal de la Aplicación ---

class AppAsistente(tk.Tk):
    
    def __init__(self, motor, guion_preguntas):
        super().__init__()
        
        self.motor = motor
        self.preguntas = guion_preguntas
        self.datos_paciente = {} 
        self.pregunta_actual_idx = -1 

        self.title("🩺 Asistente de Diagnóstico Respiratorio")
        self.geometry("600x400")
        self.resizable(False, False)
        
        style = ttk.Style(self)
        style.configure("TLabel", font=("Arial", 14))
        style.configure("TButton", font=("Arial", 12))
        style.configure("Title.TLabel", font=("Arial", 18, "bold"))
        style.configure("Si.TButton", font=("Arial", 14, "bold"))
        style.configure("No.TButton", font=("Arial", 14, "bold"))
        style.configure("Opcion.TButton", font=("Arial", 14))

        # --- Frame de Bienvenida ---
        self.frame_bienvenida = ttk.Frame(self, padding=20)
        self.frame_bienvenida.pack(fill="both", expand=True)
        ttk.Label(self.frame_bienvenida, text="Sistema Experto de Diagnóstico", style="Title.TLabel").pack(pady=20)
        ttk.Label(self.frame_bienvenida, 
                  text="Este asistente le hará una serie de preguntas para ayudar\n"
                       "a determinar un posible diagnóstico respiratorio.",
                  justify="center", wraplength=500).pack(pady=15)
        ttk.Button(self.frame_bienvenida, text="Comenzar Evaluación", 
                   command=self.siguiente_pregunta, style="TButton").pack(pady=30, ipady=10, ipadx=20)

        # --- Frame de Preguntas ---
        self.frame_preguntas = ttk.Frame(self, padding=20)
        
        self.label_pregunta = ttk.Label(self.frame_preguntas, text="Texto de la pregunta", style="Title.TLabel", wraplength=550)
        self.label_pregunta.pack(pady=30)
        
        self.respuesta_var_str = tk.StringVar()
        self.respuesta_var_num_str = tk.StringVar() 

        # --- WIDGETS PARA PREGUNTAS TIPO 'num' ---
        self.widget_frame_num = ttk.Frame(self.frame_preguntas)
        self.widget_entry_num = ttk.Entry(self.widget_frame_num, textvariable=self.respuesta_var_num_str, font=("Arial", 14), width=10, justify="center")
        self.widget_entry_num.pack(pady=10)
        
        self.boton_siguiente = ttk.Button(self.frame_preguntas, text="Siguiente", command=self.siguiente_pregunta, style="TButton")
        
        # --- FRAME PARA BOTONES 'si/no' ---
        self.frame_sino_botones = ttk.Frame(self.frame_preguntas)
        self.boton_si = ttk.Button(self.frame_sino_botones, text="Sí", 
                                   command=lambda: self._responder_sino('si'), 
                                   style="Si.TButton")
        self.boton_si.pack(side=tk.LEFT, padx=20, ipady=10, ipadx=40)
        self.boton_no = ttk.Button(self.frame_sino_botones, text="No", 
                                   command=lambda: self._responder_sino('no'), 
                                   style="No.TButton")
        self.boton_no.pack(side=tk.LEFT, padx=20, ipady=10, ipadx=40)
        
        # --- FRAME PARA BOTONES DE 'opcion' ---
        self.frame_opciones_botones = ttk.Frame(self.frame_preguntas)

    def _responder_sino(self, respuesta):
        self.respuesta_var_str.set(respuesta)
        self.siguiente_pregunta()

    def _responder_opcion(self, respuesta_json):
        self.respuesta_var_str.set(respuesta_json)
        self.siguiente_pregunta()

    def siguiente_pregunta(self):
        if self.pregunta_actual_idx >= 0:
            pregunta_cfg = self.preguntas[self.pregunta_actual_idx]
            id_pregunta = pregunta_cfg['id']
            tipo = pregunta_cfg['tipo']
            
            try:
                if tipo == 'num':
                    valor_str = self.respuesta_var_num_str.get()
                    if not valor_str:
                         messagebox.showerror("Error", "El valor numérico no puede estar vacío.")
                         return
                    self.datos_paciente[id_pregunta] = float(valor_str)
                elif tipo == 'opcion' or tipo == 'si/no':
                    self.datos_paciente[id_pregunta] = self.respuesta_var_str.get()
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese un número válido (ej. 38.5 o 40).")
                return

        self.pregunta_actual_idx += 1
        
        while self.pregunta_actual_idx < len(self.preguntas):
            pregunta_cfg = self.preguntas[self.pregunta_actual_idx]
            
            if 'depende_de' in pregunta_cfg:
                id_dependencia = pregunta_cfg['depende_de']
                if self.datos_paciente.get(id_dependencia) != 'si':
                    self.pregunta_actual_idx += 1
                    continue
            break 

        if self.pregunta_actual_idx < len(self.preguntas):
            self.mostrar_pregunta_actual()
        else:
            self.terminar_diagnostico()

    def mostrar_pregunta_actual(self):
        self.frame_bienvenida.pack_forget()
        self.frame_preguntas.pack(fill="both", expand=True)
        
        self.widget_frame_num.pack_forget()
        self.boton_siguiente.pack_forget()
        self.frame_sino_botones.pack_forget()
        self.frame_opciones_botones.pack_forget()
        
        for widget in self.frame_opciones_botones.winfo_children():
            widget.destroy()
        
        pregunta_cfg = self.preguntas[self.pregunta_actual_idx]
        self.label_pregunta.config(text=pregunta_cfg['texto'])
        
        if pregunta_cfg['tipo'] == 'num':
            self.respuesta_var_num_str.set("") 
            self.widget_frame_num.pack(pady=20)
            self.boton_siguiente.pack(pady=40, ipady=5, ipadx=15)
            self.widget_entry_num.focus_set() 
        
        elif pregunta_cfg['tipo'] == 'si/no':
            self.frame_sino_botones.pack(pady=40)
        
        elif pregunta_cfg['tipo'] == 'opcion':
            opciones_texto = pregunta_cfg['opciones']
            opciones_json = pregunta_cfg['valores_json']
            
            for i in range(len(opciones_texto)):
                texto_btn = opciones_texto[i]
                valor_json = opciones_json[i]
                boton = ttk.Button(self.frame_opciones_botones, 
                                   text=texto_btn, 
                                   style="Opcion.TButton",
                                   command=lambda v=valor_json: self._responder_opcion(v))
                boton.pack(side=tk.LEFT, padx=10, ipady=10, ipadx=20)
                
            self.frame_opciones_botones.pack(pady=40)
            
        if self.pregunta_actual_idx == len(self.preguntas) - 1:
            self.boton_siguiente.config(text="Diagnosticar")
        else:
            self.boton_siguiente.config(text="Siguiente")

    # --- INICIO DE LA MODIFICACIÓN ---
    def terminar_diagnostico(self):
        lista_resultados = self.motor.diagnosticar(self.datos_paciente)
        
        titulo = ""
        mensaje_partes = []
        
        # Definir el mensaje de advertencia
        advertencia = "\n\n--- ⚠️ Aviso Importante ---\n" \
                      "Este es un sistema de ayuda basado en IA y no reemplaza un diagnóstico médico definitivo.\n\n" \
                      "**Consulte siempre a un profesional de la salud.**"

        # --- CASO 1: No se encontró ningún diagnóstico ---
        if not lista_resultados:
            titulo = "Diagnóstico No Concluyente"
            mensaje_partes.append("No se activó ninguna regla diagnóstica con los datos proporcionados.")
        
        # --- CASO 2: Se encontraron uno o más diagnósticos ---
        else:
            ganador = lista_resultados[0]
            titulo = f"Diagnóstico: {ganador['diagnostico']} ({ganador['fc'] * 100:.0f}%)"
            
            # 1. El diagnóstico principal
            mensaje_partes.append("--- Diagnóstico Principal ---")
            mensaje_partes.append(f"**{ganador['diagnostico']}** (Certeza: {ganador['fc'] * 100:.0f}%)")
            mensaje_partes.append(f"Justificación: {ganador['explicacion']}")
            mensaje_partes.append(f"**Recomendación:** {ganador['recomendacion']}") 
            
            # 2. Otros diagnósticos
            if len(lista_resultados) > 1:
                mensaje_partes.append("\n--- Otras Posibilidades Consideradas ---")
                for otro_diag in lista_resultados[1:]:
                    mensaje_partes.append(f"**{otro_diag['diagnostico']}** (Certeza: {otro_diag['fc'] * 100:.0f}%)")
                    mensaje_partes.append(f"Justificación: {otro_diag['explicacion']}")
                    mensaje_partes.append(f"**Recomendación:** {otro_diag['recomendacion']}") 

        # --- AÑADIR LA ADVERTENCIA AL FINAL DE CUALQUIER MENSAJE ---
        mensaje_final = "\n".join(mensaje_partes) + advertencia

        messagebox.showinfo(titulo, mensaje_final)
        
        # Reiniciar el asistente
        self.datos_paciente = {}
        self.pregunta_actual_idx = -1
        self.frame_preguntas.pack_forget()
        self.frame_bienvenida.pack(fill="both", expand=True)
    # --- FIN DE LA MODIFICACIÓN ---

# --- 3. PUNTO DE ENTRADA PRINCIPAL ---
if __name__ == "__main__":
    
    ARCHIVO_DE_REGLAS = "reglas.json"
    motor_experto = SistemaExperto(ARCHIVO_DE_REGLAS)
    app = AppAsistente(motor_experto, PREGUNTAS)
    app.mainloop()