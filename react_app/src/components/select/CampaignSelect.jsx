import _ from 'lodash'
import moment from 'moment'
import React, {Component, PropTypes} from 'react'

import Select from 'components/select/Select'
import DropdownMenuItem from 'components/dropdown/DropdownMenuItem'

class CampaignSelect extends Component {

  static propTypes = {
    campaigns: PropTypes.array.isRequired,
    selected: PropTypes.object.isRequired,
    sendValue: PropTypes.func.isRequired
  }

  static defaultProps = {
    campaigns: [],
  }

  render () {
    const props = this.props
    const selected_text = props.selected ? props.selected.name : 'Loading ...'
    const campaign_menu_items = this.props.campaigns.map(campaign =>
      <DropdownMenuItem
        key={'campaign-' + campaign.id}
        text={campaign.name}
        onClick={this.props.sendValue.bind(this, campaign.id)}
        classes='campaign'
      />
    )
    return (
      <Select
        className='font-weight-600 cd-titlebar-margin'
        icon='fa-chevron-down'
        text={selected_text}
        searchable={false}
        items={campaign_menu_items} />
    )
  }
}

export default CampaignSelect
