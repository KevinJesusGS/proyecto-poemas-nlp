import random


def normalizar_verso(verso):

    verso = verso.strip()

    if not verso:
        return verso

    verso = verso.lower()

    return verso[0].upper() + verso[1:]


def generar_poemas_por_topico(
    poemas,
    poemas_normalizados,
    nombre_autor,
    palabras_clave,
    num_parrafos,
    num_versos
):

    versos_encontrados = []

    palabras_clave_normalizadas = []

    for palabra in palabras_clave:

        palabra = palabra.lower()

        palabra = "".join(
            c for c in palabra if c.isalnum()
        )

        if palabra:
            palabras_clave_normalizadas.append(
                palabra
            )

    for fila in poemas[1:]:

        if fila[0] == nombre_autor:

            poema_original = fila[1]

            versos = poema_original.split("\n")

            for verso in versos:

                verso_min = verso.lower()

                verso_sin_punt = "".join(
                    c for c in verso_min
                    if c not in ".,;:!?¿¡()[]{}\"'"
                )

                coincidencia = False

                for palabra_clave in palabras_clave_normalizadas:

                    if palabra_clave in verso_sin_punt:
                        coincidencia = True

                if (
                    coincidencia
                    and verso.strip() not in versos_encontrados
                    and verso.strip() != ""
                ):
                    versos_encontrados.append(
                        verso.strip()
                    )

    total_versos_necesarios = (
        num_parrafos * num_versos
    )

    if len(versos_encontrados) == 0:

        return (
            "[Aviso] No se encontraron versos "
            "con esas palabras clave."
        )

    for _ in range(5):
        random.shuffle(versos_encontrados)

    while len(versos_encontrados) < total_versos_necesarios:

        versos_encontrados.append(
            random.choice(versos_encontrados)
        )

    versos_encontrados = versos_encontrados[
        :total_versos_necesarios
    ]

    poema_final = ""

    indice = 0

    for p in range(num_parrafos):

        for v in range(num_versos):

            verso_norm = normalizar_verso(
                versos_encontrados[indice]
            )

            poema_final += verso_norm + "\n"

            indice += 1

        if p < num_parrafos - 1:
            poema_final += "\n"

    return poema_final