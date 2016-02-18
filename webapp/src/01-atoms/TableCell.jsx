import React from 'react'
import Layer from 'react-layer'
import Tooltip from '02-molecules/Tooltip.jsx'

var TableCell = React.createClass({

  propTypes: {
    key: React.PropTypes.string,
    value: React.PropTypes.string,
    classes: React.PropTypes.string,
    formatValue: React.PropTypes.func,
    tooltip: React.PropTypes.string,
    children: React.PropTypes.array
  },

  getInitialState () {
    return {
      display_value: this.props.value,
      tooltip: null
    }
  },

  showTooltip: function (event) {
    if (typeof this.props.tooltip === 'undefined' || this.props.tooltip === null) return

    let render = () => {
      return <Tooltip left={event.pageX} top={event.pageY}>{this.props.tooltip}</Tooltip>
    }
    this.state.tooltip = new Layer(document.body, render)
    this.state.tooltip.render()
  },

  hideTooltip: function () {
    if (this.state.tooltip) {
      this.state.tooltip.destroy()
      this.setState({ tooltip: null })
    }
  },

  render: function () {
    let display_value = this.state.display_value
    if (typeof display_value === 'undefined' || display_value === null) {
      display_value = ''
    } else if (this.props.formatValue) {
      display_value = this.props.formatValue(this.display_value)
    }

    return (
      <td className={this.props.classes} onMouseOver={this.showTooltip} onMouseOut={this.hideTooltip}>
        { display_value }
        { this.props.children }
      </td>
    )
  }
})

export default TableCell
