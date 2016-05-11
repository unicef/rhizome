import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'

import RootActions from 'actions/RootActions'
import IndicatorActions from 'actions/IndicatorActions'
import LocationActions from 'actions/LocationActions'
import CampaignActions from 'actions/CampaignActions'
import OfficeActions from 'actions/OfficeActions'
import DashboardActions from 'actions/DashboardActions'
import ChartActions from 'actions/ChartActions'

var RootStore = Reflux.createStore({

  listenables: RootActions,

  mixins: [StateMixin.store],

  data: {
    campaigns: [],
    charts: [],
    dashboards: [],
    indicators: [],
    locations: [],
    offices: [],
    loading: false
  },

  getInitialState () {
    return this.data
  },

  init () {
    this.getInitialData()
  },

  getInitialData () {
    RootActions.fetchAllMeta()
  },

  // =========================================================================== //
  //                               API CALL HANDLERS                             //
  // =========================================================================== //

  // ===============================  Fetch Meta  ============================= //
  onFetchAllMeta () {
    this.setState({ loading: true })
  },
  onFetchAllMetaCompleted (response) {
    this.data.superuser = response.objects[0].is_superuser
    this.data.campaigns = response.objects[0].campaigns
    this.data.charts = response.objects[0].charts
    this.data.dashboards = response.objects[0].dashboards
    this.data.indicators = response.objects[0].indicators
    this.data.locations = response.objects[0].locations
    this.data.offices = response.objects[0].offices
    CampaignActions.fetchCampaigns.completed(response)
    ChartActions.fetchCharts.completed(response)
    DashboardActions.fetchDashboards.completed(response)
    IndicatorActions.fetchIndicators.completed(response)
    IndicatorActions.fetchIndicatorTags.completed(response)
    IndicatorActions.fetchIndicatorsToTags.completed(response)
    LocationActions.fetchLocations.completed(response)
    OfficeActions.fetchOffices.completed(response)
    this.trigger(this.data)
  },
  onFetchAllMetaFailed (error) {
    this.setState({ error: error })
  }
})

export default RootStore
