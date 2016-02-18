import _ from 'lodash'
import api from 'data/api'
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
  },

  // Cant figure out a way to get location_id and campaign_id to this function
  onSaveCellValue: function (value, cell_key) {
    let upsert_options = {
      location_id: 2, // hard coded for now
      campaign_id: 307, // parseInt(campaignId, 10),
      indicator_id: cell_key,
      value: value
    }
    return api.datapointUpsert(upsert_options)
  }
})

export default EditableTableCellStore
