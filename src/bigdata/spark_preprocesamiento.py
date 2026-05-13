from pyspark.sql.functions import lower
from pyspark.sql.functions import regexp_replace
from pyspark.sql.functions import split
from pyspark.sql.functions import col


def cargar_poemas_spark(spark, ruta_csv):

    df = (
        spark.read
        .option("header", True)
        .option("multiLine", True)
        .option("escape", '"')
        .csv(ruta_csv)
    )

    return df



def limpiar_poemas(df):

    df_limpio = (
        df
        .withColumn(
            "poema_limpio",
            lower(
                regexp_replace(
                    col("content"),
                    "[^a-zA-ZáéíóúÁÉÍÓÚñÑ\\s]",
                    ""
                )
            )
        )
    )

    return df_limpio



def tokenizar_poemas(df):

    df_tokens = df.withColumn(
        "tokens",
        split(col("poema_limpio"), "\\s+")
    )

    return df_tokens