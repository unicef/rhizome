import React from 'react'
import Layer from 'react-layer'
import Tooltip from 'components/molecules/Tooltip'

var DropdownIcon = React.createClass({

  propTypes: {
    icon: React.PropTypes.string.isRequired,
    text: React.PropTypes.string,
    onClick: React.PropTypes.func,
    className: React.PropTypes.string,
    style: React.PropTypes.object
  },

  getDefaultProps: function () {
    return {
      icon: 'info-circle',
      text: null,
      style: {fontSize: '2rem'}
    }
  },

  getInitialState: function () {
    return {
      tooltip: null,
    }
  },

  showTooltip: function (event) {
     if (typeof this.props.text === 'undefined' || this.props.text === null) return

    let render = () => {
      return <Tooltip left={event.pageX} top={event.pageY}>{this.props.text}</Tooltip>
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
    return (
      <button
        onClick={this.props.onClick}
        onMouseOver={this.showTooltip}
        onMouseOut={this.hideTooltip}
        className={'button icon-button ' + this.props.className}
      >
        <i className={'fa ' + this.props.icon}/>
      </button>
    )
  }
})

export default DropdownIcon
