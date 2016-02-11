import React from 'react'

var ButtonMenu = React.createClass({
  mixins: [
    require('02-molecules/menus/MenuControl')
  ],

  propTypes: {
    text: React.PropTypes.string.isRequired,
    style: React.PropTypes.string
  },

  componentWillReceiveProps: function (nextProps) {
    if (nextProps.text !== this.props.text) {
      this.setState({ open: false })
    }
  },

  render: function () {
    return (
      <div className={this.props.style + ' cd-button'} onClick={this._toggleMenu}>
        CHOOSE
      </div>
    )
  }

})

export default ButtonMenu
