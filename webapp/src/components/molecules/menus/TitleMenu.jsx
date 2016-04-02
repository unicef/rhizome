import React from 'react'

var TitleMenu = React.createClass({

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
      <div className={'dropdown-list ' + this.props.className} onClick={this._toggleMenu}>
          {
            this.props.icon ? (
              <div className='row'>
                <div className='small-10 medium-10 columns dashboard-nav__text'>{this.props.text}</div>
                <div className='small-2 medium-2 columns'>
                  <a className='menu-button fa-stack'>
                    <i className={'fa fa-stack-1x ' + this.props.icon}></i>
                  </a>
                </div>
              </div>
            ) : (
              <div className='row'>
                <div className='medium-12 columns dashboard-nav__text'>{this.props.text}</div>
              </div>
            )
          }
      </div>
    )
  }

})

export default TitleMenu
