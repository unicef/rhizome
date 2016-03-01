import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'

import ChartActions from 'actions/ChartActions'
import CampaignActions from 'actions/CampaignActions'
import IndicatorActions from 'actions/IndicatorActions'
import LocationActions from 'actions/LocationActions'
import OfficeActions from 'actions/OfficeActions'

var RootStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: [ChartActions, CampaignActions, IndicatorActions, LocationActions, OfficeActions],

  getInitialState () {
    return {
      chartIndex: [],
      campaignIndex: [],
      indicatorIndex: [],
      locationIndex: [],
      officeIndex: [],
      loading: false
    }
  },

  // CHARTS
  // -------------------------------------------------------------------------
  onFetchCharts () {
    this.setState({ loading: true })
  },

  onFetchChartsCompleted (response) {
    const charts = []
    response.forEach(chart => { charts[chart.id] = chart })
    this.setState({ chartIndex: charts, loading: false })
  },

  onFetchChartsFailed (error) {
    this.setState({ chartIndex: error, loading: false })
  },

  // CAMPAIGNS
  // -------------------------------------------------------------------------
  onFetchCampaigns () {
    this.setState({ loading: true })
  },
  onFetchCampaignsCompleted (response) {
    const campaigns = []
    response.forEach(campaign => { campaigns[campaign.id] = campaign })
    this.setState({ campaignIndex: campaigns, loading: false })
  },
  onFetchCampaignsFailed (error) {
    this.setState({ campaignIndex: error, loading: false })
  },

  // INDICATORS
  // -------------------------------------------------------------------------
  onFetchIndicators () {
    this.setState({ loading: true })
  },
  onFetchIndicatorsCompleted (response) {
    const indicators = []
    response.forEach(indicator => { indicators[indicator.id] = indicator })
    this.setState({ indicatorIndex: indicators, loading: false })
  },
  onFetchIndicatorsFailed (error) {
    this.setState({ indicatorIndex: error, loading: false })
  },

  // LOCATIONS
  // -------------------------------------------------------------------------
  onFetchLocations () {
    this.setState({ loading: true })
  },
  onFetchLocationsCompleted (response) {
    const locations = []
    response.forEach(location => { locations[location.id] = location })
    this.setState({ locationIndex: locations, loading: false })
  },
  onFetchLocationsFailed (error) {
    this.setState({ locationIndex: error, loading: false })
  },

  // OFFICES
  // -------------------------------------------------------------------------
  onFetchOffices () {
    this.setState({ loading: true })
  },
  onFetchOfficesCompleted (response) {
    const offices = []
    response.forEach(office => { offices[office.id] = office })
    this.setState({ officeIndex: offices, loading: false })
  },
  onFetchOfficesFailed (error) {
    this.setState({ officeIndex: error, loading: false })
  }

})

export default RootStore
