import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import CellStore from 'stores/CellStore'
import CellActions from 'actions/CellActions'

var Cell = React.createClass({
  mixins: [Reflux.connect(CellStore)],

  propTypes: {
    item: React.PropTypes.object
  },

  formatted: function () {
    if (this.props.item.value === undefined || this.props.item.value === null) {
      return ''
    } else {
      // format according to attached method if it exists
      return this.format ? this.format(this.value) : this.value
    }
  },

  missing: function () {
    return _.isNull(this.props.item.value)
  },

  render: function () {
    let input = (
      <input type='textfield' className='editControl'
        v-model='value | validator'
        onBlur={CellActions.submit} />
    )

    let itemInput = this.state.isEditing && this.props.item.isEditable ? input : ''

    let isEditable = this.props.item.isEditable ? 'editable ' : ''
    let isEditing = this.state.isEditing ? 'editing ' : ''
    let missing = this.missing() ? 'missing ' : ''
    let saving = this.state.isSaving ? 'saving ' : ''

    return (
      <td className={isEditable + isEditing + missing + saving + this.props.item.class} colSpan={this.props.item.colspan}>
        {this.props.item.value}
        <div onClick={CellActions.toggleEditing.bind(this, this.props.item.isEditable)} className='displayValue'>
          {this.formatted()}
        </div>
        {itemInput}
      </td>
    )
  }
})

export default Cell
