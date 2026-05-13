def analizar_vocabulario_escritor(poemas, poemas_normalizados, nombre_autor):

    frecuencias_palabras_escritor = {}

    for i, fila in enumerate(poemas[1:]):

        if fila[0] == nombre_autor:

            poemas_tokens = poemas_normalizados[i]

            for token in poemas_tokens:
                frecuencias_palabras_escritor[token] = (
                    frecuencias_palabras_escritor.get(token, 0) + 1
                )

    return frecuencias_palabras_escritor