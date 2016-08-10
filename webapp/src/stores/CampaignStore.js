import _ from 'lodash'
import moment from 'moment'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'
import CampaignActions from 'actions/CampaignActions'

var CampaignStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: CampaignActions,

  campaigns: {
    meta: null,
    raw: null,
    index: null,
    filtered: [],
    list: []
  },

  getInitialState () {
    return this.campaigns
  },

  // =========================================================================== //
  //                              API CALL HANDLERS                              //
  // =========================================================================== //

  // =============================  Fetch Campaigns  =========================== //
  onFetchCampaigns () {
    this.setState({ raw: [] })
  },
  onFetchCampaignsCompleted (response) {
    this.campaigns.meta = response.meta
    this.campaigns.raw = response.objects[0].campaigns || response.objects
    this.processCampaigns()
  },
  onFetchCampaignsFailed (error) {
    this.setState({ error: error })
  },

  // =========================================================================== //
  //                                  UTILITIES                                  //
  // =========================================================================== //
  processCampaigns () {
    if (this.campaigns.raw) {
      this.campaigns.list = _(this.campaigns.raw).map(campaign => {
        return _.assign({}, campaign, {
          'start_date': moment(campaign.start_date, 'YYYY-MM-DD').toDate(),
          'end_date': moment(campaign.end_date, 'YYYY-MM-DD').toDate(),
        })
      })
      .sortBy(_.method('start_date.getTime'))
      .reverse()
      .value()
      this.campaigns.index = _.indexBy(this.campaigns.list, 'id')
      this.campaigns.filtered = this.campaigns.list
      this.trigger(this.campaigns)
    }
  }
})

export default CampaignStore
