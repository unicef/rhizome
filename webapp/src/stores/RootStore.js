import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'

import ChartActions from 'actions/ChartActions'
import CampaignActions from 'actions/CampaignActions'
import IndicatorActions from 'actions/IndicatorActions'
import LocationActions from 'actions/LocationActions'
import OfficeActions from 'actions/OfficeActions'

var RootStore = Reflux.createStore({

  mixins: [StateMixin.store],

  init () {
    this.getInitialData()
  },

  getInitialState () {
    return {
      chartIndex: [],
      campaignIndex: [],
      indicatorIndex: [],
      locationIndex: [],
      officeIndex: []
    }
  },

  getInitialData () {
    const promises = [
      OfficeActions.fetchOffices(),
      CampaignActions.fetchCampaigns(),
      IndicatorActions.fetchIndicators(),
      LocationActions.fetchLocations(),
      ChartActions.fetchCharts()
    ]
    Promise.all(promises).then(values => {
      const [offices, campaigns, indicators, locations, charts] = values
      const officeIndex = []
      const campaignIndex = []
      const indicatorIndex = []
      const locationIndex = []
      const chartIndex = []

      offices.forEach(office => { officeIndex[office.id] = office })
      campaigns.forEach(campaign => { campaignIndex[campaign.id] = campaign })
      indicators.forEach(indicator => { indicatorIndex[indicator.id] = indicator })
      locations.forEach(location => { locationIndex[location.id] = location })
      charts.forEach(chart => { chartIndex[chart.id] = chart })

      this.setState({
        officeIndex: officeIndex,
        campaignIndex: campaignIndex,
        indicatorIndex: indicatorIndex,
        locationIndex: locationIndex,
        chartIndex: chartIndex
      })
    })
  }

})

export default RootStore
