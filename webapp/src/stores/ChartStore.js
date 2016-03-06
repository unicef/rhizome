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
    ChartActions.fetchChartDatapoints(chartDef)
    this.setState({ chartDef: chartDef, loading: false })
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
