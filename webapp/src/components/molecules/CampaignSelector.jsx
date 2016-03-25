import _ from 'lodash'
import React, { PropTypes } from 'react'
import Reflux from 'reflux'
import ReorderableList from 'components/molecules/list/ReorderableList'
import DropdownMenu from 'components/molecules/menus/DropdownMenu'
import CampaignTitleMenu from 'components/molecules/menus/CampaignTitleMenu'

import CampaignStore from 'stores/CampaignStore'
import CampaignSelectorStore from 'stores/CampaignSelectorStore'
import CampaignSelectorActions from 'actions/CampaignSelectorActions'

const CampaignSelector = React.createClass({

  mixins: [
    Reflux.connect(CampaignSelectorStore, 'selected_campaigns'),
  ],

  campaigns_index: null,

  propTypes: {
    campaigns: PropTypes.shape({
      raw: PropTypes.array,
      list: PropTypes.array
    }).isRequired,
    preset_campaign_ids: PropTypes.array,
    classes: PropTypes.string,
    multi: PropTypes.bool
  },

  getDefaultProps() {
    return {
      multi: false,
      preset_campaign_ids: null
    }
  },

  componentDidMount () {
    CampaignStore.listen(campaigns => {
      if (this.props.preset_campaign_ids && campaigns.index) {
        CampaignSelectorActions.setSelectedCampaigns(this.props.preset_campaign_ids)
      } else if (campaigns.index) {
        CampaignSelectorActions.setSelectedCampaigns(campaigns.raw[0].id)
      }
    })
  },

  componentWillReceiveProps(nextProps) {
    if (!_.isEmpty(nextProps.preset_campaign_ids) && nextProps.campaigns.index && _.isEmpty(this.state.selected_campaigns)) {
      this.setState({selected_campaigns: nextProps.preset_campaign_ids.map(id => nextProps.campaigns.index[id])})
    }
  },

  getAvailableCampaigns () {
    const selected_ids = this.state.selected_campaigns.map(campaign => campaign.id)
    const campaigns_list = this.props.campaigns.list
    campaigns_list.forEach(campaign_group => {
      campaign_group.children.forEach(campaign => {
        campaign.disabled = selected_ids.indexOf(campaign.id) > -1
      })
    })
    return campaigns_list
  },

  render () {
    const props = this.props
    const raw_campaigns = props.campaigns.raw || []
    if (props.multi) {
      const available_campaigns = this.getAvailableCampaigns()
      return (
        <form className={props.classes}>
          <h3>Campaigns
            <DropdownMenu
              items={available_campaigns}
              sendValue={CampaignSelectorActions.selectCampaign}
              item_plural_name='Campaigns'
              style='icon-button right'
              icon='fa-plus'
            />
          </h3>
          <a className='remove-filters-link' onClick={CampaignSelectorActions.clearSelectedCampaigns}>Remove All </a>
          <ReorderableList items={this.state.selected_campaigns} removeItem={CampaignSelectorActions.deselectCampaign} dragItem={CampaignSelectorActions.reorderCampaign} />
        </form>
      )
    } else {
      return (
        <div className={props.classes}>
          <h3>Campaign</h3>
          <CampaignTitleMenu
            campaigns={raw_campaigns}
            selected={this.state.selected_campaigns[0]}
            sendValue={CampaignSelectorActions.setSelectedCampaigns}/>
        </div>
      )
    }
  }
})

export default CampaignSelector
