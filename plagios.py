import os
SIGNOS = ",.¡¿!?!¡?¿+-_)[¡¿?!¡¿'"

def palabras_sin_signos(texto):
    """Elimina los signos de puntuación de un texto y los hago minusculas"""
    palabras_limpias = []
    for palabra in texto.split():
        palabra_sin_signos = ""
        for caracter in palabra.lower():
            if caracter not in SIGNOS:
                palabra_sin_signos += caracter
        palabras_limpias.append(palabra_sin_signos)
    return " ".join(palabras_limpias)


def ngramas_archivo(archivo, N):
    """Calcula los ngramas de un archivo"""
    ngramas = {}
    ngramas_actuales = []
    for linea in archivo:
        palabras = palabras_sin_signos(linea).split()
        for palabra in palabras:
            ngramas_actuales.append(palabra)
            if len(ngramas_actuales) > N:
                ngramas_actuales.pop(0)
            if len(ngramas_actuales) == N:
                n_grama = tuple(ngramas_actuales)
                if n_grama in ngramas:
                    ngramas[n_grama] += 1
                else:
                    ngramas[n_grama] = 1
    return ngramas


def leer_archivos(directorio, N):
    """Lee los archivos del directorio que se le pasa y calcula los ngramas"""
    archivos = {}
    for archivo in os.listdir(directorio):
        ruta_archivo = os.path.join(directorio, archivo)
        with open(ruta_archivo, "r") as txt:
            ngramas = ngramas_archivo(txt, N)
            archivos[archivo] = ngramas
    return archivos


def jaccard(ngramas1, ngramas2):
    """Calcula la similitud de Jaccard entre dos conjuntos de ngramas"""
    interseccion = 0
    union = sum(ngramas1.values()) + sum(ngramas2.values())
    for ngrama, cantidad1 in ngramas1.items():
        if ngrama in ngramas2:
            cantidad2 = ngramas2[ngrama]
            interseccion += cantidad1 + cantidad2
    return interseccion / union


def pedir_directorio():
    while True:
        directorio = input("Ingrese el directorio a escanear (o deje vacío para salir): ")
        if directorio == "":
            print("Saliendo del programa...")
            return None
        try:
            os.listdir(directorio)
            return directorio
        except FileNotFoundError:
            print("El directorio ingresado no existe")
        except NotADirectoryError:
            print("La ruta ingresada no es un directorio")


def tamaño_ngramas():
    ngramas = None
    while ngramas is None:
        try:
            ngramas = int(input("Ingrese el tamaño de los ngramas (entre 2 y 10 ): "))
            if ngramas < 2 or ngramas >= 10:
                print("Ingrese un número entre 2 y 9")
                ngramas = None
        except ValueError:
            print("Ingrese un número entero")
    return ngramas


def similitud(archivos, ngramas):
    resultados_sospechosos = []
    resultados_comunes = []
    for i, (archivo1, ngramas1) in enumerate(archivos.items()):
        for archivo2, ngramas2 in list(archivos.items())[i + 1:]:
            similitud = jaccard(ngramas1, ngramas2)
            if similitud >= 0.15:
                resultados_sospechosos.append((archivo1, archivo2, similitud * 100))
            if similitud >= 0.01:
                resultados_comunes.append((archivo1, archivo2, similitud * 100))
    return resultados_sospechosos, resultados_comunes


def guardar_resultados(resultados_sospechosos, resultados_comunes):
    """Imprime los resultados de los archivos que tienen ngramas en común y los que tienen similitud sospechosa y los guarda en un archivo si se quiere"""
    print("Resultados sospechosos:")
    for resultado in resultados_sospechosos:
        archivo_1, archivo_2, similitud = resultado
        print(f"{resultado[0]} vs {resultado[1]} ({resultado[2]}%)")

    guardar_archivo = input("Ingrese el nombre del archivo para guardar el reporte: ")
    if guardar_archivo == "":
        print("No se guardará el reporte")
    else:
        try:
            with open(guardar_archivo, "w") as similaridades:
                similaridades.write("Archivo 1, Archivo 2, Similaridad\n")
                for archivo_1, archivo_2, similitud in resultados_comunes:
                    similaridades.write(f"{archivo_1}, {archivo_2}, ({similitud}%)\n")
        except FileNotFoundError:
            print(f"Error: La ruta {guardar_archivo} no existe.")


def main():
    while True:
        directorio = pedir_directorio()
        if directorio is None:
            break

        ngramas = tamaño_ngramas()

        archivos_ngramas = leer_archivos(directorio, ngramas)

        resultados_sospechosos, resultados_comunes = similitud(archivos_ngramas, ngramas)

        guardar_resultados(resultados_sospechosos, resultados_comunes)

main()