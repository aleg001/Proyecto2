# Librerías para el título
import time
import sys
import RayOptions as RTO

# Funciones para el menu:
def Opciones():
    menuOp = input("1) Proyecto 2 \n2) Salir\n")
    menuVer = verificarNum(menuOp)
    return menuVer


def verificarNum(input):
    try:
        val = float(input)
        return val
    except ValueError:
        try:
            val = int(input)
            return val
        except ValueError:
            print("¡Solamente números!")


# Mensaje de despedida
def bye():
    print("¡Gracias por usar el programa!!")


Bienvenida = "\n----- RT Library----\n"
procesando = "Procesando solicitud..."


def ImpresionTitulo(string):
    # Se imprime el título con efecto de typewriter
    for i in string:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.02)


ImpresionTitulo(Bienvenida)


menu = False
# menu = True
while menu == False:
    opcion = Opciones()
    if opcion == 1:
        tituloArchivo = input(
            "Ingrese el nombre para el archivo (NO incluir extension .bpm): "
        )
        tituloArchivo = tituloArchivo + ".bmp"
        RTO.run(tituloArchivo)
        ImpresionTitulo(procesando)

        print("\n\n¡Imagen generada!\n")

    if opcion == 2:
        print("Gracias por utilizar este programa.")
        print("\n")
        menu = True
