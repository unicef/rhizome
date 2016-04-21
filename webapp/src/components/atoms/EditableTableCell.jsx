import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import format from 'utilities/format'

import randomHash from 'utilities/randomHash'
import TableCell from 'components/atoms/TableCell'

import EditableTableCellStore from 'stores/EditableTableCellStore'
import EditableTableCellActions from 'actions/EditableTableCellActions'
import ComputedDatapointAPI from 'data/requests/ComputedDatapointAPI'
import DropdownMenu from 'components/molecules/menus/DropdownMenu'

let EditableTableCell = React.createClass({
  mixins: [Reflux.connect(EditableTableCellStore)],

  propTypes: {
    key: React.PropTypes.string,
    field: React.PropTypes.object,
    row: React.PropTypes.object,
    value: React.PropTypes.string,
    formatValue: React.PropTypes.func,
    validateValue: React.PropTypes.func,
    isSaving: React.PropTypes.bool,
    onSave: React.PropTypes.func,
    tooltip: React.PropTypes.string,
    classes: React.PropTypes.string
  },

  isBool: false,
  cell_id: 'edit_id_' + randomHash(),
  display_value: null,
  tooltip: null,

  componentWillMount: function () {
    this.isBool = this.props.field.schema.data_format === 'bool'
    this.display_value = this.isBool ? this.props.value : format.autoFormat(this.props.value, this.props.field.schema.data_format, 2)
  },

  enterEditMode: function (event) {
    this.setState({ editMode: true })
    EditableTableCellActions.focusInput(this.cell_id, this.display_value)
  },

  exitEditMode: function (event) {
    if (event.type === 'blur' || event.keyCode === 13) { // Keycode for 'Enter' key
      if (this._shouldUpdateCell(event)) {
        this.updateCellValue(event.target.value)
      }
      this.setState({editMode: false})
    }
  },

  _shouldUpdateCell: function(event){
    let displayValue = event.target.value
    if (this.props.field.schema.data_format === 'pct') {
      const pctIndex = event.target.value.indexOf('%')
      displayValue = pctIndex === -1 ? event.target.value : event.target.value.slice(0, pctIndex)
      displayValue = format.autoFormat(displayValue/100, this.props.field.schema.data_format, 2)
      event.target.value = event.target.value/100
    }
    return displayValue !== this.display_value
  },

  updateCellValue: function (new_value) {
    let validation = EditableTableCellActions.validateValue(new_value)
    let computed_id = this.props.row[this.props.field.key].computed
    if (new_value === '' && computed_id) { // this is the delete //
      ComputedDatapointAPI.deleteComputedDataPoint(computed_id)
      this.display_value = ''
      this.setState({ editMode: false, hasError: false })
    }
    if (!validation) {
      this.setState({ editMode: false, hasError: true })
    } else {
      this.isSaving = true
      let query_params = {
        location_id: this.props.row.location_id,
        campaign_id: this.props.row.campaign_id.id,
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
        this.props.row[this.props.field.key].computed = response.objects.id
        this.props.value = response.objects.value
        this.isSaving = false
        this.hasError = false
        if (!this.isBool) { this.setState({editMode: false}) }
      }, reject => {
        this.isSaving = false
        this.hasError = true
        if (!this.isBool) { this.setState({editMode: false}) }
      })
    }
    this.display_value = this.isBool ? new_value : format.autoFormat(new_value, this.props.field.schema.data_format, 2)

    this.forceUpdate()
  },

  render: function () {
    let classes = this.props.classes + ' editable '
    classes += this.state.editMode ? ' in-edit-mode' : ''
    classes += this.isSaving ? ' saving ' : ''
    classes += this.hasError ? ' error ' : ''
    classes += this.display_value === '' ? ' missing ' : ''

    if (this.isBool) {
      const boolean_options = [
        { 'value': '0', 'title': 'No' },
        { 'value': '1', 'title': 'Yes' },
        { 'value': '', 'title': 'No Data' }
      ]
      const selected_item = boolean_options[this.display_value]
      return (
        <td className={'editable' + classes}>
          <DropdownMenu
            items={boolean_options}
            sendValue={this.updateCellValue}
            text={selected_item ? selected_item.title : ''}
            onChange={this.updateCellValue}
            style='boolean-dropdown'
            searchable={false}
          />
        </td>
      )
    } else {
      const input_field = (
        <input placeholder={this.display_value}
          onBlur={this.exitEditMode}
          onKeyUp={this.exitEditMode}
          id={this.cell_id}
          type='text'/>
      )
      return (
        <TableCell
          field={this.props.field}
          row={this.props.row}
          value={this.display_value}
          classes={classes}
          onClick={!this.state.editMode ? this.enterEditMode : null}
          hideValue={this.state.editMode || this.isSaving}>
          {this.isSaving ? <i className='fa fa-spinner fa-spin saving-icon'></i> : null}
          {this.state.editMode ? input_field : null}
        </TableCell>
      )
    }
  }
})

export default EditableTableCell
