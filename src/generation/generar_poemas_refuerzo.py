import random
import string
import os
import json
from datetime import datetime

# ============================================================
# VOCABULARIO DE RIMAS
# ============================================================

VOCABULARIO_RIMAS_REFUERZO = {

    "or": [
        "dolor",
        "color",
        "temblor",
        "ardor",
        "resplandor"
    ],

    "ar": [
        "mar",
        "cantar",
        "pasar",
        "olvidar",
        "lugar"
    ],

    "as": [
        "alas",
        "ramas",
        "sombras",
        "aguas",
        "casas"
    ],

    "te": [
        "muerte",
        "suerte",
        "frente",
        "verte",
        "siempre"
    ],

    "ia": [
        "vida",
        "alegría",
        "día",
        "fría",
        "mía"
    ],

    "do": [
        "mundo",
        "olvido",
        "lado",
        "todo",
        "claro"
    ],

    "che": [
        "noche",
        "broche",
        "derroche"
    ]
}

# ============================================================
# PALABRAS AUXILIARES
# ============================================================

ADJETIVOS = [
    "lento",
    "oscuro",
    "lejano",
    "fuerte",
    "bello",
    "frágil",
    "silencioso"
]

SUSTANTIVOS = [
    "cielo",
    "corazón",
    "tiempo",
    "alma",
    "viento",
    "camino",
    "silencio"
]

VERBOS = [
    "trae",
    "siente",
    "oculta",
    "busca",
    "muestra",
    "recuerda",
    "observa"
]

# ============================================================
# NORMALIZACIÓN
# ============================================================

def normalizar_verso(verso):

    verso = verso.strip()

    if not verso:
        return verso

    verso = verso.lower()

    return verso[0].upper() + verso[1:]


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def extraer_terminacion_rima(
    palabra,
    num_letras=3
):

    mapa = str.maketrans(
        "áéíóúüñÁÉÍÓÚÜÑ",
        "aeiouunAEIOUUN"
    )

    palabra_proc = palabra.lower().translate(mapa)

    palabra_proc = "".join(
        c for c in palabra_proc if c.isalpha()
    )

    if len(palabra_proc) <= num_letras:
        return palabra_proc

    return palabra_proc[-num_letras:]


def obtener_ultima_palabra(verso):

    trad = str.maketrans(
        "",
        "",
        string.punctuation
    )

    palabras = verso.strip().split()

    if not palabras:
        return ""

    palabra = palabras[-1].lower()

    palabra = palabra.translate(trad)

    mapa = str.maketrans(
        "áéíóúüñÁÉÍÓÚÜÑ",
        "aeiouunAEIOUUN"
    )

    return palabra.translate(mapa)


def verificar_rima_flexible(r1, r2):

    if not r1 or not r2:
        return False

    if r1 == r2:
        return True

    if len(r1) >= 2 and len(r2) >= 2:

        if r1[-2:] == r2[-2:]:
            return True

    return False


# ============================================================
# DICCIONARIO EXTERNO
# ============================================================

def cargar_diccionario_palabras(
    ruta="data/diccionario_palabras.csv"
):

    palabras = []

    try:

        with open(
            ruta,
            "r",
            encoding="utf-8"
        ) as f:

            for linea in f:

                palabra = linea.strip().lower()

                if palabra:

                    palabra = "".join(
                        c for c in palabra
                        if c.isalpha() or c == "ñ"
                    )

                    if palabra:
                        palabras.append(palabra)

    except FileNotFoundError:

        print(
            "[Aviso] "
            "No se encontró diccionario_palabras.csv"
        )

    return palabras


def buscar_palabras_por_topico(
    diccionario,
    claves
):

    relacionadas = []

    claves = [c.lower() for c in claves]

    for palabra in diccionario:

        for clave in claves:

            if clave in palabra:

                if palabra not in relacionadas:
                    relacionadas.append(palabra)

    return relacionadas


def integrar_diccionario_a_rimas(
    palabras,
    num_letras=3
):

    for palabra in palabras:

        terminacion = extraer_terminacion_rima(
            palabra,
            num_letras
        )

        if not terminacion:
            continue

        if terminacion not in VOCABULARIO_RIMAS_REFUERZO:

            VOCABULARIO_RIMAS_REFUERZO[
                terminacion
            ] = []

        if (
            palabra
            not in VOCABULARIO_RIMAS_REFUERZO[
                terminacion
            ]
        ):

            VOCABULARIO_RIMAS_REFUERZO[
                terminacion
            ].append(palabra)


# ============================================================
# GENERADOR DE VERSOS
# ============================================================

def generar_verso_de_refuerzo(
    rima,
    excluir,
    palabras_diccionario=None,
    num_letras_rima=3
):

    candidatos = []

    if palabras_diccionario:

        for palabra in palabras_diccionario:

            terminacion = extraer_terminacion_rima(
                palabra,
                num_letras_rima
            )

            if (
                verificar_rima_flexible(
                    terminacion,
                    rima
                )
                and palabra not in excluir
            ):

                candidatos.append(palabra)

    for terminacion, lista_palabras in (
        VOCABULARIO_RIMAS_REFUERZO.items()
    ):

        if verificar_rima_flexible(
            terminacion,
            rima
        ):

            for palabra in lista_palabras:

                if (
                    palabra not in excluir
                    and palabra not in candidatos
                ):
                    candidatos.append(palabra)

    if not candidatos:
        return None

    palabra_final = random.choice(candidatos)

    adjetivo = random.choice(ADJETIVOS)

    sustantivo = random.choice(SUSTANTIVOS)

    verbo = random.choice(VERBOS)

    verso = (
        f"El {adjetivo} "
        f"{sustantivo} "
        f"{verbo} "
        f"{palabra_final}"
    )

    return verso.capitalize() + "."


