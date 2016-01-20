import Reflux from 'reflux'

var CellStore = Reflux.createStore({
  listenables: [require('actions/CellActions')],

  data: {
    previousValue: null, // save the previous value to compare with edited value
    isSaving: false, // whether the cell is in the process of saving right now
    isEditable: false, // whether the cell is editable
    isEditing: false, // whether the cell is currently being edited
    hasError: false
  },

  getInitialState: function () {
    return this.data
  },

  onToggleEditing: function (orgIsEditable) {
    if (orgIsEditable === true) {
      this.data.isEditing = true !== 'undefined' ? true : !this.data.isEditing
      this.trigger(this.data)
    }
  },

  onSubmit: function () {
    this.data.isEditing = false
    this.trigger(this.data)
  }
})

export default CellStore
