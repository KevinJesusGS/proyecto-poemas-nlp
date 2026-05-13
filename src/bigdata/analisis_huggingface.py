# src/bigdata/analisis_huggingface.py

import pandas as pd
import re
from collections import Counter

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import nltk

# Descargar recursos de NLTK
nltk.download("punkt")
nltk.download("stopwords")

STOPWORDS_ES = set(stopwords.words("spanish"))


def limpiar_texto(texto):
    """
    Limpia texto:
    - minúsculas
    - elimina números
    - elimina símbolos
    """

    if pd.isna(texto):
        return ""

    texto = texto.lower()

    texto = re.sub(r"\d+", " ", texto)

    texto = re.sub(
        r"[^a-záéíóúñü\s]",
        " ",
        texto
    )

    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()


def tokenizar_texto(texto):
    """
    Tokeniza y elimina stopwords.
    """

    tokens = word_tokenize(texto, language="spanish")

    tokens_limpios = [
        t for t in tokens
        if t not in STOPWORDS_ES and len(t) > 2
    ]

    return tokens_limpios


def preparar_dataframe(df):
    """
    Prepara dataframe completo.
    """

    # Detectar columna texto
    posibles_columnas = [
        "poema",
        "content",
        "text",
        "texto",
        "verse_text"
    ]
    columna_texto = None

    for col in posibles_columnas:
        if col in df.columns:
            columna_texto = col
            break

    if columna_texto is None:
        raise ValueError(
            "No se encontró columna de texto."
        )

    df["texto_limpio"] = df[columna_texto].apply(
        limpiar_texto
    )

    df["tokens"] = df["texto_limpio"].apply(
        tokenizar_texto
    )

    df["num_palabras"] = df["tokens"].apply(len)

    return df


def obtener_vocabulario_global(df, top_n=50):
    """
    Obtiene palabras más frecuentes.
    """

    todas = []

    for tokens in df["tokens"]:
        todas.extend(tokens)

    conteo = Counter(todas)

    return conteo.most_common(top_n)


def obtener_vocabulario_autor(
    df,
    nombre_autor,
    top_n=30
):
    """
    Obtiene vocabulario específico de autor.
    """

    posibles_autores = [
        "autor",
        "author",
        "poet"
    ]

    columna_autor = None

    for col in posibles_autores:
        if col in df.columns:
            columna_autor = col
            break

    if columna_autor is None:
        raise ValueError(
            "No existe columna de autor."
        )

    df_autor = df[
        df[columna_autor] == nombre_autor
    ]

    palabras = []

    for tokens in df_autor["tokens"]:
        palabras.extend(tokens)

    conteo = Counter(palabras)

    return conteo.most_common(top_n)


def estadisticas_generales(df):
    """
    Estadísticas generales del dataset.
    """

    total_poemas = len(df)

    promedio = df["num_palabras"].mean()

    maximo = df["num_palabras"].max()

    minimo = df["num_palabras"].min()

    return {
        "total_poemas": total_poemas,
        "promedio_palabras": promedio,
        "max_palabras": maximo,
        "min_palabras": minimo
    }


def exportar_vocabulario(
    vocabulario,
    ruta="results/vocabulario.csv"
):
    """
    Exporta vocabulario a CSV.
    """

    df_vocab = pd.DataFrame(
        vocabulario,
        columns=["palabra", "frecuencia"]
    )

    df_vocab.to_csv(
        ruta,
        index=False,
        encoding="utf-8"
    )

    print(f"Archivo guardado en: {ruta}")