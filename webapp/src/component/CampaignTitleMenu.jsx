import React from 'react'
import _ from 'lodash'
import moment from 'moment'

import TitleMenu from 'component/TitleMenu.jsx'
import CampaignMenuItem from 'component/CampaignMenuItem.jsx'

var CampaignTitleMenu = React.createClass({
  propTypes: {
    campaigns: React.PropTypes.array.isRequired,
    selected: React.PropTypes.object.isRequired,
    sendValue: React.PropTypes.func.isRequired,
    location: React.PropTypes.object.isRequired
  },

  render: function () {
    let campaigns = this.props.campaigns.map(campaign => {
      let percentageComplete = ' (' + Math.round(campaign.management_dash_pct_complete * 100) + '% complete)'
      return _.assign({}, campaign, {
        slug: campaign.slug + percentageComplete
      })
    })
    let campaignItems = CampaignMenuItem.fromArray(campaigns, this.props.sendValue)
    var startDate = moment(this.props.selected.start_date, 'YYYY-MM-DD').format('MMMM YYYY')

    return (
      <TitleMenu
        className='font-weight-600 cd-titlebar-margin'
        icon='fa-chevron-down'
        text={startDate}>
        {campaignItems}
      </TitleMenu>
    )
  }
})

export default CampaignTitleMenu
