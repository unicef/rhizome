import React from 'react'
import Layer from 'react-layer'
import Tooltip from '02-molecules/Tooltip'

var TableCell = React.createClass({

  propTypes: {
    key: React.PropTypes.string,
    value: React.PropTypes.string,
    classes: React.PropTypes.string,
    formatValue: React.PropTypes.func,
    onClick: React.PropTypes.func,
    tooltip: React.PropTypes.string,
    hideValue: React.PropTypes.bool,
    children: React.PropTypes.array
  },

  getInitialState () {
    return {
      tooltip: null
    }
  },

  handleClick: function (event) {
    this.hideTooltip()
    return this.props.onClick(event)
  },

  showTooltip: function (event) {
     if (typeof this.props.tooltip === 'undefined' || this.props.tooltip === null || this.props.hideValue) return

    let render = () => {
      return <Tooltip left={event.pageX} top={event.pageY}>{this.props.tooltip}</Tooltip>
    }
    this.state.tooltip = new Layer(document.body, render)
    this.state.tooltip.render()
  },

  hideTooltip: function () {
    if (this.state.tooltip) {
      this.state.tooltip.destroy()
      this.state.tooltip = null
    }
  },

  render: function () {
    let value = this.props.value
    let shouldDisplayValue = (typeof value !== 'undefined' || value !== null) && !this.props.hideValue

    let value_component = ''

    if (shouldDisplayValue) {
      if (this.props.formatValue) {
        value_component = <span className='display-value'>{this.props.formatValue(value)}</span>
      } else {
        value_component = <span className='display-value'>{value}</span>
      }
    }

    return (
      <td onClick={this.handleClick}
        onMouseOver={this.showTooltip}
        onMouseOut={this.hideTooltip}
        className={this.props.classes}>
        { value_component }
        { this.props.children }
      </td>
    )
  }
})

export default TableCell
