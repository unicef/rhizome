import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import randomHash from '00-utilities/randomHash'
import TableCell from '01-atoms/TableCell'

import EditableTableCellStore from 'stores/EditableTableCellStore'
import EditableTableCellActions from 'actions/EditableTableCellActions'
import ComputedDatapointAPI from 'data/requests/ComputedDatapointAPI'

let EditableTableCell = React.createClass({

  mixins: [Reflux.connect(EditableTableCellStore)],

  propTypes: {
    key: React.PropTypes.string,
    fields: React.PropTypes.object,
    value: React.PropTypes.string,
    formatValue: React.PropTypes.func,
    validateValue: React.PropTypes.func,
    isSaving: React.PropTypes.bool,
    onSave: React.PropTypes.func,
    tooltip: React.PropTypes.string,
    classes: React.PropTypes.string
  },

  cell_id: 'edit_id_' + randomHash(),
  display_value: null,

  componentWillMount() {
    this.display_value = this.props.value
  },

  enterEditMode: function (event) {
    this.setState({ editMode: true })
    EditableTableCellActions.focusInput(this.cell_id, this.props.value)
  },

  updateCell: function (event) {
    if (event.type === 'blur' || event.keyCode === 13 ) { // Keycode for 'Enter' key
      let validation = EditableTableCellActions.validateValue(event.target.value)
      if (!validation) {
        this.setState({ editMode: false, hasError: true })
      } else {
        this.isSaving = true
        let query_params = {
          location_id: this.props.row.location_id,
          campaign_id: this.props.row.campaign_id,
          indicator_id: this.props.field.key,
          computed_id: this.props.row[this.props.field.key].computed,
          value: event.target.value
        }
        let api_response = {}
        if (query_params.computed_id) {
          api_response = ComputedDatapointAPI.putComputedDatapoint(query_params)
        } else {
          api_response = ComputedDatapointAPI.postComputedDatapoint(query_params)
        }
        api_response.then(response => {
          console.log('response',response)
          this.display_value = query_params.value
          this.isSaving = false
          this.hasError = false
          this.setState({editMode: false})
        }, reject => {
          console.log('reject',reject)
          this.display_value = query_params.value
          this.isSaving = false
          this.hasError = true
          this.setState({editMode: false})
        })
      }
      this.display_value = event.target.value
    }
  },


  render: function () {
    let classes = this.props.classes + ' editable'
    classes += this.state.editMode ? ' editing ' : ''
    classes += this.isSaving ? ' saving ' : ''
    classes += this.hasError ? ' error ' : ''
    // classes += this.state.missing() ? 'missing ' : ''

    let hideValue = this.state.editMode || this.isSaving
    let input_field = ''
    let spinner = ''

    if (this.state.editMode) {
      classes += ' in-edit-mode'
      input_field = <input type='text' onBlur={this.updateCell} onKeyUp={this.updateCell} id={this.cell_id}/>
    }

    if (this.isSaving)
      spinner = <i className='fa fa-spinner fa-spin saving-icon'></i>

    return (
      <TableCell
        field={this.props.field}
        row={this.props.row}
        value={this.display_value}
        formatValue={this.props.formatValue}
        tooltip={this.props.tooltip}
        classes={classes}
        onClick={this.enterEditMode}
        hideValue={hideValue}>
          { spinner }
          { input_field }
      </TableCell>
    )
  }
})

export default EditableTableCell
