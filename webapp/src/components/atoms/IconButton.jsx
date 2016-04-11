import React, {PropTypes} from 'react'
import Layer from 'react-layer'
import Tooltip from 'components/molecules/Tooltip'

var IconButton = React.createClass({

  propTypes: {
    icon: PropTypes.string.isRequired,
    text: PropTypes.string,
    alt_text: PropTypes.string,
    onClick: PropTypes.func,
    className: PropTypes.string,
    style: PropTypes.object,
    isBusy: PropTypes.bool
  },

  getDefaultProps: function () {
    return {
      icon: 'info-circle',
      text: null,
      alt_text: 'Loading ...',
      isBusy: false,
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
      return <Tooltip left={event.pageX} top={event.pageY}>{ this.props.isBusy ? this.props.alt_text : this.props.text}</Tooltip>
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
        <i className={'fa ' + (this.props.isBusy ? 'fa-spinner fa-spin' : this.props.icon)}/>
      </button>
    )
  }
})

export default IconButton
