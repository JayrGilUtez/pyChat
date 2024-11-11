def cifrado_cesar(key, message):
    
    alfabeto = "abcdefghijklmnopqrstuvwxyz"
    

    # palabra = input("Introduce la palabra a cifrar: ")
    # clave = int(input("Introduce la clave de cifrado: "))

    palabra = message
    clave = key

    palabra_cifrada = ""
    for letra in palabra:

        indice_actual = alfabeto.index(letra)

        nuevo_indice = (indice_actual + clave) % 26

        palabra_cifrada += alfabeto[nuevo_indice]


    print("Palabra original:", palabra)
    print("Palabra cifrada:", palabra_cifrada)

cifrado_cesar(3,"hola")