import React from 'react'
import Reflux from 'reflux'

import CampaignDropdown from 'components/molecules/menus/CampaignDropdown'
import DropdownMenu from 'components/molecules/menus/DropdownMenu'
import DatabrowserTable from 'components/molecules/DatabrowserTable'
import List from 'components/molecules/list/List'

import DataEntryHeader from 'components/organisms/DataEntryHeader'
import IndicatorStore from 'stores/IndicatorStore'
import CampaignStore from 'stores/CampaignStore'
import DataEntryStore from 'stores/DataEntryStore'
import DataEntryActions from 'actions/DataEntryActions'

const DataEntry = React.createClass({

  mixins: [
    Reflux.connect(DataEntryStore),
    Reflux.connect(CampaignStore, 'campaigns'),
    Reflux.connect(IndicatorStore, 'indicators')
  ],

  componentWillMount: function () {
    DataEntryActions.initData()
    CampaignStore.listen(campaigns => DataEntryActions.setCampaign(campaigns.raw[0]))
  },

  render: function () {
    const table_data = this.state.apiResponseData
    console.log('table_data', table_data)

    return (
      <div>
        <DataEntryHeader {...this.state}/>
        <div className='row'>
          <div className='medium-12 columns'>
            <DatabrowserTable
              data={table_data}
              selected_locations={this.state.locationSelected}
              selected_indicators={this.state.filteredIndicators}
              editable />
          </div>
        </div>
        <div className='row text-center'>
          <br/><br/><br/><br/><br/><br/>
          <DropdownMenu
            items={this.state.filterLocations}
            sendValue={DataEntryActions.addLocations}
            item_plural_name='Locations'
            text='Add Locations'
            icon=''
            uniqueOnly/>
        </div>
      </div>
    )
  }
})

export default DataEntry
