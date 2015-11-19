import React from 'react'

var DropdownMenu = React.createClass({
  mixins: [
    require('mixin/MenuControl')
  ],

  propTypes: {
    text: React.PropTypes.string,
    icon: React.PropTypes.string,
    size: React.PropTypes.string,
    multi: React.PropTypes.bool
  },

  getDefaultProps: function () {
    return {
      icon: 'fa-bars',
      multi: false
    }
  },

  componentWillReceiveProps: function (nextProps) {
    if (!this.multi && nextProps.text !== this.props.text) {
      this.setState({ open: false })
    }
  },

  render: function () {
    var icon = this.props.icon
      ? (<i className={['fa', this.props.icon, this.props.size].join(' ')} />)
      : null

    var classes = 'menu-button'

    if (this.state.open) {
      classes += ' open'
    }

    return (
      <span className={classes}>
        <a className='button' role='button' onClick={this._toggleMenu}>
          {icon} {this.props.text}
        </a>
      </span>
    )
  }
})

export default DropdownMenu
