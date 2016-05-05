import React from 'react'
import _ from 'lodash'
import moment from 'moment'

import Select from 'components/atoms/select/Select'
import DropdownMenuItem from 'components/atoms/dropdown/DropdownMenuItem'

var CampaignSelect = React.createClass({
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
      <DropdownMenuItem
        key={'campaign-' + campaign.id}
        text={campaign.name}
        onClick={this.props.sendValue.bind(this, campaign.id)}
        classes='campaign'
      />
    )

    const selected_text = this.props.selected ? this.props.selected.name : 'Select Campaign'
    return (
      <Select
        className='font-weight-600 cd-titlebar-margin'
        icon='fa-chevron-down'
        text={selected_text}
        searchable={false}>
        {campaign_menu_items}
      </Select>
    )
  }
})

export default CampaignSelect
