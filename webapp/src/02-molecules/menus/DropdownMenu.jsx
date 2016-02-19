import _ from 'lodash'
import React from 'react'

import MenuItem from '02-molecules/MenuItem.jsx'

var DropdownMenu = React.createClass({

  mixins: [
    require('02-molecules/menus/MenuControl')
  ],

  propTypes: {
    items: React.PropTypes.array.isRequired,
    sendValue: React.PropTypes.func.isRequired,
    item_plural_name: React.PropTypes.string,
    text: React.PropTypes.string,
    style: React.PropTypes.string,
    icon: React.PropTypes.string,
    value_field: React.PropTypes.string,
    title_field: React.PropTypes.string,
    uniqueOnly: React.PropTypes.bool,
    multi: React.PropTypes.bool,
    grouped: React.PropTypes.bool
  },

  getDefaultProps: function () {
    return {
      icon: 'fa-bars',
      uniqueOnly: false,
      multi: false,
      grouped: false,
      value_field: 'value',
      title_field: 'title'
    }
  },

  componentWillReceiveProps: function (nextProps) {
    if (!this.multi && nextProps.text !== this.props.text) {
      this.setState({ open: false })
    }
  },

  componentWillUpdate: function (nextProps, nextState) {
    if (this.props.grouped) {
      nextProps.children = this._getGroupedMenuItemComponents(this.props.items, this.state.pattern)
    } else {
      nextProps.children = this._getMenuItemComponents(this.props.items, this.state.pattern)
    }

    nextProps.onSearch = this._setPattern
  },

  _getGroupedMenuItemComponents: function (items, pattern) {
    let grouped_menu_item_components = []

    _.forEach(items, function (item) {
      let menu_item_components = this._getMenuItemComponents(item.value, pattern)
      let group_name_component = <MenuItem key={item.title} depth={0} sendValue={_.noop} title={item.title} classes='menu-group-title' />
      menu_item_components.splice(0, 0, group_name_component)
      grouped_menu_item_components = grouped_menu_item_components.concat(menu_item_components)
    }, this )

    return grouped_menu_item_components
  },

  _getMenuItemComponents: function (items, pattern) {
    var filtered_items = this.filterMenu(items, pattern)
    var menu_items = this.props.uniqueOnly ? _.uniq(filtered_items, (item) => { return item.id }) : filtered_items
    menu_items = menu_items.map(item => {
      // if (typeof item.title === 'undefined' || item.title !== null ) {
        item.title = item[this.props.title_field]
      // }
      // if (typeof item.value === 'undefined' || item.value !== null ) {
        item.value = item[this.props.value_field].toString()
      // }
      return item
    })
    return menu_items.map(item => {
      return (<MenuItem key={item.value} depth={0} sendValue={this.props.sendValue} {...item} /> )
    })
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

    return (
      <a className={'button ' + this.props.style} role='button' onClick={this._toggleMenu}>
        {icon} {this.props.text}
      </a>
    )
  }
})

export default DropdownMenu
