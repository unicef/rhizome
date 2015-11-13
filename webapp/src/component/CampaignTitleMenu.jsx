'use strict'

import React from 'react'
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
    var campaigns = CampaignMenuItem.fromArray(this.props.campaigns, this.props.sendValue)
    var startDate = moment(this.props.selected.start_date, 'YYYY-MM-DD').format('MMMM YYYY')

    return (
      <TitleMenu
        icon='fa-chevron-down'
        text={startDate}>
        {campaigns}
      </TitleMenu>
    )
  }
})

export default CampaignTitleMenu
