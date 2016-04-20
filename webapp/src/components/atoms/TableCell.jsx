import React from 'react'
import Layer from 'react-layer'
import Tooltip from 'components/molecules/Tooltip'
import moment from 'moment'
import numeral from 'numeral'
import format from 'utilities/format'

var TableCell = React.createClass({

  propTypes: {
    field: React.PropTypes.object,
    row: React.PropTypes.object,
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
    if (!this.props.onClick) return
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
    let value = this.props.value ? this.props.value : this.props.row[this.props.field.key]
    let shouldDisplayValue = (typeof value !== 'undefined' || value !== null) && !this.props.hideValue
    let value_component = ''

    if (shouldDisplayValue) {
      let display_value = format.autoFormat((typeof value !== 'object' ? value : value.value), this.props.field.schema.data_format, 2)
      value_component = this.props.field.renderer(
        display_value,
        this.props.field,
        { moment: moment, numeral: numeral }
      )
    }

    return (
      <td onClick={this.handleClick}
        onMouseOver={this.showTooltip}
        onMouseOut={this.hideTooltip}
        className={this.props.classes}>
        { this.props.field.name === 'location' ? <b>{ value_component }</b> : value_component }
        { this.props.children }
      </td>
    )
  }
})

export default TableCell
