import React from 'react'

var DropdownIcon = React.createClass({

  mixins: [
    require('components/molecules/menus/MenuControl')
  ],

  propTypes: {
    className: React.PropTypes.string,
    text: React.PropTypes.string.isRequired,
    icon: React.PropTypes.string,
    searchable: React.PropTypes.bool,
    onSearch: React.PropTypes.func
  },

  getDefaultProps: function () {
    return {
      icon: 'fa-bars'
    }
  },

  componentWillReceiveProps: function (nextProps) {
    if (nextProps.text !== this.props.text) {
      this.setState({ open: false })
    }
  },

  render: function () {
    return (
      <button className='button icon-button remove-chart-button' onClick={this._toggleMenu}>
        <i className={'fa ' + this.props.icon}/>
      </button>
    )
  }
})

export default DropdownIcon
