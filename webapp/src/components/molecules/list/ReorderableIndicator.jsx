import React from 'react'
import IconButton from 'components/atoms/IconButton'
import DropdownIcon from 'components/atoms/DropdownIcon'
import DropdownItem from 'components/molecules/menus/DropdownItem'
import palettes from 'utilities/palettes'

export default React.createClass({
  propTypes: {
    item: React.PropTypes.object.isRequired
  },

  render: function () {
    let item = this.props.item
    const colors = palettes['full_rainbow']
    const color_menu_items = colors.map(color =>
      <li className='color-dot'>
        <IconButton
          onClick={() => item.setIndicatorColor(item.id, color)}
          icon={item.selectedColor === color ? ' fa-check-circle ' : ' fa-circle '}
          color={color}
        />
      </li>
    )
    return (
      <div key={item.id}>
        <DropdownIcon
          searchable={false}
          icon='fa-circle'
          text='Select Color'
          className='color-picker-icon'
          color={item.selectedColor}
        >
          {color_menu_items}
        </DropdownIcon>
        {item.short_name || item.name}
        <IconButton className='clear-btn' onClick={() => item.removeFunction(item.id)} icon='fa-times-circle' />
      </div>
    )
  }
})