# ============================================================
# GENERADOR PRINCIPAL
# ============================================================

def generar_poemas_vocabulario_refuerzo(
    poemas,
    nombre_autor,
    palabras_clave,
    num_parrafos,
    num_versos,
    num_letras_rima=3,
    patron_rima="ABAB"
):

    traductor = str.maketrans(
        "",
        "",
        string.punctuation
    )

    palabras_clave = [
        p.lower().translate(traductor)
        for p in palabras_clave
    ]

    diccionario = cargar_diccionario_palabras()

    palabras_diccionario = (
        buscar_palabras_por_topico(
            diccionario,
            palabras_clave
        )
    )

    integrar_diccionario_a_rimas(
        palabras_diccionario,
        num_letras=num_letras_rima
    )

    versos_disponibles = []

    versos_vistos = set()

    for fila in poemas[1:]:

        autor = fila[0]

        poema = fila[1]

        versos = poema.split("\n")

        for verso in versos:

            verso_limpio = verso.strip()

            if (
                not verso_limpio
                or verso_limpio in versos_vistos
            ):
                continue

            verso_min = verso_limpio.lower()

            verso_sin_punt = verso_min.translate(
                traductor
            )

            if any(
                palabra in verso_sin_punt
                for palabra in palabras_clave
            ):

                ultima = obtener_ultima_palabra(
                    verso_limpio
                )

                rima = extraer_terminacion_rima(
                    ultima,
                    num_letras_rima
                )

                versos_disponibles.append({

                    "verso": verso_limpio,

                    "rima": rima,

                    "ultima_palabra": ultima,

                    "autor": autor
                })

                versos_vistos.add(
                    verso_limpio
                )

    if not versos_disponibles:

        return (
            "[Aviso] "
            "No hay versos disponibles."
        )

    poema_final = []

    for _ in range(num_parrafos):

        usados = set()

        versos_parrafo = []

        verso_a1 = random.choice(
            versos_disponibles
        )

        usados.add(
            verso_a1["ultima_palabra"]
        )

        rima_a = verso_a1["rima"]

        versos_parrafo.append(
            verso_a1["verso"]
        )

        candidatos_b = [

            v for v in versos_disponibles

            if not verificar_rima_flexible(
                v["rima"],
                rima_a
            )
        ]

        if candidatos_b:

            verso_b1 = random.choice(
                candidatos_b
            )

        else:

            verso_b1 = random.choice(
                versos_disponibles
            )

        usados.add(
            verso_b1["ultima_palabra"]
        )

        rima_b = verso_b1["rima"]

        versos_parrafo.append(
            verso_b1["verso"]
        )

        verso_a2 = generar_verso_de_refuerzo(
            rima_a,
            usados,
            palabras_diccionario,
            num_letras_rima
        )

        if verso_a2:

            usados.add(
                obtener_ultima_palabra(
                    verso_a2
                )
            )

            versos_parrafo.append(
                verso_a2
            )

        verso_b2 = generar_verso_de_refuerzo(
            rima_b,
            usados,
            palabras_diccionario,
            num_letras_rima
        )

        if verso_b2:

            versos_parrafo.append(
                verso_b2
            )

        versos_parrafo = versos_parrafo[
            :num_versos
        ]

        parrafo = "\n".join(

            normalizar_verso(v)

            for v in versos_parrafo
        )

        poema_final.append(parrafo)

    poema_generado = "\n\n".join(
        poema_final
    )

    guardar_poema_refuerzo(
        poema_generado,
        nombre_autor,
        palabras_clave
    )

    return poema_generado

# ============================================================
# MÉTRICAS DE POEMA
# ============================================================

def calcular_metricas_poema(poema):

    versos = [
        v.strip()
        for v in poema.split("\n")
        if v.strip()
    ]

    palabras = []

    for verso in versos:
        palabras.extend(
            verso.lower().split()
        )

    total_versos = len(versos)

    total_palabras = len(palabras)

    promedio_palabras = 0

    if total_versos > 0:

        promedio_palabras = (
            total_palabras / total_versos
        )

    vocabulario_unico = len(set(palabras))

    diversidad_lexica = 0

    if total_palabras > 0:

        diversidad_lexica = (
            vocabulario_unico / total_palabras
        )

    return {

        "total_versos": total_versos,

        "total_palabras": total_palabras,

        "promedio_palabras_verso":
            round(promedio_palabras, 2),

        "vocabulario_unico":
            vocabulario_unico,

        "diversidad_lexica":
            round(diversidad_lexica, 3)
    }

# ============================================================
# GUARDAR POEMAS GENERADOS
# ============================================================

def guardar_poema_refuerzo(
    poema,
    nombre_autor,
    palabras_clave,
    carpeta="results/generados"
):

    os.makedirs(
        carpeta,
        exist_ok=True
    )

    fecha = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    nombre_base = (
        f"poema_refuerzo_{fecha}"
    )

    ruta_txt = (
        f"{carpeta}/{nombre_base}.txt"
    )

    ruta_json = (
        f"{carpeta}/{nombre_base}.json"
    )

    # ========================================================
    # GUARDAR TXT
    # ========================================================

    with open(
        ruta_txt,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(poema)

    # ========================================================
    # MÉTRICAS
    # ========================================================

    metricas = calcular_metricas_poema(
        poema
    )

    data = {

        "autor_objetivo":
            nombre_autor,

        "palabras_clave":
            palabras_clave,

        "fecha":
            fecha,

        "metricas":
            metricas,

        "poema":
            poema
    }

    # ========================================================
    # GUARDAR JSON
    # ========================================================

    with open(
        ruta_json,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"[OK] Poema guardado en:\n"
        f"{ruta_txt}"
    )