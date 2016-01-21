import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import CellStore from 'stores/CellStore'
import CellActions from 'actions/CellActions'

var Cell = React.createClass({
  mixins: [Reflux.connect(CellStore)],

  isEditing: false,

  propTypes: {
    item: React.PropTypes.object
  },

  formatted: function () {
    if (this.props.item.value === undefined || this.props.item.value === null) {
      return ''
    }
  },

  missing: function () {
    return _.isNull(this.props.item.value)
  },

  _EditValue: function (isEditable) {
    this.isEditing = true
    CellActions.toggleEditing(isEditable)
    this.forceUpdate()
  },

  _submit: function () {
    this.isEditing = false
    CellActions.submit()
    this.forceUpdate()
  },

  render: function () {
    let input = (
      <input type='textfield' className='editControl'
        v-model='value | validator'
        onBlur={this._submit} />
    )

    let itemInput = this.isEditing && this.props.item.isEditable ? input : ''

    let isEditable = this.props.item.isEditable ? 'editable ' : ''
    let isEditing = this.isEditing ? 'editing ' : ''
    let missing = this.missing() ? 'missing ' : ''
    let saving = this.state.isSaving ? 'saving ' : ''

    return (
      <td className={isEditable + isEditing + missing + saving + this.props.item.class} colSpan={this.props.item.colspan}>
        {this.props.item.value}
        <div onClick={this._EditValue.bind(this, this.props.item.isEditable)} className='displayValue'>
          {this.formatted()}
        </div>
        {itemInput}
      </td>
    )
  }
})

export default Cell
