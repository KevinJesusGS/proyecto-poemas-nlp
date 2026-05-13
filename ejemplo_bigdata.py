from src.bigdata.spark_session import crear_sesion_spark
from src.bigdata.spark_preprocesamiento import cargar_poemas_spark
from src.bigdata.spark_preprocesamiento import limpiar_poemas
from src.bigdata.spark_preprocesamiento import tokenizar_poemas

from src.bigdata.spark_vocabulario import obtener_vocabulario_autor
from src.bigdata.spark_estadisticas import top_palabras_globales
from src.bigdata.spark_estadisticas import estadisticas_generales
from src.bigdata.spark_similitud import similitud_jaccard


spark = crear_sesion_spark()


df = cargar_poemas_spark(
    spark,
    "data/poemas.csv"
)


df = limpiar_poemas(df)


df = tokenizar_poemas(df)


print("=== Top palabras globales ===")

top = top_palabras_globales(df)

top.show()


print("=== Estadísticas ===")

estadisticas = estadisticas_generales(df)

estadisticas.show()


print("=== Vocabulario de autor ===")

vocabulario = obtener_vocabulario_autor(
    df,
    "Leopoldo Lugones"
)

vocabulario.show(20)


print("=== Similitud ===")

sim = similitud_jaccard(
    df,
    "Leopoldo Lugones",
    "Rubén Darío"
)

print(sim)

from src.bigdata.cargar_dataset_hf import cargar_poemas_huggingface

df_hf = cargar_poemas_huggingface()

print(df_hf.head())