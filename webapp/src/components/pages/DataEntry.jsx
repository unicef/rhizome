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

let DataEntry = React.createClass({

  mixins: [
    Reflux.connect(DataEntryStore),
    Reflux.connect(CampaignStore, 'campaigns'),
    Reflux.connect(IndicatorStore, 'indicators')
  ],

  componentWillMount: function () {
    DataEntryActions.initData()
  },

  render: function () {
    let tableData = this.state.apiResponseData

    return (
      <div>
        <DataEntryHeader {...this.state}/>
        <div className='row'>
          <div className='medium-12 columns'>
            <DatabrowserTable
              data={tableData}
              selected_locations={this.state.locationSelected}
              selected_indicators={this.state.filteredIndicators}
              editable />
          </div>
        </div>
        <div className='row'>
          <form className='medium-12 columns'>
            <div className='medium-2 columns'>
              <label htmlFor='locations'><h3>Locations</h3></label>
              <DropdownMenu
                items={this.state.filterLocations}
                sendValue={DataEntryActions.addLocations}
                item_plural_name='Locations'
                text='Select Locations'
                icon=''
                uniqueOnly/>
              <List items={this.state.locationSelected} removeItem={DataEntryActions.removeLocation} />
              <br /><br />
            </div>
          </form>
        </div>
      </div>
    )
  }
})

export default DataEntry
