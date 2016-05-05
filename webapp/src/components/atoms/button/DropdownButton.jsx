import _ from 'lodash'
import React from 'react'

import ExpandableMenuItem from 'components/atoms/dropdown/ExpandableMenuItem'
import Dropdown from 'components/atoms/dropdown/Dropdown'

class DropdownButton extends Dropdown {

  static propTypes = {
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
  }

  static defaultProps = {
    uniqueOnly: false,
    multi: false,
    grouped: false,
    value_field: 'value',
    title_field: 'title'
  }

  componentWillReceiveProps = (nextProps) => {
    if (!this.multi && nextProps.text !== this.props.text) {
      this.setState({ open: false })
    }
  }

  componentWillUpdate = (nextProps, nextState) => {
    if (this.props.grouped) {
      nextProps.children = this._getGroupedMenuItemComponents(this.props.items, this.state.pattern)
    } else {
      nextProps.children = this._getMenuItemComponents(this.props.items, this.state.pattern)
    }

    nextProps.onSearch = this._setPattern
  }

  _getGroupedMenuItemComponents = (items, pattern) => {
    let grouped_menu_item_components = []

    items.forEach(item => {
      let menu_item_components = this._getMenuItemComponents(item.value, pattern)
      let group_name_component = <ExpandableMenuItem key={item.title} depth={0} sendValue={_.noop} title={item.title} classes='menu-group-title' />
      menu_item_components.splice(0, 0, group_name_component)
      grouped_menu_item_components = grouped_menu_item_components.concat(menu_item_components)
    })

    return grouped_menu_item_components
  }

  _getMenuItemComponents = (items, pattern) => {
    const filtered_items = this.filterMenu(items, pattern)
    let menu_items = this.props.uniqueOnly ? _.uniq(filtered_items, item => item.id) : filtered_items
    menu_items = menu_items.map(item => {
      item.title = item[this.props.title_field]
      item.value = item[this.props.value_field].toString()
      return item
    })
    return menu_items.map(item => <ExpandableMenuItem key={item.value} depth={0} sendValue={this.props.sendValue} {...item} />)
  }

  _setPattern = (value) => {
    this.setState({ pattern: value })
  }

  render = () => {
    if (!this.props.items || this.props.items.length === 0) {
      if (this.props.text) {
        return (
          <button className={this.props.style} role='button'>
            <i className='fa fa-spinner fa-spin'></i> &nbsp;
            Loading {_.capitalize(this.props.item_plural_name)}...
          </button>
        )
      } else {
        return <i className='fa fa-spinner fa-spin right'></i>
      }
    }

    const icon = this.props.icon ? (<i className={['fa', this.props.icon].join(' ')} />) : null

    return (
      <button className={this.props.style} role='button' onClick={this._toggleMenu}>
        {icon} {this.props.text}
      </button>
    )
  }
}

export default DropdownButton
