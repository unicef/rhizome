import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'
import RootStore from 'stores/RootStore'
import ChartActions from 'actions/ChartActions'

var ChartStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: ChartActions,

  init () {
    this.listenTo(RootStore, this.onRootStore)
  },

  getInitialState () {
    return {
      selectedLocations: [],
      selectedIndicators: [],
      selectedCampaign: null,
      chart: null,
      chartDef: null,
      datapoints: null,
      loading: false
    }
  },

  onRootStore (store) {
    this.campaignIndex = store.campaignIndex
    this.chartIndex = store.chartIndex
    this.locationIndex = store.locationIndex
    this.indicatorIndex = store.indicatorIndex
    this.officeIndex = store.officeIndex
    this.rootDataIsReady = store.dataIsReady
  },

  // =========================================================================== //
  //                                 BASIC ACTIONS                               //
  // =========================================================================== //
  onSetSelectedLocations (location_ids, locationIndex) {
    if (location_ids && locationIndex.length) {
      if (Array.isArray(location_ids)) {
        this.setState({ selectedLocations: location_ids.map(id => locationIndex[id]) })
      } else {
        this.setState({ selectedLocations: [locationIndex[location_ids]] })
      }
    }
  },
  onSetSelectedIndicators (indicator_ids, indicatorIndex) {
    if (indicator_ids && indicatorIndex.length) {
      if (Array.isArray(indicator_ids)) {
        this.setState({ selectedIndicators: indicator_ids.map(id => indicatorIndex[id]) })
      } else {
        this.setState({ selectedIndicators: [indicatorIndex[indicator_ids]] })
      }
    }
  },
  onSetSelectedCampaign (campaign_id) {
    if (campaign_id && this.campaignIndex[campaign_id]) {
      this.setState({ selectedCampaign: this.campaignIndex[campaign_id] })
    } else {
      this.setState({ selectedCampaign: this.campaignIndex[0] })
    }
  },

  // =========================================================================== //
  //                              API CALL HANDLERS                              //
  // =========================================================================== //

  // ===============================  Fetch Chart  ============================= //
  onFetchChart () {
    this.setState({ loading: true })
  },
  onFetchChartCompleted (response) {
    const chartDef = response.chart_json
    chartDef.id = response.id
    chartDef.title = response.title
    this.setState({ chartDef: chartDef, loading: false })
    this.joinLeading(RootStore, (RootStore) => {
      ChartActions.fetchChartDatapoints(chartDef)
      ChartActions.setSelectedIndicators(chartDef.indicator_ids, this.indicatorIndex)
      ChartActions.setSelectedLocations(chartDef.location_ids, this.locationIndex)
    })
  },
  onFetchChartFailed (error) {
    this.setState({ chartDef: error, loading: false })
  },

  // ==========================  Fetch Chart Datapoints  ======================== //
  onFetchChartDatapoints () {
    this.setState({ loading: true })
  },
  onFetchChartDatapointsCompleted (response) {
    this.setState({ datapoints: response, loading: false })
  },
  onFetchChartDatapointsFailed (error) {
    this.setState({ datapoints: error, loading: false })
  }
})

export default ChartStore
