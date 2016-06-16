import React from 'react'
import DropdownButton from 'components/button/DropdownButton'

const BoolCell = ({cellParams}) => {
	const params = cellParams.params
	const datapoint = cellParams.datapoint
	const displayValue = datapoint.value ? datapoint.value : 'No Data'
	const boolean_options = [
      { 'value': '0', 'title': 'No' },
      { 'value': '1', 'title': 'Yes' },
      { 'value': '', 'title': 'No Data' }
   ]
	return (
		<DropdownButton
      items={boolean_options}
      sendValue={value => cellParams.updateDatapoint({
      	value: value,
      	id: datapoint.id
      })}
      text={displayValue}
      style='boolean-dropdown'
      searchable={false} />
	)
}


export default BoolCell