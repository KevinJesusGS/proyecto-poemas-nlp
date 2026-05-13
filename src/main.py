import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path
import string
from collections import Counter

from src.utils import leer_csv as leer

from src.analysis import (
    analizar_vocabulario_escritor as analizar
)

from src.generation import generar_poemas as generar

from src.generation import (
    generar_poemas_por_topico as generar2
)

from src.generation import (
    generar_poemas_refuerzo as generar3
)

# ============================================================
# CONFIGURACIÓN VISUAL
# ============================================================

COLOR_FONDO = "#2b2b2b"
COLOR_FRAME = "#383838"
COLOR_TEXTO = "#ffffff"
COLOR_ACENTO = "#00adb5"
COLOR_SECUNDARIO = "#393e46"

FUENTE_TITULO = ("Segoe UI", 12, "bold")
FUENTE_TEXTO = ("Segoe UI", 10)

# ============================================================
# DICCIONARIOS
# ============================================================

DICCIONARIO_SENTIMIENTOS = {
    'positivo': [
        "amor", "luz", "sol", "vida", "alegría",
        "cielo", "esperanza", "paz", "beso",
        "flor", "dulce", "suave", "eterno",
        "brillo", "dios", "gloria", "feliz",
        "amar", "corazón", "alma", "bello",
        "hermoso", "sonrisa"
    ],

    'negativo': [
        "muerte", "dolor", "noche", "sombra",
        "llanto", "triste", "frío", "olvido",
        "sangre", "miedo", "vacío", "gris",
        "tumba", "pena", "cruel", "roto",
        "perdido", "fin", "lágrima",
        "oscuridad", "morir", "sufrir"
    ]
}

TOPICOS_CLAVE = {

    'Romántico': [
        "amor", "beso", "pasión", "amada",
        "labios", "querer", "corazón",
        "fuego", "deseo", "caricia",
        "enamorada"
    ],

    'Melancólico': [
        "tristeza", "olvido", "soledad",
        "llanto", "pena", "ayer",
        "recuerdo", "nostalgia",
        "ausencia", "dolor"
    ],

    'Naturaleza': [
        "mar", "árbol", "viento",
        "flor", "río", "montaña",
        "bosque", "pájaro", "tierra",
        "agua", "cielo", "nube",
        "estrella"
    ],

    'Místico/Existencial': [
        "dios", "alma", "muerte",
        "vida", "tiempo", "eternidad",
        "ser", "espíritu", "nada",
        "destino", "sueño"
    ]
}


# ============================================================
# APLICACIÓN
# ============================================================

