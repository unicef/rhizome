import React from 'react'
import Reflux from 'reflux'

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

  componentWillMount () {
    this.display_value = this.props.value
  // this.tooltip = this.props.tooltip.value !==  '' ? this.props.tooltip.value : 'No value'
  },

  enterEditMode: function (event) {
    this.setState({ editMode: true })
    EditableTableCellActions.focusInput(this.cell_id, this.props.value)
  },

  exitEditMode: function (event) {
    if (event.type === 'blur' || event.keyCode === 13) { // Keycode for 'Enter' key
      if (event.target.value !== this.display_value) {
        this.updateCellValue(event.target.value)
      }
      this.setState({editMode: false})
    }
  },

  updateCellValue: function (new_value) {

    let computed_id = this.props.row[this.props.field.key].computed

    if (new_value === '' && computed_id) { // this is the delete //
      ComputedDatapointAPI.deleteComputedDataPoint(computed_id)
      this.display_value = ''
      this.setState({ editMode: false, hasError: false })

    // WHAT DOES THIS DO -- Under what circubmstance will this prevent bad data ///
    // let validation = EditableTableCellActions.validateValue(new_value)
    // if (!validation) {
    //   this.setState({ editMode: false, hasError: true })
    } else {
      this.isSaving = true
      let query_params = {
        location_id: this.props.row.location_id,
        campaign_id: this.props.row.campaign_id.id,
        indicator_id: this.props.field.key,
        computed_id: this.props.row[this.props.field.key].computed,
        value: this.props.field.schema.data_format === 'pct' ? new_value / 100.00 : new_value
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
        this.display_value = query_params.value
        this.isSaving = false
        this.hasError = false
        if (!this.isBool) { this.setState({editMode: false}) }
      }, reject => {
        this.display_value = query_params.value
        this.isSaving = false
        this.hasError = true
        if (!this.isBool) { this.setState({editMode: false}) }
      })
    }

    this.display_value = new_value
    this.forceUpdate()
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
      input_field = <input
                      type='text'
                      onBlur={this.exitEditMode}
                      onKeyUp={this.exitEditMode}
                      id={this.cell_id} />
    }

    if (this.isSaving) {
      spinner = <i className='fa fa-spinner fa-spin saving-icon'></i>
    }

    let data_format = this.props.field.schema.data_format

    let cell = ''
    if (data_format === 'bool') {
      this.isBool = true
      let items = [
        {
          'value': '0',
          'title': 'No'
        },
        {
          'value': '1',
          'title': 'Yes'
        },
        {
          'value': '',
          'title': 'No Data'
        }
      ]

      let dropDownDisplayValue = 'No Data'
      if (this.display_value) {
        dropDownDisplayValue = items[this.display_value].title
      }

      cell = (<td>
                <DropdownMenu
                  items={items}
                  sendValue={this.updateCellValue}
                  text={dropDownDisplayValue}
                  onChange={this.updateCellValue}
                  style='boolColor'
                />
              </td>)
    } else {
      cell = (<TableCell
                field={this.props.field}
                row={this.props.row}
                value={this.display_value}
                formatValue={this.props.formatValue}
                classes={classes}
                onClick={this.enterEditMode}
                hideValue={hideValue}>
                {spinner}
                {input_field}
              </TableCell>)
    }
    return (cell)
  }
})

export default EditableTableCell
