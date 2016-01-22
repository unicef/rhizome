import Reflux from 'reflux'

var CellStore = Reflux.createStore({
  listenables: [require('actions/CellActions')],

  data: {
  },

  getInitialState: function () {
    return this.data
  },

  onFocusInput: function (cellId, value) {
    let dom = document.getElementById(cellId)
    dom.value = value
    dom.focus()
    dom.select()
  }
})

export default CellStore
