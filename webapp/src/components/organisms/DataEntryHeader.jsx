import _ from 'lodash'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'

import CampaignDropdown from 'components/molecules/menus/CampaignDropdown'
import CampaignStore from 'stores/CampaignStore'
import DataEntryActions from 'actions/DataEntryActions'

const DataEntryHeader = React.createClass({

  mixins: [
    Reflux.connect(CampaignStore, 'campaigns'),
  ],

  render () {
    const props = this.props

    const dashboard_filters = (
      <div className='page-header-filters'>
        <CampaignDropdown
          campaigns={props.campaigns.raw || []}
          selected={props.selected_campaign}
          sendValue={id => DataEntryActions.setCampaign(props.campaigns.index[id])}
        />
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
