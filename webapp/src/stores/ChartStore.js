import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'

import ChartActions from 'actions/ChartActions'

var ChartStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: ChartActions,

  getInitialState () {
    return {
      selectedLocations: [],
      chart: null,
      chart_data: null,
      loading: false
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
    const chart = response.chart_json
    chart.id = response.id
    chart.title = response.title
    ChartActions.fetchChartDatapoints(chart)
    this.setState({ chart: chart, loading: false })
  },
  onFetchChartFailed (error) {
    this.setState({ chart: error, loading: false })
  },

  // ===============================  Fetch Charts  ============================= //
  onFetchCharts () {
    this.setState({ loading: true })
  },
  onFetchChartsCompleted (response) {
    const charts = []
    response.forEach(chart => { charts[chart.id] = chart })
    this.setState({ charts: charts, loading: false })
  },
  onFetchChartsFailed (error) {
    this.setState({ charts: error, loading: false })
  },

  // ===========================  Fetch Chart Datapoints  ========================= //
  onFetchChartDatapoints () {
    this.setState({ loading: true })
  },
  onFetchChartDatapointsCompleted (response) {
    this.setState({ chart_data: response, loading: false })
  },
  onFetchChartDatapointsFailed (error) {
    this.setState({ chart_data: error, loading: false })
  }

})

export default ChartStore
