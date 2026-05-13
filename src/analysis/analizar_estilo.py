from collections import Counter
import string


def analizar_estilo_escritor(
    poemas,
    poemas_originales,
    poemas_normalizados,
    escritor,
    top_n_bigramas=10
):

    tokens_poemas_escritor = []
    largo_poemas_escritor = []
    versos_tokens = []
    bigramas_escritor = []

    for i, fila in enumerate(poemas[1:]):

        if fila[0] == escritor:

            poema_tokens = poemas_normalizados[i]

            tokens_poemas_escritor.append(poema_tokens)
            largo_poemas_escritor.append(len(poema_tokens))

            contenido_original = poemas_originales[i]

            versos = contenido_original.split("\n")

            for verso in versos:

                verso_tokens = verso.split()

                tokens_normalizados = []

                translator = str.maketrans('', '', string.punctuation)

                for token in verso_tokens:

                    token = token.lower()
                    token = token.translate(translator)

                    if token:
                        tokens_normalizados.append(token)

                if tokens_normalizados:

                    versos_tokens.append(tokens_normalizados)

                    for j in range(len(tokens_normalizados) - 1):

                        bigramas_escritor.append(
                            (
                                tokens_normalizados[j],
                                tokens_normalizados[j + 1]
                            )
                        )

    largo_promedio = (
        sum(largo_poemas_escritor) / len(largo_poemas_escritor)
        if largo_poemas_escritor else 0
    )

    largo_total_versos = sum(len(v) for v in versos_tokens)

    largo_promedio_verso = (
        largo_total_versos / len(versos_tokens)
        if versos_tokens else 0
    )

    top_bigramas = Counter(bigramas_escritor).most_common(top_n_bigramas)

    return {
        "artista": escritor,
        "largo promedio de los poemas": largo_promedio,
        "largo promedio de los versos": largo_promedio_verso,
        "Bigramas más frecuentes del escritor": top_bigramas
    }