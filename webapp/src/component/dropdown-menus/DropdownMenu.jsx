import _ from 'lodash'
import React from 'react'

import MenuItem from 'component/MenuItem.jsx'

var DropdownMenu = React.createClass({

  mixins: [
    require('mixin/MenuControl')
  ],

  propTypes: {
    items: React.PropTypes.array.isRequired,
    sendValue: React.PropTypes.func.isRequired,
    item_plural_name: React.PropTypes.string,
    text: React.PropTypes.string,
    style: React.PropTypes.string,
    icon: React.PropTypes.string,
    uniqueOnly: React.PropTypes.bool,
    multi: React.PropTypes.bool
  },

  getDefaultProps: function () {
    return {
      icon: 'fa-bars',
      uniqueOnly: false,
      multi: false
    }
  },

  componentWillReceiveProps: function (nextProps) {
    if (!this.multi && nextProps.text !== this.props.text) {
      this.setState({ open: false })
    }
  },

  componentWillUpdate: function (nextProps, nextState) {
    var filtered_items = this.filterMenu(this.props.items, this.state.pattern)
    var menu_items = this.props.uniqueOnly ? _.uniq(filtered_items, (item) => { return item.id }) : filtered_items
    nextProps.children = MenuItem.fromArray(menu_items, this.props.sendValue)
    nextProps.onSearch = this._setPattern
  },

  _setPattern: function (value) {
    this.setState({ pattern: value })
  },

  render: function () {
    if (this.props.items.length === 0) {
      return (
        <button className={'button' + this.props.style }>
          <i className='fa fa-spinner fa-spin'></i>
          Loading {_.capitalize(this.props.item_plural_name)}...
        </button>
      )
    }

    var icon = this.props.icon ? (<i className={['fa', this.props.icon].join(' ')} />) : null
    var classes = this.state.open ? 'menu-button open' : 'menu-button '

    return (
      <span className={classes}>
        <a className={'button ' + this.props.style} role='button' onClick={this._toggleMenu}>
          {icon} {this.props.text}
        </a>
      </span>
    )
  }
})

export default DropdownMenu
