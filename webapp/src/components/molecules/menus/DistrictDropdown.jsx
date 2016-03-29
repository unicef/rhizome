import _ from 'lodash'
import React from 'react'

import Dropdown from 'components/molecules/menus/Dropdown'
import DropdownItem from 'components/molecules/menus/DropdownItem'

const filters = [
  { id: 1, value: 0, name: 'All LPDs', type: 'LPD Status' },
  { id: 2, value: 1, name: 'LPD 1', type: 'LPD Status' },
  { id: 3, value: 2, name: 'LPD 2', type: 'LPD Status' },
  { id: 4, value: 3, name: 'LPD 3', type: 'LPD Status' }
]

const DistrictDropdown = React.createClass({
  propTypes: {
    selected: React.PropTypes.object.isRequired,
    sendValue: React.PropTypes.func.isRequired,
    idsToRender: React.PropTypes.array
  },

  getDefaultProps () {
    return {
      statuses: [],
      idsToRender: [],
      selected: filters[0]
    }
  },

  render () {
    const selected_text = _.isEmpty(this.props.selected) ? filters[0].name: this.props.selected.name

    const indicator_menu_items = filters.map(filter =>
      <DropdownItem
        key={'filter-' + filter.id}
        text={filter.name}
        onClick={() => this.props.sendValue(filter)}
        classes='filter'
      />
    )

    return (
      <Dropdown
        className='font-weight-600 cd-titlebar-margin'
        icon='fa-chevron-down'
        searchable={false}
        text={selected_text}>
        {indicator_menu_items}
      </Dropdown>
    )
  }
})

export default DistrictDropdown