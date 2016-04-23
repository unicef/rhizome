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

  onSetDefaultData: function (currentState) {
    _.merge(this.data, currentState)
    this.trigger(this.data)
  },

  onFocusInput: function (cell_id, value) {
    setTimeout(() => {
      let element = document.getElementById(cell_id)
      element.value = value
      element.focus()
      element.select()
    }, 10)
  },
  onGetBooleanComponent () {

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
