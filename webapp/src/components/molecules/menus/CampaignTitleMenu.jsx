import React from 'react'
import _ from 'lodash'
import moment from 'moment'

import TitleMenu from 'components/molecules/menus/TitleMenu'
import TitleMenuItem from 'components/molecules/menus/TitleMenuItem'

var CampaignTitleMenu = React.createClass({
  propTypes: {
    campaigns: React.PropTypes.array.isRequired,
    selected: React.PropTypes.object.isRequired,
    sendValue: React.PropTypes.func.isRequired
  },

  getDefaultProps () {
    return {
      campaigns: [],
      selected: {'name':'Loading ...'}
    }
  },

  render () {
    const campaign_menu_items = this.props.campaigns.map(campaign =>
      <TitleMenuItem
        key={'campaign-' + campaign.id}
        text={campaign.name}
        onClick={this.props.sendValue.bind(this, campaign.id)}
        classes='campaign'
      />
    )

    return (
      <TitleMenu
        className='font-weight-600 cd-titlebar-margin'
        icon='fa-chevron-down'
        text={this.props.selected.name}>
        {campaign_menu_items}
      </TitleMenu>
    )
  }
})

export default CampaignTitleMenu
