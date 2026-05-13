from pyspark.sql.functions import explode
from pyspark.sql.functions import collect_set
from pyspark.sql.functions import col



def obtener_palabras_autor(df_tokens, autor):

    palabras = (
        df_tokens
        .filter(col("author") == autor)
        .select(explode(col("tokens")).alias("palabra"))
        .distinct()
    )

    return set(
        fila["palabra"]
        for fila in palabras.collect()
    )



def similitud_jaccard(df_tokens, autor1, autor2):

    set1 = obtener_palabras_autor(df_tokens, autor1)
    set2 = obtener_palabras_autor(df_tokens, autor2)

    interseccion = len(set1.intersection(set2))
    union = len(set1.union(set2))

    if union == 0:
        return 0

    return interseccion / union