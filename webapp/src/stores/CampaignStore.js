import _ from 'lodash'
import moment from 'moment'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'
import CampaignActions from 'actions/CampaignActions'
import OfficeStore from 'stores/OfficeStore'

var CampaignStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: CampaignActions,

  offices_index: {},

  campaigns: {
    meta: null,
    raw: null,
    index: null,
    filtered: [],
    list: [],
    selected: []
  },

  init () {
    CampaignActions.fetchCampaigns()
    this.listenTo(OfficeStore, this.onOfficeStore)
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
    this.campaigns.raw = response.objects
    this.campaigns.index = _.indexBy(this.campaigns.raw, 'id')
    this.processCampaigns()
  },
  onFetchCampaignsFailed (error) {
    this.setState({ error: error })
  },

  // =========================================================================== //
  //                            OTHER STORE DEPENDECIES                          //
  // =========================================================================== //
  onOfficeStore (offices) {
    this.offices_index = offices.index
    this.processCampaigns()
  },

  // =========================================================================== //
  //                                  UTILITIES                                  //
  // =========================================================================== //
  processCampaigns () {
    if (this.campaigns.raw && this.offices_index) {
      this.campaigns.list = _(this.campaigns.raw).map(campaign => {
        return _.assign({}, campaign, {
          'start_date': moment(campaign.start_date, 'YYYY-MM-DD').toDate(),
          'end_date': moment(campaign.end_date, 'YYYY-MM-DD').toDate(),
          'office': this.offices_index[campaign.office_id]
        })
      })
      .sortBy(_.method('start_date.getTime'))
      .reverse()
      .value()
      this.campaigns.filtered = this.campaigns.list
      this.setState(this.campaigns)
    }
  }
})

export default CampaignStore
