import React, {Component} from 'react'
import {Multiselect} from 'react-widgets'
import DropdownButton from 'components/button/DropdownButton'
import Placeholder from 'components/global/Placeholder'
import CampaignSelect from 'components/select/CampaignSelect'

const selectLocation = () => {
  console.log('hello')
}

class EnterDataPage extends Component {

  render () {
    const props = this.props
    const datapoints = [] // temporary
    const selected_locations = [] // temporary
    const campaign_select = (
      <CampaignSelect
        campaigns={props.campaigns.raw || []}
        selected_campaign={props.selected_campaign}
        selectCampaign={id => props.selectGlobalCampaign(props.campaigns.index[id])}
      />
    )
    const placeholder = selected_locations.length < 1
      ? <Placeholder height={300} text={'Add location(s) to begin'} loading={false}/>
      : <Placeholder height={300}/>
    return (
      <div>
        <header className='row page-header'>
          <div className='medium-5 columns medium-text-left small-text-center'>
            <h1>Enter Data</h1>
          </div>
          <div className='medium-7 columns medium-text-right small-text-center dashboard-actions'>
            <div className='page-header-filters'>
              { campaign_select }
              <DropdownButton
                items={props.locations.list}
                sendValue={id => props.selectGlobalLocation(props.locations.index[id])}
                item_plural_name='Locations'
                text='Add Locations'
                style='button'
                searchable
                uniqueOnly
              />
            </div>
          </div>
        </header>
        <div className='row'>
          <div className='medium-12 columns'>
            { datapoints.flattened ? data_table : placeholder }
          </div>
        </div>
      </div>
    )
  }
}

export default EnterDataPage
