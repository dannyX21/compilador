from compilador.sintactico import Sintactico
codigo = input('Ingresa una expresion: ')
sin = Sintactico(codigo=codigo)

if sin.EXPRESION() and len(sin.errores.coleccion) == 0:
    print('La Expresion es valida!')

else:
    print('La Expresion es invalida!')
    for error in sin.errores.coleccion:
        print(error)