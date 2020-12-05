from compilador.sintactico import Sintactico
codigo = input('Ingresa una expresion: ')
sin = Sintactico(codigo=codigo)

if sin.PROGRAMA() and len(sin.errores.coleccion) == 0:
    print('Programa valido')

else:
    print('Programa invalido')
    for error in sin.errores.coleccion:
        print(error)