import json
from flask import Flask, render_template, request, jsonify
from compilador.lexico import Lexico
from compilador.errores import ColeccionError
from compilador.sintactico import Sintactico

app = Flask(__name__)

@app.route('/')
def index(methods=('get',)):
    return render_template('index.html')

@app.route('/expresion/')
def expresion(methods=('get',)):
    return render_template('expresion.html')

@app.route('/tabla-de-simbolos/')
def tabla_de_simbolos(*args, **kwargs):
    lexico = Lexico()
    simbolos = [{'token': s.token, 'lexema': s.lexema} for s in lexico.tabla_de_simbolos]
    return ({'simbolos': simbolos}, 200)

@app.route('/compila/', methods=('post',))
def compila(*args, **kwargs):
    json_data = json.loads(request.data)
    errores = ColeccionError()
    lexico = Lexico(codigo=json_data.get('codigo', ''), errores=errores)
    componentes_lexicos = []
    while True:
        componente_lexico = lexico.siguiente_componente_lexico()
        if componente_lexico:
            componentes_lexicos.append(
                {
                    "token": componente_lexico.token,
                    "lexema": componente_lexico.lexema,
                }
            )

        else:
            break

    resultado = {'componentes_lexicos': componentes_lexicos}
    resultado['errores'] = [
        {
            'tipo': e.tipo,
            'num_linea': e.num_linea,
            'mensaje': e.mensaje
        } for e in lexico.errores
    ]

    return (resultado, 200)

@app.route('/compila-expresion/', methods=('post',))
def compila_expresion(*args, **kwargs):
    json_data = json.loads(request.data)
    sintactico = Sintactico(codigo=json_data.get('codigo', ''))
    expresion = sintactico.EXPRESION()
    resultado = {'expresion': expresion }
    resultado['errores'] = [
        {
            'tipo': error.tipo,
            'num_linea': error.num_linea,
            'mensaje': error.mensaje
        } for error in sintactico.errores.coleccion
    ]
    
    return (resultado, 200)

if __name__ == '__main__':
    app.run(debug=True)