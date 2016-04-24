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
  classes: '',

  getInitialState: function () {
    return {
      editMode: false,
      isSaving: false,
      hasError: false
    }
  },
  componentWillMount: function () {
    this._setDefaultProps()
  },
  _setDefaultProps: function () {
    this.isBool = this.props.field.schema.data_format === 'bool'
    this.display_value = this.props.field.schema.data_format === 'bool' ? this.props.value : format.autoFormat(this.props.value, this.props.field.schema.data_format, 2)
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

  _shouldUpdateCell: function (event) {
    let displayValue = event.target.value
    if (this.props.field.schema.data_format === 'pct') {
      const pctIndex = event.target.value.indexOf('%')
      displayValue = pctIndex === -1 ? event.target.value : event.target.value.slice(0, pctIndex)
      displayValue = format.autoFormat(displayValue / 100, this.props.field.schema.data_format, 2)
      event.target.value = event.target.value === '' ? '' : event.target.value / 100
    }
    return displayValue !== this.display_value
  },

  _deleteValue: function (computed_id, query_params, new_value) {
    // this path does not delete. modified to simply update the value with null
    // all commented lines are for 'delete' route
    ComputedDatapointAPI.deleteComputedDataPoint(computed_id)
    // this._queryDatapoint(query_params, new_value)
    this.display_value = this.isBool ? '2' : ''
    this.setState({isSaving: false, editMode: false, hasError: false })
  },
  _getQueryParams: function (new_value) {
    return {
      location_id: this.props.row.location_id,
      campaign_id: this.props.row.campaign_id.id,
      indicator_id: this.props.field.key,
      computed_id: this.props.row[this.props.field.key].computed,
      value: new_value
    }
  },
  _queryDatapoint: function (query_params, new_value) {
    let api_response = {}
    if (query_params.computed_id) {
      api_response = ComputedDatapointAPI.putComputedDatapoint(query_params)
    } else {
      api_response = ComputedDatapointAPI.postComputedDatapoint(query_params)
    }
    api_response.then(response => {
      this.props.row[this.props.field.key].computed = response.objects.id
      this.props.value = response.objects.value
      if ((this.isBool && new_value === '2') || (new_value === '')) {
        // for 'null'
        this.display_value = this.isBool ? '2' : ''
      } else {
        // for any other value
        this.display_value = this.isBool ? new_value : format.autoFormat(new_value, this.props.field.schema.data_format, 2)
      }
      if (!this.isBool) {
        this.setState({editMode: false, isSaving: false, hasError: false})
      } else {
        this.setState({isSaving: false, hasError: false})
      }
    }, reject => {
      this.display_value = this.isBool ? new_value : format.autoFormat(new_value, this.props.field.schema.data_format, 2)
      if (!this.isBool) {
        this.setState({editMode: false, isSaving: false, hasError: true})
      } else {
        this.setState({isSaving: false, hasError: true})
      }
    })
  },

  updateCellValue: function (new_value) {
    let cleaned_value = new_value.replace(',', '')

    const isEmpty = this.isBool ? cleaned_value === '2' : cleaned_value === ''
    let computed_id = this.props.row[this.props.field.key].computed
    if (isEmpty && computed_id) {
      let query_params = this._getQueryParams(null)
      this._deleteValue(computed_id, query_params, cleaned_value)
    } else if (isNaN(cleaned_value)) {
      this.setState({ editMode: false, hasError: true })
    } else {
      this.setState({isSaving: true})
      let query_params = this._getQueryParams(cleaned_value)
      this._queryDatapoint(query_params, cleaned_value)
    }
    this.forceUpdate()
  },

  _setClasses: function () {
    let display_value
    if (this.isBool) {
      if (this.display_value === '2' || this.display_value === '') {
        display_value = ''
      }
    } else {
      display_value = this.display_value
    }
    this.classes = (this.props.classes + ' editable ' +
    (this.state.editMode ? 'in-edit-mode ' : '') +
    (this.state.isSaving ? 'saving ' : '') +
    (this.state.hasError ? 'error ' : '') +
    (display_value === '' ? 'missing ' : ''))
  },
  _getBooleanComponent: function () {
    const boolean_options = [
      { 'value': '0', 'title': 'No' },
      { 'value': '1', 'title': 'Yes' },
      { 'value': '', 'title': 'No Data' }
    ]
    const selected_item = boolean_options[this.display_value]
    return (
    <td className={'editable ' + this.classes}>
      <DropdownMenu
        items={boolean_options}
        sendValue={this.updateCellValue}
        text={selected_item ? selected_item.title : ''}
        onChange={this.updateCellValue}
        style='boolean-dropdown'
        searchable={false} />
    </td>
    )
  },
  _getTableCellComponent: function () {
    const input_field = (
    <input
      placeholder={this.display_value}
      onBlur={this.exitEditMode}
      onKeyUp={this.exitEditMode}
      id={this.cell_id}
      type='text' />
    )
    return (
    <TableCell
      field={this.props.field}
      row={this.props.row}
      value={this.display_value}
      classes={this.classes}
      onClick={!this.state.editMode ? this.enterEditMode : null}
      hideValue={this.state.editMode || this.state.isSaving || this.display_value === ''}>
      {this.state.isSaving ? <i className='fa fa-spinner fa-spin saving-icon'></i> : null}
      {this.state.editMode ? input_field : null}
    </TableCell>
    )
  },

  render: function () {
    this._setClasses()
    if (this.isBool) {
      return this._getBooleanComponent()
    } else {
      return this._getTableCellComponent()
    }
  }
})

export default EditableTableCell
