from pyspark.sql import SparkSession


def crear_sesion_spark(nombre_app="PoetryBigData"):

    spark = (
        SparkSession
        .builder
        .appName(nombre_app)
        .master("local[*]")
        .getOrCreate()
    )

    return spark