import React from 'react'
import _ from 'lodash'
import moment from 'moment'

import Dropdown from 'components/molecules/menus/Dropdown'
import DropdownItem from 'components/molecules/menus/DropdownItem'

var CampaignDropdown = React.createClass({
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
      <DropdownItem
        key={'campaign-' + campaign.id}
        text={campaign.name}
        onClick={this.props.sendValue.bind(this, campaign.id)}
        classes='campaign'
      />
    )

    const selected_text = this.props.selected ? this.props.selected.name : 'Select Campaign'
    return (
      <Dropdown
        className='font-weight-600 cd-titlebar-margin'
        icon='fa-chevron-down'
        text={selected_text}
        searchable={false}>
        {campaign_menu_items}
      </Dropdown>
    )
  }
})

export default CampaignDropdown
