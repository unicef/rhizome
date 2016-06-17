import React from 'react'
import DropdownButton from 'components/button/DropdownButton'

const BoolCell = ({cellParams}) => {
	const params = cellParams.params
	const datapoint = cellParams.datapoint
	const display_value = datapoint.display_value ? datapoint.display_value : 'No Data'
	const boolean_options = [
      { 'value': '0', 'title': 'No' },
      { 'value': '1', 'title': 'Yes' },
      { 'value': '', 'title': 'No Data' }
   ]

	return (
		<DropdownButton
      items={boolean_options}
      text={display_value}
      style='boolean-dropdown hollow'
      searchable={false}
      sendValue={value => {
        datapoint.value = value
        cellParams.updateDatapoint(datapoint)
      }}
    />
	)
}


export default BoolCell