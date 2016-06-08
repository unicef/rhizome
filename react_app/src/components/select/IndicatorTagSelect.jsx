import React, {Component, PropTypes} from 'react'

import Select from 'components/select/Select'
import DropdownMenuItem from 'components/dropdown/DropdownMenuItem'

const IndicatorTagSelect = ({indicator_tags, selected_indicator_tag, selectIndicatorTag}) => {
  const indicator_tag_menu_items = indicator_tags.map(indicator_tag =>
    <DropdownMenuItem
      key={'indicator_tag-' + indicator_tag.id}
      text={indicator_tag.tag_name}
      onClick={() => selectIndicatorTag(indicator_tag)}
      classes='indicator_tag'
    />
  )
  return (
    <Select
      className='font-weight-600 cd-titlebar-margin'
      icon='fa-chevron-down'
      text={selected_indicator_tag ? selected_indicator_tag.tag_name : 'Select Form'}
      searchable={false}
      items={indicator_tag_menu_items} />
  )
}

export default IndicatorTagSelect
