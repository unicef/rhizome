import React from 'react'
import IconButton from 'components/atoms/IconButton'

var DropdownIcon = React.createClass({

  mixins: [
    require('components/atoms/dropdowns/DropdownControl')
  ],

  propTypes: {
    className: React.PropTypes.string,
    color: React.PropTypes.string,
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
      <IconButton {...this.props} onClick={this._toggleMenu}/>
    )
  }
})

export default DropdownIcon
