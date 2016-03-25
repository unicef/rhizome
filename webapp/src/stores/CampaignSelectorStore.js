import _ from 'lodash'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'
import CampaignSelectorActions from 'actions/CampaignSelectorActions'
import CampaignStore from 'stores/CampaignStore'

const CampaignSelectorStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: CampaignSelectorActions,

  campaigns: [],

  selected_campaigns: [],

  getInitialState () {
    return this.selected_campaigns
  },

  init () {
    this.listenTo(CampaignStore, this.onCampaignStore)
  },

  onCampaignStore (store) {
    this.campaigns = store
  },

  onSelectCampaign (id) {
    this.selected_campaigns.push(this.campaigns.index[id])
    this.trigger(this.selected_campaigns)
  },

  onDeselectCampaign (id) {
    _.remove(this.selected_campaigns, {id: id})
    this.trigger(this.selected_campaigns)
  },

  onReorderCampaign (selected_campaigns) {
    this.selected_campaigns = selected_campaigns
    this.trigger(this.selected_campaigns)
  },

  onSetSelectedCampaigns (ids) {
    if (Array.isArray(ids)) {
      this.selected_campaigns = ids.map(id => this.campaigns.index[id])
    } else {
      this.selected_campaigns = [this.campaigns.index[ids]]
    }
    this.trigger(this.selected_campaigns)
  },

  onClearSelectedCampaigns () {
    this.selected_campaigns = []
    this.trigger(this.selected_campaigns)
  }
})

export default CampaignSelectorStore
