import React from 'react'
import _ from 'lodash'
import moment from 'moment'

import TitleMenu from 'components/molecules/menus/TitleMenu.jsx'
import CampaignMenuItem from 'components/molecules/CampaignMenuItem.jsx'

var CampaignTitleMenu = React.createClass({
  propTypes: {
    campaigns: React.PropTypes.array.isRequired,
    selected: React.PropTypes.object.isRequired,
    sendValue: React.PropTypes.func.isRequired,
    location: React.PropTypes.object.isRequired
  },

  render: function () {
    let campaigns = this.props.campaigns.map(campaign => {
      return _.assign({}, campaign, {
        slug: campaign.slug
      })
    })
    let campaignItems = CampaignMenuItem.fromArray(campaigns, this.props.sendValue)

    var selectedCampaignName = this.props.selected.name
    return (
      <TitleMenu
        className='font-weight-600 cd-titlebar-margin'
        icon='fa-chevron-down'
        text={selectedCampaignName}>
        {campaignItems}
      </TitleMenu>
    )
  }
})

export default CampaignTitleMenu
