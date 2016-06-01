import React from 'react'
import Reflux from 'reflux'
import format from 'utilities/format'

import randomHash from 'utilities/randomHash'
import TableCell from 'components/organisms/datascope/TableCell'

import EditableTableCellStore from 'stores/EditableTableCellStore'
import EditableTableCellActions from 'actions/EditableTableCellActions'
import DataEntryActions from 'actions/DataEntryActions'
import DropdownButton from 'components/button/DropdownButton'

import api from 'utilities/api'

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
  computed_id: null,

  getInitialState: function () {
    return {
      editMode: false,
      isSaving: false,
      hasError: false,
    }
  },

  componentWillMount: function () {
    this._initComponentValues()
  },

  _initComponentValues: function () {
    this.computed_id = this.props.row[this.props.field.key].computed
    this.isBool = this.props.field.schema.data_format === 'bool'
    this.display_value = this.isBool ? this.props.value : format.autoFormat(this.props.value, this.props.field.schema.data_format, 2)
  },

  enterEditMode: function (event) {
    this.setState({ editMode: true })
    EditableTableCellActions.focusInput(this.cell_id, this.display_value)
  },

  exitEditMode: function (event) {
    if (event.type === 'blur' || event.keyCode === 13) { // Keycode for 'Enter' key
      let cleaned_value = this._cleanValue(event.target.value)
      if (this._shouldQuery(cleaned_value)) {
        this.updateCellValue(cleaned_value)
      }
      if (!this.isBool) { this.setState({ editMode: false }) }
    }
  },

  _cleanValue: function(value) {
    let cleaned_value = value.replace(',', '')
    if (cleaned_value.indexOf('%') !== -1 || this.props.field.schema.data_format === 'pct') {
      cleaned_value = cleaned_value.replace('%', '')
      cleaned_value = cleaned_value === '' ? cleaned_value : cleaned_value / 100.00
    }
    return cleaned_value
  },

  _shouldQuery: function (value) {
    let formattedValue = ''
    if (value !== '') {
      formattedValue = this.isBool ? value : format.autoFormat(value, this.props.field.schema.data_format, 2)
    }
    return formattedValue !== this.display_value
  },

  _deleteValue: function (query_params, new_value) {
    DataEntryActions.deleteDatapoint(this.computed_id)
    this.computed_id = null
    this.display_value = ''
    this.setState({ isSaving: false, editMode: false, hasError: false })
  },

  _getQueryParams: function (new_value) {
    return {
      location_id: this.props.row.location_id,
      campaign_id: this.props.row.campaign_id,
      indicator_id: this.props.field.key,
      computed_id: this.computed_id,
      value: new_value
    }
  },

  putComputedDatapoint: function (options) {
    let fetch = api.endPoint('/computed_datapoint/' + options.computed_id, 'PATCH', 1)
    return new Promise(function (fulfill, reject) {
      fetch({value: options.value}, null, {'cache-control': 'no-cache'}).then(function (response) {
        fulfill(response)
      }, reject)
    })
  },

  postComputedDatapoint: function (options) {
    delete options['computed_id']
    let fetch = api.endPoint('/computed_datapoint/', 'POST', 1)
    return new Promise(function (fulfill, reject) {
      fetch(options, null, {'cache-control': 'no-cache'}).then(function (response) {
        fulfill(response)
      }, reject)
    })
  },

  _queryDatapoint: function (query_params, new_value) {
    let api_response = {}
    if (this.computed_id) {
      api_response = this.putComputedDatapoint(query_params)
    } else {
      api_response = this.postComputedDatapoint(query_params)
    }
    api_response.then(response => {
      this.computed_id = response.objects.id
      this.display_value = this.isBool ? new_value : format.autoFormat(new_value, this.props.field.schema.data_format, 2)
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
    const isEmpty = new_value === ''

    if (isEmpty && this.computed_id) {
      let query_params = this._getQueryParams(null)
      this._deleteValue(query_params, new_value)
    } else if (isNaN(new_value)) { //validation in case user inputs symbols, good to have even if back end has validations
      this.setState({ editMode: false, hasError: true })
    } else {
      this.setState({isSaving: true})
      let query_params = this._getQueryParams(new_value)
      this._queryDatapoint(query_params, new_value)
    }
    this.forceUpdate()
  },

  _setClasses: function () {
    this.classes = (this.props.classes + ' editable ' +
                   (this.state.editMode ? 'in-edit-mode ' : '') +
                   (this.state.isSaving ? 'saving ' : '') +
                   (this.state.hasError ? 'error ' : '') +
                   ((this.display_value === '') ? 'missing ' : ''))
  },

  _getBooleanComponent: function () {
    const boolean_options = [
      { 'value': '0', 'title': 'No' },
      { 'value': '1', 'title': 'Yes' },
      { 'value': '', 'title': 'No Data' }
    ]
    const index = this.display_value === '' ? 2 : this.display_value
    const selected_item = boolean_options[index]
    return (
      <td className={'editable ' + this.classes}>
        <DropdownButton
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
