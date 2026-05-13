from pyspark.sql.functions import size
from pyspark.sql.functions import avg
from pyspark.sql.functions import explode
from pyspark.sql.functions import col
from pyspark.sql.functions import count
from pyspark.sql.functions import desc



def estadisticas_generales(df_tokens):

    estadisticas = (
        df_tokens
        .withColumn(
            "num_palabras",
            size(col("tokens"))
        )
        .select(
            avg("num_palabras").alias("promedio_palabras")
        )
    )

    return estadisticas



def top_palabras_globales(df_tokens, limite=20):

    top_palabras = (
        df_tokens
        .select(explode(col("tokens")).alias("palabra"))
        .groupBy("palabra")
        .agg(count("palabra").alias("frecuencia"))
        .orderBy(desc("frecuencia"))
        .limit(limite)
    )

    return top_palabras