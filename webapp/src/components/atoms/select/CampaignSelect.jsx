import _ from 'lodash'
import moment from 'moment'
import React, {Component, PropTypes} from 'react'

import Select from 'components/atoms/select/Select'
import DropdownMenuItem from 'components/atoms/dropdown/DropdownMenuItem'

class CampaignSelect extends Component {

  static propTypes = {
    campaigns: React.PropTypes.array.isRequired,
    selected: React.PropTypes.object.isRequired,
    sendValue: React.PropTypes.func.isRequired
  }

  static defaultProps = {
    campaigns: [],
    selected: {'name':'Loading ...'}
  }

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
}

export default CampaignSelect
