import React from 'react'

var Cell = React.createClass({
  propTypes: {
    item: React.PropTypes.object
  },

  render: function () {
    let input = (
      <input type='textfield' className='editControl'
        v-model='value | validator'
        v-on='keyup: submit | key 13, blur: submit' />
    )

    let itemInput = this.props.item.isEditable ? input : ''
    return (
      <td className={this.props.item.class} colSpan={this.props.item.colspan}>
        {this.props.item.value}
        {itemInput}
      </td>
    )
  }
})

export default Cell
