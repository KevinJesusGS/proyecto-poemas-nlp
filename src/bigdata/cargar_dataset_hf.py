from datasets import load_dataset
import pandas as pd


def cargar_poemas_huggingface(
    nombre_dataset="poem_sentiment"
):

    dataset = load_dataset(nombre_dataset)

    df = pd.DataFrame(dataset["train"])

    return df