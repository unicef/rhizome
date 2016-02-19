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
  tooltip: null,

  componentWillMount() {
    this.display_value = this.props.value
    this.tooltip = this.props.tooltip.value !==  '' ? this.props.tooltip.value : 'No value'
  },

  enterEditMode: function (event) {
    this.setState({ editMode: true })
    EditableTableCellActions.focusInput(this.cell_id, this.props.value)
  },

  exitEditMode: function (event) {
    if (event.type === 'blur' || event.keyCode === 13 ) { // Keycode for 'Enter' key
      if (event.target.value !== this.display_value ) {
        this.updateCellValue(event.target.value)
      }
      this.setState({editMode: false})
    }
  },

  updateCellValue: function (new_value) {
    let validation = EditableTableCellActions.validateValue(new_value)
    if (!validation) {
      this.setState({ editMode: false, hasError: true })
    } else {
      this.isSaving = true
      let query_params = {
        location_id: this.props.row.location_id,
        campaign_id: this.props.row.campaign_id,
        indicator_id: this.props.field.key,
        computed_id: this.props.row[this.props.field.key].computed,
        value: new_value
      }
      let api_response = {}
      if (query_params.computed_id) {
        api_response = ComputedDatapointAPI.putComputedDatapoint(query_params)
      } else {
        api_response = ComputedDatapointAPI.postComputedDatapoint(query_params)
      }
      api_response.then(response => {
        console.log('response',response)
        this.props.row[this.props.field.key].computed = response.objects.id
        this.props.value = response.objects.value
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
    this.display_value = new_value
  },

  render: function () {
    let classes = this.props.classes + ' editable '
    classes += this.state.editMode ? ' in-edit-mode' : ''
    classes += this.isSaving ? ' saving ' : ''
    classes += this.hasError ? ' error ' : ''
    classes += this.display_value === '' ? ' missing ' : ''

    let hideValue = this.state.editMode || this.isSaving
    let input_field = ''
    let spinner = ''

    if (this.state.editMode) {
      input_field = <input type='text' onBlur={this.exitEditMode} onKeyUp={this.exitEditMode} id={this.cell_id}/>
    }

    if (this.isSaving)
      spinner = <i className='fa fa-spinner fa-spin saving-icon'></i>

    return (
      <TableCell
        field={this.props.field}
        row={this.props.row}
        value={this.display_value}
        formatValue={this.props.formatValue}
        tooltip={this.tooltip}
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
