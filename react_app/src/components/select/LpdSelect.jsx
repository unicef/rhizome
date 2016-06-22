import _ from 'lodash'
import React from 'react'
import DropdownButton from 'components/button/DropdownButton'

const LpdSelect = props => {
  const filters = [
    { id: 0, value: 0, title: 'All Districts', type: 'LPD Status' },
    { id: 1, value: 1, title: 'LPD 1', type: 'LPD Status' },
    { id: 2, value: 2, title: 'LPD 2', type: 'LPD Status' },
    { id: 3, value: 3, title: 'LPD 3', type: 'LPD Status' },
    { id: 4, value: '1,2,3', title: 'All LPDs', type: 'LPD Status' }
  ]

  const _selectLpds = id => {
    const selected_filter = _.keyBy(filters, 'id')[id]
    // Weird annoying hack to deal with the way DropdownButton modifies the original array
    if (parseInt(id) === 4) {
      selected_filter.value = '1,2,3'
    }
    props.sendValue(selected_filter)
  }

  return (
    <DropdownButton
      items={filters}
      text={props.selected.title}
      value_field='id'
      style='dropdown-list'
      icon='fa-chevron-down'
      sendValue={_selectLpds}
    />
  )
}

export default LpdSelect
