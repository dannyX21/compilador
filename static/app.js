const vm = new Vue({
  el: "#app",
  delimiters: ['<%', '%>'],
  data: {
    codigo: '',
    tokens: [],
    errores: [],
    tablaSimbolos: [],
    resultadoExpresion: false,
    resultadoPrograma: false,
    columnas: [
      {
        field: 'id',
        label: '#',
        centered: true
      },
      {
        field: 'token',
        label: 'Token',
        centered: true
      },
      {
        field: 'codigo',
        label: 'Codigo',
        centered: true
      },
      {
        field: 'lexema',
        label: 'Lexema',
        centered: true
      }
      {
        field: 'tipo',
        label: 'Tipo',
        centered: true
      }
    ],
    activeTab: 0
  },
  computed: {
    expresionValida() {
      return this.resultadoExpresion && this.errores.length === 0
    },
    programaValido() {
      return this.resultadoPrograma && this.errores.length === 0
    }
  },
  methods: {
    compila: _.debounce(function() {
      axios.post('/compila/', { codigo: this.codigo }, ).then((response) => {
        this.tokens = response.data.componentes_lexicos.map(function(componente, indice) {
          componente['id'] = indice + 1
          return componente
        })
        this.tablaSimbolos = response.data.tabla_de_simbolos.map(function(simbolo, indice) {
          simbolo['id'] = indice + 1
          return simbolo
        })
        this.errores = response.data.errores.map(function(error, indice) {
          error['id'] = indice + 1
          return error
        })
      })
    }, 500),
    compilaExpresion: _.debounce(function() {
      axios.post('/compila-expresion/', { codigo: this.codigo }, ).then((response) => {
        this.resultadoExpresion = response.data.expresion
        this.errores = response.data.errores.map(function(error, indice) {
          error['id'] = indice + 1
          return error
        })
      })
    }, 500),
    compilaPrograma: _.debounce(function() {
      axios.post('/compila-sintactico/', { codigo: this.codigo }, ).then((response) => {
        this.resultadoPrograma = response.data.programa
        this.tablaSimbolos = response.data.tabla_de_simbolos.map(function(simbolo, indice) {
          simbolo['id'] = indice + 1
          return simbolo
        })
        this.errores = response.data.errores.map(function(error, indice) {
          error['id'] = indice + 1
          return error
        })
      })
    }, 500)
  },
  mount() {
    this.$refs.codigoInput.input.focus()
  }
})
