import React from 'react'

var TitleMenu = React.createClass({
  mixins: [
    require('mixin/MenuControl')
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
      <div className={'dropdown-list ' + this.props.className} onClick={this._toggleMenu}>
        {this.props.text}
        <a className='menu-button fa-stack'>
          <i className={'fa fa-stack-1x ' + this.props.icon}></i>
        </a>
      </div>
    )
  }

})

export default TitleMenu
