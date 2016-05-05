import React, {Component, PropTypes} from 'react'

import Select from 'components/atoms/select/Select'
import DropdownMenuItem from 'components/atoms/dropdown/DropdownMenuItem'

var IndicatorTagSelect = React.createClass({
  propTypes: {
    indicator_tags: React.PropTypes.array.isRequired,
    selected: React.PropTypes.object.isRequired,
    sendValue: React.PropTypes.func.isRequired
  },

  getDefaultProps () {
    return {
      indicator_tags: [],
      selected: {'name': 'Loading ...'}
    }
  },

  render () {
    const indicator_tag_menu_items = this.props.indicator_tags.map(indicator_tag =>
      <DropdownMenuItem
        key={'indicator_tag-' + indicator_tag.id}
        text={indicator_tag.tag_name}
        onClick={this.props.sendValue.bind(this, indicator_tag.id)}
        classes='indicator_tag'
      />
    )

    const selected_text = this.props.selected ? this.props.selected.tag_name : 'Select Form'
    return (
      <Select
        className='font-weight-600 cd-titlebar-margin'
        icon='fa-chevron-down'
        text={selected_text}
        searchable={false}>
        {indicator_tag_menu_items}
      </Select>
    )
  }
})

export default IndicatorTagSelect
