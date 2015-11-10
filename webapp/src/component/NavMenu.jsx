'use strict'

var React = require('react')

var MenuControl = require('mixin/MenuControl')

var NavMenu = React.createClass({
  mixins: [
    require('mixin/MenuControl')
  ],

  propTypes: {
    text: React.PropTypes.string.isRequired,
    icon: React.PropTypes.string
  },

  render: function () {
    var display = this.props.icon
      ? (<span><i className={'fa fa-lg ' + this.props.icon}></i>&ensp;{this.props.text}</span>)
      : (<span>{this.props.text}</span>)

    return (
      <a onClick={this._toggleMenu} onBlur={this._onBlur} tabIndex='-1'>
        {display}&emsp;<i className='fa fa-chevron-down'></i>
      </a>
    )
  }

})

module.exports = NavMenu
