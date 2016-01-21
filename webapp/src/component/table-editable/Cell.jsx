import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import CellStore from 'stores/CellStore'
import CellActions from 'actions/CellActions'
import randomHash from 'util/randomHash'

var Cell = React.createClass({
  mixins: [Reflux.connect(CellStore)],

  previousValue: null, // save the previous value to compare with edited value
  isSaving: false, // whether the cell is in the process of saving right now
  isEditable: false, // whether the cell is editable
  isEditing: false, // whether the cell is currently being edited
  hasError: false,

  cellId: 'edit_id_' + randomHash(),

  propTypes: {
    item: React.PropTypes.object
  },

  formatted: function () {
    if (this.props.item.value === undefined || this.props.item.value === null) {
      return ''
    } else {
      // format according to attached method if it exists
      return this.props.item.format ? this.props.item.format(this.props.item.value) : this.props.item.value
    }
  },

  missing: function () {
    return _.isNull(this.props.item.value)
  },

  _editValue: function () {
    if (this.props.item.isEditable) {
      this.isEditing = true
      this.forceUpdate()
      CellActions.focusInput(this.cellId)
    }
  },

  _keuUp: function (event) {
    if (event.keyCode === 13) {
      this._submit()
    }
  },

  _submit: function () {
    if (this.props.item.isEditable) {
      this.isEditing = false
      this.forceUpdate()
    }
  },

  render: function () {
    let input = (<input type='textfield' className='editControl' onBlur={this._submit} onKeyUp={this._keuUp} id={this.cellId}/>)

    let itemInput = this.props.item.isEditable && this.isEditing ? input : ''
    let isEditable = this.props.item.isEditable ? 'editable ' : ''
    let isEditing = this.isEditing ? 'editing ' : ''
    let missing = this.missing() ? 'missing ' : ''
    let saving = this.isSaving ? 'saving ' : ''
    let error = this.hasError ? 'error ' : ''
    let className = isEditable + isEditing + missing + saving + error + this.props.item.class
    let icon = this.props.item.isEditable ? (<i className='fa fa-spinner fa-spin saving-icon'></i>) : ''

    return (
      <td className={className} colSpan={this.props.item.colspan}>
        {icon}
        <div onClick={this._editValue} className='displayValue'>
          {this.formatted()}
        </div>
        {itemInput}
      </td>
    )
  }
})

export default Cell
