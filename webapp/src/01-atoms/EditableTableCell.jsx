import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import TableCell from '01-atoms/TableCell'
import EditableTableCellStore from 'stores/EditableTableCellStore'
import EditableTableCellActions from 'actions/EditableTableCellActions'
import randomHash from '00-utilities/randomHash'

let EditableTableCell = React.createClass({

  mixins: [Reflux.connect(EditableTableCellStore)],

  propTypes: {
    key: React.PropTypes.string,
    schema: React.PropTypes.object,
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
        let promise = EditableTableCellActions.saveCellValue(event.target.value, this.props.field.key)
        promise.then(response => {
          this.isSaving = false
          this.hasError = false
          this.setState({editMode: false})
        })
      }
      this.display_value = event.target.value
    }
  },

  render: function () {
    let classes = this.props.classes + ' editable'
    classes += this.state.editMode ? 'editing ' : ''
    classes += this.state.isSaving ? 'saving ' : ''
    classes += this.state.hasError ? 'error ' : ''
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
      <TableCell key={this.props.key}
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
