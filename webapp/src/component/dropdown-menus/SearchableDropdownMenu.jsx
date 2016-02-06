import _ from 'lodash'
import React from 'react'

import DropdownMenu from 'component/dropdown-menus/DropdownMenu.jsx'
import MenuItem from 'component/MenuItem.jsx'

var SearchableDropdownMenu = React.createClass({

  mixins: [
    require('mixin/MenuControl')
  ],

  propTypes: {
    items: React.PropTypes.array.isRequired,
    sendValue: React.PropTypes.func.isRequired,
    text: React.PropTypes.string,
    style: React.PropTypes.string,
    uniqueOnly: React.PropTypes.bool,
    icon: React.PropTypes.string,
    item_plural_name: React.PropTypes.string
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

    var filtered_items = this.filterMenu(this.props.items, this.state.pattern)
    var menu_items = this.props.uniqueOnly ? _.uniq(filtered_items, (item) => { return item.id }) : filtered_items
    var menu_items_components = MenuItem.fromArray(menu_items, this.props.sendValue)

    return (
      <DropdownMenu
        searchable
        onSearch={this._setPattern}
        text={this.props.text}
        style={this.props.style}
        icon={this.props.icon}>
        {menu_items_components}
      </DropdownMenu>
    )
  }
})

export default SearchableDropdownMenu
