
def tabla_de_simbolos(*args, **kwargs):
    lexico = Lexico()
    simbolos = [{'token': s.token, 'lexema': s.lexema} for s in lexico.tabla_de_simbolos]
    simbolos = [{'token': s.token, 'lexema': s.lexema, 'tipo': s.tipo} for s in lexico.tabla_de_simbolos]
    return ({'simbolos': simbolos}, 200)
('/compila/', methods=('post',))
def compila(*args, **kwargs):
                {
                    "token": componente_lexico.token,
                    "lexema": componente_lexico.lexema,
                    "codigo": componente_lexico.codigo
                    "codigo": componente_lexico.codigo,
                    "tipo": componente_lexico.tipo
                }
            )

def compila(*args, **kwargs):
    resultado['tabla_de_simbolos'] = [{
        'token': s.token,
        'lexema': s.lexema,
        'codigo': s.codigo
        'codigo': s.codigo,
        'tipo': s.tipo
    } for s in lexico.tabla_de_simbolos]
    return (resultado, 200)

def compila_sintactico(*args, **kwargs):
    resultado['tabla_de_simbolos'] = [{
        'token': s.token,
        'lexema': s.lexema,
        'codigo': s.codigo
        'codigo': s.codigo,
        'tipo': s.tipo
    } for s in sintactico.lexico.tabla_de_simbolos]
    resultado['errores'] = [
        {
def compila_sintactico(*args, **kwargs):
    return (resultado, 200)

if __name__ == '__main__':
    app.run(debug=True) 
    app.run(debug=True)
