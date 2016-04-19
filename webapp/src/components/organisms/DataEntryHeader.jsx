import _ from 'lodash'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'

import DropdownMenu from 'components/molecules/menus/DropdownMenu'
import IndicatorTagDropdown from 'components/molecules/menus/IndicatorTagDropdown'
import CampaignDropdown from 'components/molecules/menus/CampaignDropdown'
import DataEntryActions from 'actions/DataEntryActions'

const DataEntryHeader = React.createClass({

  render () {
    const props = this.props
    const dashboard_filters = (
      <div className='page-header-filters'>
        <CampaignDropdown
          campaigns={props.campaigns.raw || []}
          selected={props.selected_campaign}
          sendValue={id => DataEntryActions.setCampaign(props.campaigns.index[id])}
        />
        <IndicatorTagDropdown
          indicator_tags={props.indicators.tags || []}
          selected={props.selected_indicator_tag}
          sendValue={id => DataEntryActions.setForm(props.indicators.tags.filter(tag => tag.id ===id)[0])}
        />
        <DropdownMenu
          items={props.filterLocations}
          sendValue={DataEntryActions.addLocations}
          item_plural_name='Locations'
          text='Add Locations'
          style='button'
          uniqueOnly/>
      </div>
    )
    return (
      <header className='row page-header'>
        <div className='medium-5 columns medium-text-left small-text-center'>
          <h1>Enter Data</h1>
        </div>
        <div className='medium-7 columns medium-text-right small-text-center dashboard-actions'>
          { dashboard_filters }
        </div>
      </header>
    )
  }
})

export default DataEntryHeader
