import Reflux from 'reflux'

var CellStore = Reflux.createStore({
  listenables: [require('actions/CellActions')],

  data: {
  },

  getInitialState: function () {
    return this.data
  },

  onFocusInput: function (cellId) {
    document.getElementById(cellId).focus()
  }
})

export default CellStore
