import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter

from wordcloud import WordCloud

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans


# =========================================================
# CREAR CARPETAS
# =========================================================

def crear_carpetas_results():

    carpetas = [
        "results",
        "results/vocabulario",
        "results/visualizaciones",
        "results/estadisticas",
        "results/generados",
        "results/modelos",
        "results/embeddings"
    ]

    for carpeta in carpetas:
        os.makedirs(carpeta, exist_ok=True)

    print("Carpetas creadas correctamente.")


# =========================================================
# NUBE DE PALABRAS
# =========================================================

def generar_nube_palabras(df):

    texto = " ".join(df["texto_limpio"])

    nube = WordCloud(
        width=1200,
        height=600,
        background_color="white"
    ).generate(texto)

    plt.figure(figsize=(14, 7))

    plt.imshow(nube)

    plt.axis("off")

    ruta = (
        "results/visualizaciones/"
        "nube_palabras.png"
    )

    plt.savefig(
        ruta,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Nube guardada en: {ruta}")


# =========================================================
# HISTOGRAMA LONGITUDES
# =========================================================

def generar_histograma_longitudes(df):

    plt.figure(figsize=(10, 6))

    plt.hist(
        df["num_palabras"],
        bins=30
    )

    plt.xlabel("Número de palabras")
    plt.ylabel("Frecuencia")
    plt.title("Distribución de longitud de poemas")

    ruta = (
        "results/visualizaciones/"
        "histograma_longitudes.png"
    )

    plt.savefig(ruta)

    plt.close()

    print(f"Histograma guardado en: {ruta}")


# =========================================================
# TOP PALABRAS CSV
# =========================================================

def guardar_top_palabras(df, top_n=50):

    palabras = []

    for tokens in df["tokens"]:
        palabras.extend(tokens)

    conteo = Counter(palabras)

    top = conteo.most_common(top_n)

    df_top = pd.DataFrame(
        top,
        columns=[
            "palabra",
            "frecuencia"
        ]
    )

    ruta = (
        "results/vocabulario/"
        "top_palabras.csv"
    )

    df_top.to_csv(
        ruta,
        index=False,
        encoding="utf-8"
    )

    print(f"Top palabras guardado en: {ruta}")


# =========================================================
# GRÁFICA TOP PALABRAS
# =========================================================

def grafica_top_palabras(df, top_n=20):

    palabras = []

    for tokens in df["tokens"]:
        palabras.extend(tokens)

    conteo = Counter(palabras)

    top = conteo.most_common(top_n)

    palabras_top = [
        x[0] for x in top
    ]

    frecuencias = [
        x[1] for x in top
    ]

    plt.figure(figsize=(12, 6))

    plt.bar(
        palabras_top,
        frecuencias
    )

    plt.xticks(rotation=45)

    plt.title("Top palabras")

    ruta = (
        "results/visualizaciones/"
        "top_palabras.png"
    )

    plt.savefig(
        ruta,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Gráfica guardada en: {ruta}")


# =========================================================
# ESTADÍSTICAS GENERALES
# =========================================================

def guardar_estadisticas(df):

    stats = {

        "total_poemas":
            int(len(df)),

        "promedio_palabras":
            float(df["num_palabras"].mean()),

        "max_palabras":
            int(df["num_palabras"].max()),

        "min_palabras":
            int(df["num_palabras"].min())
    }

    ruta = (
        "results/estadisticas/"
        "estadisticas_generales.json"
    )

    with open(
        ruta,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            stats,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"Estadísticas guardadas en: {ruta}")


# =========================================================
# DATASET LIMPIO
# =========================================================

def guardar_dataset_limpio(df):

    ruta = (
        "results/estadisticas/"
        "dataset_limpio.csv"
    )

    df.to_csv(
        ruta,
        index=False,
        encoding="utf-8"
    )

    print(f"Dataset limpio guardado en: {ruta}")


# =========================================================
# EMBEDDINGS TF-IDF
# =========================================================

def generar_embeddings_tfidf(df):

    vectorizer = TfidfVectorizer(
        max_features=500
    )

    X = vectorizer.fit_transform(
        df["texto_limpio"]
    )

    embeddings = X.toarray()

    ruta = (
        "results/embeddings/"
        "embeddings.npy"
    )

    np.save(ruta, embeddings)

    print(f"Embeddings guardados en: {ruta}")

    guardar_modelo_tfidf(vectorizer)

    return embeddings

def guardar_modelo_tfidf(vectorizer):

    ruta = (
        "results/modelos/"
        "tfidf_vectorizer.pkl"
    )

    joblib.dump(
        vectorizer,
        ruta
    )

    print(f"Modelo TF-IDF guardado en: {ruta}")

# =========================================================
# VISUALIZACIÓN t-SNE
# =========================================================

from sklearn.decomposition import PCA


def visualizar_tsne(
    embeddings,
    clusters=None
):

    pca = PCA(
        n_components=50
    )

    embeddings_pca = pca.fit_transform(
        embeddings
    )

    tsne = TSNE(
        n_components=2,
        random_state=42
    )

    X_2d = tsne.fit_transform(
        embeddings_pca
    )

    plt.figure(figsize=(12, 8))

    if clusters is not None:

        plt.scatter(
            X_2d[:, 0],
            X_2d[:, 1],
            c=clusters
        )

    else:

        plt.scatter(
            X_2d[:, 0],
            X_2d[:, 1]
        )

    plt.title(
        "Visualización t-SNE de embeddings"
    )

    ruta = (
        "results/visualizaciones/"
        "embeddings_tsne.png"
    )

    plt.savefig(ruta)

    plt.close()

    print(f"t-SNE guardado en: {ruta}")


# =========================================================
# CLUSTERING KMEANS
# =========================================================

def clustering_poemas(
    embeddings,
    n_clusters=5
):

    modelo = KMeans(
        n_clusters=n_clusters,
        random_state=42
    )

    clusters = modelo.fit_predict(
        embeddings
    )

    df_clusters = pd.DataFrame({
        "cluster": clusters
    })

    ruta = (
        "results/estadisticas/"
        "clusters.csv"
    )

    df_clusters.to_csv(
        ruta,
        index=False
    )

    print(f"Clusters guardados en: {ruta}")

    return clusters


# =========================================================
# GUARDAR POEMA GENERADO
# =========================================================

def guardar_poema_generado(
    poema,
    nombre="poema_generado.txt"
):

    ruta = f"results/generados/{nombre}"

    with open(
        ruta,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(poema)

    print(f"Poema guardado en: {ruta}")

from random import choice


def generar_poema_aleatorio(
    df,
    longitud=30
):

    palabras = []

    for tokens in df["tokens"]:
        palabras.extend(tokens)

    poema = " ".join(

        choice(palabras)

        for _ in range(longitud)
    )

    return poema

def generar_multiples_poemas(
    df,
    cantidad=5
):

    for i in range(cantidad):

        poema = generar_poema_aleatorio(df)

        guardar_poema_generado(
            poema,
            f"poema_{i+1}.txt"
        )

def generar_matriz_similitud(
    embeddings,
    max_muestras=10
):

    if len(embeddings) > max_muestras:

        indices = np.random.choice(
            len(embeddings),
            max_muestras,
            replace=False
        )

        embeddings = embeddings[indices]

    similitud = cosine_similarity(
        embeddings
    )

    plt.figure(figsize=(10, 8))

    plt.imshow(
        similitud,
        aspect="auto"
    )

    plt.colorbar()

    plt.title(
        "Matriz de similitud"
    )

    ruta = (
        "results/visualizaciones/"
        "matriz_similitud.png"
    )

    plt.savefig(
        ruta,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Matriz guardada en: {ruta}")

def generar_bigramas(
    df,
    top_n=20
):

    vectorizer = CountVectorizer(
        ngram_range=(2, 2),
        max_features=top_n
    )

    X = vectorizer.fit_transform(
        df["texto_limpio"]
    )

    palabras = (
        vectorizer
        .get_feature_names_out()
    )

    frecuencias = (
        X.sum(axis=0)
        .A1
    )

    df_bi = pd.DataFrame({

        "bigrama":
            palabras,

        "frecuencia":
            frecuencias
    })

    df_bi = df_bi.sort_values(
        by="frecuencia",
        ascending=False
    )

    ruta = (
        "results/vocabulario/"
        "bigramas.csv"
    )

    df_bi.to_csv(
        ruta,
        index=False
    )

    print(f"Bigramas guardados en: {ruta}") 

def generar_trigramas(
    df,
    top_n=20
):

    vectorizer = CountVectorizer(
        ngram_range=(3, 3),
        max_features=top_n
    )

    X = vectorizer.fit_transform(
        df["texto_limpio"]
    )

    palabras = (
        vectorizer
        .get_feature_names_out()
    )

    frecuencias = (
        X.sum(axis=0)
        .A1
    )

    df_tri = pd.DataFrame({

        "trigrama":
            palabras,

        "frecuencia":
            frecuencias
    })

    df_tri = df_tri.sort_values(
        by="frecuencia",
        ascending=False
    )

    ruta = (
        "results/vocabulario/"
        "trigramas.csv"
    )

    df_tri.to_csv(
        ruta,
        index=False
    )

    print(f"Trigramas guardados en: {ruta}")