import React from 'react'
import Reflux from 'reflux'

import IndicatorTagDropdown from 'components/molecules/menus/IndicatorTagDropdown'
import DropdownMenu from 'components/molecules/menus/DropdownMenu'
import CampaignDropdown from 'components/molecules/menus/CampaignDropdown'
import DatabrowserTable from 'components/molecules/DatabrowserTable'

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
    IndicatorStore.listen(indicators => DataEntryActions.setForm(indicators.tags[1]))
  },

  render: function () {
    const state = this.state
    const campaigns = state.campaigns
    const indicators = state.indicators

    return (
      <div>
        <header className='row page-header'>
          <div className='medium-5 columns medium-text-left small-text-center'>
            <h1>Enter Data</h1>
          </div>
          <div className='medium-7 columns medium-text-right small-text-center dashboard-actions'>
            <div className='page-header-filters'>
              <CampaignDropdown
                campaigns={campaigns.raw || []}
                selected={state.selected_campaign}
                sendValue={id => DataEntryActions.setCampaign(campaigns.index[id])}
              />
              <IndicatorTagDropdown
                indicator_tags={indicators.tags || []}
                selected={state.selected_indicator_tag}
                sendValue={id => DataEntryActions.setForm(indicators.tags.filter(tag => tag.id === id)[0])}
              />
              <DropdownMenu
                items={state.filterLocations}
                sendValue={DataEntryActions.addLocations}
                item_plural_name='Locations'
                text='Add Locations'
                style='button'
                uniqueOnly/>
            </div>
          </div>
        </header>
        <div className='row'>
          <div className='medium-12 columns'>
            <DatabrowserTable
              data={state.apiResponseData}
              selected_locations={state.locationSelected}
              selected_indicators={state.filteredIndicators}
              rowAction={DataEntryActions.removeLocation}
              hideCampaigns
              editable />
          </div>
        </div>
      </div>
    )
  }
})

export default DataEntry
