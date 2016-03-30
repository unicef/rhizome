import _ from 'lodash'
import React, { PropTypes } from 'react'
import Reflux from 'reflux'
import ReorderableList from 'components/molecules/list/ReorderableList'
import DropdownMenu from 'components/molecules/menus/DropdownMenu'
import CampaignTitleMenu from 'components/molecules/menus/CampaignTitleMenu'

import CampaignStore from 'stores/CampaignStore'

const CampaignSelector = React.createClass({

  propTypes: {
    campaigns: PropTypes.shape({
      raw: PropTypes.array,
      list: PropTypes.array
    }).isRequired,
    selected_campaigns: PropTypes.array,
    setCampaigns: PropTypes.func,
    linkCampaigns: PropTypes.func,
    selectCampaign: PropTypes.func,
    deselectCampaign: PropTypes.func,
    clearSelectedCampaigns: PropTypes.func,
    classes: PropTypes.string,
    linked: PropTypes.bool,
    multi: PropTypes.bool
  },

  getDefaultProps() {
    return {
      multi: false,
      linked: false,
      selected_campaigns: []
    }
  },

  render () {
    const props = this.props
    const raw_campaigns = props.campaigns.raw || []
    let selected_campaigns = !_.isEmpty(props.selected_campaigns) ? props.selected_campaigns : raw_campaigns
    if (props.multi) {
      return (
        <form className={props.classes}>
          <h3>Campaigns
            <DropdownMenu
              items={raw_campaigns}
              sendValue={this.props.selectCampaign}
              item_plural_name='Campaigns'
              style='icon-button right'
              icon='fa-plus'
            />
          </h3>
          <a className='remove-filters-link' onClick={this.props.clearSelectedCampaigns}>Remove All </a>
          <List items={selected_campaigns} removeItem={this.props.deselectCampaign} />
        </form>
      )
    } else {
      return (
        <div className={props.classes}>
          <h3>
            Campaign <a onClick={this.props.linkCampaigns}><i className={'fa ' + (this.props.linked ? 'fa-chain ' : 'fa-chain-broken') }/></a>
          </h3>
          <CampaignTitleMenu
            campaigns={raw_campaigns}
            selected={selected_campaigns[0]}
            sendValue={this.props.setCampaigns}/>
        </div>
      )
    }
  }
})

export default CampaignSelector
