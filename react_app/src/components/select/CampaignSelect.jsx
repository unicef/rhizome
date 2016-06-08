import React, {Component, PropTypes} from 'react'

import Select from 'components/select/Select'
import DropdownMenuItem from 'components/dropdown/DropdownMenuItem'

const CampaignSelect = ({campaigns, selected_campaign, selectCampaign}) => {
  const campaign_menu_items = campaigns.map(campaign =>
    <DropdownMenuItem
      key={'campaign-' + campaign.id}
      text={campaign.name}
      onClick={() => selectCampaign(campaign)}
      classes='campaign'
    />
  )
  return (
    <Select
      className='font-weight-600 cd-titlebar-margin'
      icon='fa-chevron-down'
      text={selected_campaign ? selected_campaign.name : 'Loading ...'}
      searchable={false}
      items={campaign_menu_items} />
  )
}

export default CampaignSelect
