from pyspark.sql.functions import (
    col,
    explode,
    split,
    desc
)


def obtener_vocabulario_autor(df, nombre_autor):

    df_tokens = (
        df.withColumn(
            "tokens",
            split(col("poema_limpio"), r"\s+")
        )
    )

    df_autor = df_tokens.filter(
        col("author") == nombre_autor
    )

    palabras = (
        df_autor
        .select(explode(col("tokens")).alias("palabra"))
        .groupBy("palabra")
        .count()
        .withColumnRenamed("count", "frecuencia")
        .orderBy(desc("frecuencia"))
    )

    return palabras