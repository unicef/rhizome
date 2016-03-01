import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'

import ChartActions from 'actions/ChartActions'
import prepareChartData from 'data/chartData'

var ChartStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: ChartActions,

  getInitialState () {
    return {
      selectedLocations: [],
      loading: false
    }
  },

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

  onPrepChartData (chart) {
    console.log('STORE - onPrepChartData')
    console.log('chart', chart)
    prepareChartData(chart)
    console.log('STORE - AFTER PREP')
  }

  // onFetchForChartData: chart => {
  //   const dashboard_layout = 1 // Hard Coded - figure out programatic way
  //   let responses = [
  //     api.locations(),
  //     api.campaign(),
  //     api.office(),
  //     api.indicators(null, null, { 'cache-control': 'no-cache' })
  //   ]
  //   let promise = ChartDataInit.prepareData(chart, dashboard_layout || 0, responses)
  //   // this.setState(chart: ChartDataInit.prepareData(
  //   //   chart, dashboard_layout || 0, responses)
  //   // )
  // }
})

export default ChartStore
