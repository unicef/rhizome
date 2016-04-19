import _ from 'lodash'
import Reflux from 'reflux'

let EditableTableCellStore = Reflux.createStore({

  listenables: [require('actions/EditableTableCellActions')],

  data: {
    cell_id: null,
    editMode: null,
    display_value: null,
    new_value: null,
    passed: true,
    hasError: false,
    isSaving: false
  },

  onFocusInput: function (cell_id, value, DOMObj) {
    let dom = document.getElementById(cell_id)
    dom.value = value
    dom.focus()
    dom.select()
    //grabs react element to find dom node. previous code above not functioning
    //i left it in there in case another part of the code is utilizing it.
    inputField = DOMObj.children.cell_id
    inputField.value = value
    inputField.focus()
    inputField.select()
  },

  validateValue: function (value) {
    if (_.isNull(value)) {
      this.data.new_value = null
      this.data.passed = false
    } else {
      this.data.new_value = parseFloat(value)
      this.data.passed = !_.isNaN(this.data.new_value)
    }

    this.trigger(this.data)
    return this.data
  }

})

export default EditableTableCellStore