class AplicacionPoemas:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "AI Poetry Studio - Data Science Project"
        )

        self.root.geometry("1100x850")

        self.root.configure(bg=COLOR_FONDO)

        # ----------------------------------------------------
        # RUTAS
        # ----------------------------------------------------

        BASE_DIR = Path(__file__).resolve().parent.parent

        DATA_DIR = BASE_DIR / "data"

        self.ruta_archivo = DATA_DIR / "poemas.csv"

        # ----------------------------------------------------
        # DATOS
        # ----------------------------------------------------

        self.poemas = []

        self.poemas_normalizados = []

        self.perfiles_autores = {}

        self.lista_autores = []

        # ----------------------------------------------------
        # CONFIGURACIÓN VISUAL
        # ----------------------------------------------------

        self.configurar_estilos()

        # ----------------------------------------------------
        # CABECERA
        # ----------------------------------------------------

        header = tk.Frame(
            root,
            bg=COLOR_FONDO
        )

        header.pack(pady=15)

        tk.Label(
            header,
            text="Generador y Analizador de Poesía",
            font=("Segoe UI", 22, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_ACENTO
        ).pack()

        # ----------------------------------------------------
        # NOTEBOOK
        # ----------------------------------------------------

        self.notebook = ttk.Notebook(root)

        self.notebook.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=10
        )

        # ====================================================
        # TAB GENERADOR
        # ====================================================

        self.tab_generador = tk.Frame(
            self.notebook,
            bg=COLOR_FRAME
        )

        self.notebook.add(
            self.tab_generador,
            text="   🤖 Generar Poemas (IA)   "
        )

        self.construir_tab_generador()

        # ====================================================
        # TAB ANALIZADOR
        # ====================================================

        self.tab_usuario = tk.Frame(
            self.notebook,
            bg=COLOR_FRAME
        )

        self.notebook.add(
            self.tab_usuario,
            text="   ✍️ Analizar mi Estilo   "
        )

        self.construir_tab_usuario()

        # ----------------------------------------------------
        # CARGA DE DATOS
        # ----------------------------------------------------

        self.root.after(100, self.cargar_datos)

    # ========================================================
    # ESTILOS
    # ========================================================

    def configurar_estilos(self):

        style = ttk.Style()

        style.theme_use('clam')

        style.configure(
            "TNotebook",
            background=COLOR_FONDO,
            borderwidth=0
        )

        style.configure(
            "TNotebook.Tab",
            background=COLOR_SECUNDARIO,
            foreground="white",
            padding=[15, 8],
            font=FUENTE_TEXTO
        )

        style.map(
            "TNotebook.Tab",
            background=[("selected", COLOR_ACENTO)],
            foreground=[("selected", "white")]
        )

        style.configure(
            "Boton.TButton",
            font=("Segoe UI", 10, "bold"),
            background=COLOR_ACENTO,
            foreground="white",
            borderwidth=0
        )

        style.map(
            "Boton.TButton",
            background=[('active', '#007f85')]
        )

    # ========================================================
    # TAB GENERADOR
    # ========================================================

    def construir_tab_generador(self):

        frame_sel = tk.LabelFrame(
            self.tab_generador,
            text="1. Selecciona Autor",
            bg=COLOR_FRAME,
            fg=COLOR_ACENTO,
            font=FUENTE_TITULO
        )

        frame_sel.pack(
            fill="x",
            padx=20,
            pady=10
        )

        tk.Label(
            frame_sel,
            text="Escritor:",
            bg=COLOR_FRAME,
            fg=COLOR_TEXTO,
            font=FUENTE_TEXTO
        ).pack(side="left", padx=10)

        self.combo_autores = ttk.Combobox(
            frame_sel,
            state="readonly",
            width=35,
            font=FUENTE_TEXTO
        )

        self.combo_autores.pack(
            side="left",
            padx=10,
            pady=10
        )

        ttk.Button(
            frame_sel,
            text="🔄 Recargar",
            command=self.cargar_datos,
            style="Boton.TButton"
        ).pack(side="right", padx=10)

        # ----------------------------------------------------

        frame_config = tk.LabelFrame(
            self.tab_generador,
            text="2. Método de Generación",
            bg=COLOR_FRAME,
            fg=COLOR_ACENTO,
            font=FUENTE_TITULO
        )

        frame_config.pack(
            fill="x",
            padx=20,
            pady=5
        )

        sub_notebook = ttk.Notebook(frame_config)

        sub_notebook.pack(
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )

        # ====================================================
        # ESTILO
        # ====================================================

        self.frame_estilo = tk.Frame(
            sub_notebook,
            bg=COLOR_SECUNDARIO
        )

        sub_notebook.add(
            self.frame_estilo,
            text=" Estilo "
        )

        self.crear_controles_estilo()

        # ====================================================
        # TÓPICO
        # ====================================================

        self.frame_topico = tk.Frame(
            sub_notebook,
            bg=COLOR_SECUNDARIO
        )

        sub_notebook.add(
            self.frame_topico,
            text=" Tópico "
        )

        tk.Label(
            self.frame_topico,
            text="Palabras clave:",
            bg=COLOR_SECUNDARIO,
            fg="white"
        ).pack(side="left", padx=10)

        self.entry_claves = tk.Entry(
            self.frame_topico,
            width=30
        )

        self.entry_claves.insert(
            0,
            "amor, noche, luz"
        )

        self.entry_claves.pack(
            side="left",
            padx=5
        )

        ttk.Button(
            self.frame_topico,
            text="🔍 Generar",
            command=self.generar_topico,
            style="Boton.TButton"
        ).pack(side="left", padx=15)

        # ====================================================
        # RIMA
        # ====================================================

        self.frame_rima = tk.Frame(
            sub_notebook,
            bg=COLOR_SECUNDARIO
        )

        sub_notebook.add(
            self.frame_rima,
            text=" Rima ABAB "
        )

        tk.Label(
            self.frame_rima,
            text="Palabras clave:",
            bg=COLOR_SECUNDARIO,
            fg="white"
        ).grid(row=0, column=0, padx=10, pady=15)

        self.entry_claves_rima = tk.Entry(
            self.frame_rima,
            width=30
        )

        self.entry_claves_rima.insert(
            0,
            "vida, muerte, cielo"
        )

        self.entry_claves_rima.grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Label(
            self.frame_rima,
            text="Párrafos:",
            bg=COLOR_SECUNDARIO,
            fg="white"
        ).grid(row=0, column=2)

        self.spin_p_rima = tk.Spinbox(
            self.frame_rima,
            from_=1,
            to=10,
            width=5
        )

        self.spin_p_rima.insert(0, 3)

        self.spin_p_rima.grid(row=0, column=3)

        ttk.Button(
            self.frame_rima,
            text="🎶 Generar",
            command=self.generar_rima,
            style="Boton.TButton"
        ).grid(row=0, column=5, padx=20)

        # ----------------------------------------------------

        tk.Label(
            self.tab_generador,
            text="Resultado:",
            bg=COLOR_FRAME,
            fg="white"
        ).pack(anchor="w", padx=20)

        self.txt_res_gen = scrolledtext.ScrolledText(
            self.tab_generador,
            height=12,
            bg="#1e1e1e",
            fg=COLOR_ACENTO,
            font=("Georgia", 12),
            insertbackground="white"
        )

        self.txt_res_gen.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

    # ========================================================
    # CONTROLES ESTILO
    # ========================================================

    def crear_controles_estilo(self):

        tk.Label(
            self.frame_estilo,
            text="Párrafos:",
            bg=COLOR_SECUNDARIO,
            fg="white"
        ).grid(row=0, column=0, padx=5, pady=15)

        self.spin_p_estilo = tk.Spinbox(
            self.frame_estilo,
            from_=1,
            to=10,
            width=5
        )

        self.spin_p_estilo.insert(0, 4)

        self.spin_p_estilo.grid(row=0, column=1)

        tk.Label(
            self.frame_estilo,
            text="Versos:",
            bg=COLOR_SECUNDARIO,
            fg="white"
        ).grid(row=0, column=2, padx=5)

        self.spin_v_estilo = tk.Spinbox(
            self.frame_estilo,
            from_=1,
            to=10,
            width=5
        )

        self.spin_v_estilo.insert(0, 4)

        self.spin_v_estilo.grid(row=0, column=3)

        tk.Label(
            self.frame_estilo,
            text="Palabras:",
            bg=COLOR_SECUNDARIO,
            fg="white"
        ).grid(row=0, column=4, padx=5)

        self.spin_w_estilo = tk.Spinbox(
            self.frame_estilo,
            from_=1,
            to=20,
            width=5
        )

        self.spin_w_estilo.insert(0, 8)

        self.spin_w_estilo.grid(row=0, column=5)

        ttk.Button(
            self.frame_estilo,
            text="✨ Generar",
            command=self.generar_estilo,
            style="Boton.TButton"
        ).grid(row=0, column=6, padx=20)

    # ========================================================
    # TAB ANALIZADOR
    # ========================================================

    def construir_tab_usuario(self):

        paned = tk.PanedWindow(
            self.tab_usuario,
            orient=tk.HORIZONTAL,
            bg=COLOR_FRAME,
            sashwidth=4
        )

        paned.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        frame_izq = tk.Frame(
            paned,
            bg=COLOR_FRAME
        )

        frame_der = tk.Frame(
            paned,
            bg="#222222"
        )

        paned.add(frame_izq, width=500)

        paned.add(frame_der)

        tk.Label(
            frame_izq,
            text="Escribe tu poema aquí:",
            bg=COLOR_FRAME,
            fg="white",
            font=FUENTE_TITULO
        ).pack(pady=10)

        self.txt_input_user = scrolledtext.ScrolledText(
            frame_izq,
            height=20,
            bg="#1e1e1e",
            fg="white",
            font=("Georgia", 11),
            insertbackground="white"
        )

        self.txt_input_user.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        ttk.Button(
            frame_izq,
            text="📊 ANALIZAR",
            command=self.analizar_usuario_avanzado,
            style="Boton.TButton"
        ).pack(
            pady=15,
            fill="x",
            padx=10
        )

        tk.Label(
            frame_der,
            text="Resultados",
            bg="#222222",
            fg=COLOR_ACENTO,
            font=FUENTE_TITULO
        ).pack(pady=10)

        self.txt_reporte = scrolledtext.ScrolledText(
            frame_der,
            bg="#222222",
            fg="#dddddd",
            font=("Consolas", 10),
            bd=0
        )

        self.txt_reporte.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

    # ========================================================
    # CARGAR DATOS
    # ========================================================

    def cargar_datos(self):

        try:

            self.poemas = leer.leer_csv(
                self.ruta_archivo
            )

            self.poemas_normalizados = []

            self.perfiles_autores = {}

            autores_set = set()

            traductor = str.maketrans(
                '',
                '',
                string.punctuation
            )

            if not self.poemas:

                messagebox.showerror(
                    "Error",
                    "Archivo CSV vacío"
                )

                return

            for fila in self.poemas[1:]:

                if len(fila) > 1:

                    autor = fila[0]

                    texto = fila[1]

                    autores_set.add(autor)

                    tokens = [
                        t.lower().translate(traductor)
                        for t in texto.split()
                    ]

                    tokens = [
                        t for t in tokens if t
                    ]

                    self.poemas_normalizados.append(
                        tokens
                    )

                    if autor not in self.perfiles_autores:
                        self.perfiles_autores[autor] = []

                    self.perfiles_autores[autor].extend(
                        tokens
                    )

            for autor in self.perfiles_autores:

                self.perfiles_autores[autor] = set(
                    self.perfiles_autores[autor]
                )

            self.lista_autores = sorted(
                list(autores_set)
            )

            self.combo_autores['values'] = (
                self.lista_autores
            )

            if self.lista_autores:
                self.combo_autores.current(0)

            messagebox.showinfo(
                "Sistema",
                f"Autores cargados: "
                f"{len(self.lista_autores)}"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ========================================================
    # ANÁLISIS
    # ========================================================

    def calcular_similitud_jaccard(self, tokens_usuario):

        set_usuario = set(tokens_usuario)

        mejor_match = "Desconocido"

        mejor_score = 0

        ranking = []

        for autor, set_autor in self.perfiles_autores.items():

            interseccion = len(
                set_usuario.intersection(set_autor)
            )

            union = len(
                set_usuario.union(set_autor)
            )

            score = (
                (interseccion / union) * 100
                if union > 0 else 0
            )

            ranking.append((autor, score))

            if score > mejor_score:

                mejor_score = score

                mejor_match = autor

        ranking.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return mejor_match, mejor_score, ranking[:3]

    def analizar_usuario_avanzado(self):

        texto = self.txt_input_user.get(
            "1.0",
            tk.END
        ).strip()

        if len(texto) < 5:

            messagebox.showwarning(
                "Texto corto",
                "Escribe un poema válido."
            )

            return

        traductor = str.maketrans(
            '',
            '',
            string.punctuation
        )

        tokens = [
            p.lower().translate(traductor)
            for p in texto.split()
        ]

        tokens = [p for p in tokens if p]

        versos = [
            v for v in texto.split('\n')
            if v.strip()
        ]

        num_palabras = len(tokens)

        top_palabras = Counter(tokens).most_common(5)

        match_nombre, match_score, top3 = (
            self.calcular_similitud_jaccard(tokens)
        )

        reporte = f"""
========================================
REPORTE DE ESTILO
========================================

Versos: {len(versos)}
Palabras: {num_palabras}

Palabras frecuentes:
{top_palabras}

Autor más similar:
{match_nombre}

Similitud:
{match_score:.2f}%

========================================
"""

        self.txt_reporte.delete(
            1.0,
            tk.END
        )

        self.txt_reporte.insert(
            tk.END,
            reporte
        )

    # ========================================================
    # GENERADORES
    # ========================================================

    def obtener_autor(self):

        return self.combo_autores.get()

    def generar_estilo(self):

        autor = self.obtener_autor()

        if autor:

            try:

                vocab = (
                    analizar.analizar_vocabulario_escritor(
                        self.poemas,
                        self.poemas_normalizados,
                        autor
                    )
                )

                poema = generar.generar_poemas_escritor(
                    self.poemas,
                    self.poemas_normalizados,
                    autor,
                    vocab,
                    int(self.spin_p_estilo.get()),
                    int(self.spin_v_estilo.get()),
                    int(self.spin_w_estilo.get())
                )

                self.mostrar_resultado(poema)

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    str(e)
                )

    def generar_topico(self):

        autor = self.obtener_autor()

        if autor:

            poema = generar2.generar_poemas_por_topico(
                self.poemas,
                self.poemas_normalizados,
                autor,
                self.entry_claves.get().split(","),
                3,
                4
            )

            self.mostrar_resultado(poema)

    def generar_rima(self):

        autor = self.obtener_autor()

        if autor:

            try:

                poema = (
                    generar3.generar_poemas_vocabulario_refuerzo(
                        self.poemas,
                        autor,
                        self.entry_claves_rima.get().split(","),
                        int(self.spin_p_rima.get()),
                        4
                    )
                )

                self.mostrar_resultado(poema)

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    str(e)
                )

    # ========================================================
    # RESULTADOS
    # ========================================================

    def mostrar_resultado(self, texto):

        self.txt_res_gen.delete(
            1.0,
            tk.END
        )

        self.txt_res_gen.insert(
            tk.END,
            texto
        )