def leer_csv(ruta_archivo, separador=",", comillas='"', encoding="utf-8"):
    """
    Lee un archivo CSV y devuelve una lista de listas.
    """

    datos = []

    with open(ruta_archivo, "r", encoding=encoding) as f:
        contenido = f.read()

    fila_actual = []
    campo_actual = ""
    dentro_comillas = False

    i = 0

    while i < len(contenido):
        char = contenido[i]

        if char == comillas:
            dentro_comillas = not dentro_comillas

        elif char == separador and not dentro_comillas:
            fila_actual.append(campo_actual)
            campo_actual = ""

        elif char == "\n" and not dentro_comillas:
            fila_actual.append(campo_actual)
            datos.append(fila_actual)

            fila_actual = []
            campo_actual = ""

        else:
            campo_actual += char

        i += 1

    if campo_actual or fila_actual:
        fila_actual.append(campo_actual)
        datos.append(fila_actual)

    return datos