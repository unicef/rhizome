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

  onFocusInput: function (cell_id, value) {
    let dom = document.getElementById(cell_id)
    dom.value = value
    dom.focus()
    dom.select()
  },

  onValidateValue: function (value) {
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
