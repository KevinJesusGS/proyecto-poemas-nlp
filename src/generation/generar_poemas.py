import random


def generar_poemas_escritor(
    poemas,
    poemas_normalizados,
    nombre_autor,
    vocabulario_autor,
    num_parrafos,
    num_versos,
    num_palabras
):

    tokens_generados_poema = []

    palabras_peso = []

    for palabra, frec in vocabulario_autor.items():
        palabras_peso.extend([palabra] * frec)

    for parrafo in range(num_parrafos):

        for verso in range(num_versos):

            verso_tokens = []

            for _ in range(num_palabras):

                if palabras_peso:

                    palabra_selec = random.choice(palabras_peso)

                    verso_tokens.append(palabra_selec)

            tokens_generados_poema.extend(verso_tokens)

            if not (
                parrafo == num_parrafos - 1
                and verso == num_versos - 1
            ):
                tokens_generados_poema.append("\n")

        if parrafo < num_parrafos - 1:
            tokens_generados_poema.append("\n")

    texto_poema_generado = " ".join(tokens_generados_poema)

    return texto_poema_generado