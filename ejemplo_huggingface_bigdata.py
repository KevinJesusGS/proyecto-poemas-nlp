from src.bigdata.cargar_dataset_hf import (
    cargar_poemas_huggingface
)

from src.bigdata.analisis_huggingface import (
    preparar_dataframe,
    obtener_vocabulario_global,
    obtener_vocabulario_autor,
    estadisticas_generales,
    exportar_vocabulario
)

# ==========================
# CARGAR DATASET
# ==========================

print("Cargando dataset...")

df = cargar_poemas_huggingface()

print(df.head())

# ==========================
# PREPROCESAMIENTO
# ==========================

print("\nPreparando textos...")

df = preparar_dataframe(df)

print(df[[
    "texto_limpio",
    "num_palabras"
]].head())

# ==========================
# VOCABULARIO GLOBAL
# ==========================

print("\nTop palabras globales:")

vocabulario = obtener_vocabulario_global(df)

for palabra, freq in vocabulario:
    print(f"{palabra}: {freq}")

# ==========================
# ESTADÍSTICAS
# ==========================

print("\nEstadísticas generales:")

stats = estadisticas_generales(df)

for k, v in stats.items():
    print(f"{k}: {v}")

# ==========================
# VOCABULARIO AUTOR
# ==========================

try:
    autor = df["author"].iloc[0]

    print(f"\nAnalizando autor: {autor}")

    vocab_autor = obtener_vocabulario_autor(
        df,
        autor
    )

    for palabra, freq in vocab_autor:
        print(f"{palabra}: {freq}")

except Exception as e:
    print("No se pudo analizar autor:")
    print(e)

# ==========================
# EXPORTAR RESULTADOS
# ==========================

exportar_vocabulario(vocabulario)

print("\nProceso finalizado.")

from src.visualization.resultados import *

crear_carpetas_results()

generar_nube_palabras(df)

generar_histograma_longitudes(df)

guardar_top_palabras(df)

grafica_top_palabras(df)

guardar_estadisticas(df)

guardar_dataset_limpio(df)

embeddings = generar_embeddings_tfidf(df)

clusters = clustering_poemas(
    embeddings
)

visualizar_tsne(
    embeddings,
    clusters
)

generar_matriz_similitud(
    embeddings
)

generar_bigramas(df)

generar_trigramas(df)

generar_multiples_poemas(df)