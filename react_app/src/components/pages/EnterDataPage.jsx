import React from 'react'
import {Multiselect} from 'react-widgets'
import DropdownButton from 'components/button/DropdownButton'

const selectLocation = () => {
  console.log('hello')
}

const EnterDataPage = ({campaigns, indicators, locations}) => {
 return  (
  <div>
  	<h1>EnterData Page</h1>
    <DropdownButton
      items={locations.list}
      sendValue={selectLocation}
      item_plural_name='Locations'
      text='Add Locations'
      style='button'
      searchable
      uniqueOnly
    />
  </div>
)
}

export default EnterDataPage