const vm = new Vue({
  el: "#app",
  delimiters: ['<%', '%>'],
  data: {
    codigo: '',
    tokens: [],
    errores: [],
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
        field: 'lexema',
        label: 'Lexema',
        centered: true
      }
    ]
  },
  methods: {
    compila: _.debounce(function() {
      axios.post('/compila/', { codigo: this.codigo }, ).then((response) => {
        this.tokens = response.data.componentes_lexicos.map(function(componente, indice) {
          componente['id'] = indice + 1
          return componente
        })
        this.errores = response.data.errores.map(function(error, indice) {
          error['id'] = indice + 1
          return error
        })
      })
    }, 500)
  }
})