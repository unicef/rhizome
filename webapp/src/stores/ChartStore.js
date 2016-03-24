import _ from 'lodash'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'

import ChartActions from 'actions/ChartActions'

var ChartStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: ChartActions,

  charts: {
    meta: null,
    list: null,
    raw: null,
    index: null
  },

  getInitialState () {
    return this.charts
  },

  // =========================================================================== //
  //                               API CALL HANDLERS                             //
  // =========================================================================== //
  // ===============================  Fetch Charts  ============================ //
  onFetchCharts () {
    this.setState({ raw: null })
  },
  onFetchChartsCompleted (response) {
    this.charts.meta = response.meta
    this.charts.raw = response.objects[0].charts || response.objects
    this.charts.list = this.charts.raw.map(chart => {
      if (typeof chart.chart_json === 'string') {
        chart.chart_json = JSON.parse(chart.chart_json)
      }
      return chart
    })
    this.charts.index = _.indexBy(this.charts.raw, 'id')
    this.trigger(this.charts)
  },
  onFetchChartsFailed (error) {
    this.setState({ error: error })
  },

  // ===============================  Post Chart  ============================= //
  onPostChart () {
    this.setState({ raw: null })
  },
  onPostChartCompleted (response) {
    ChartActions.fetchCharts()
  },
  onPostChartFailed (error) {
    this.setState({ error: error })
  },

  // ===============================  Delete Chart  ============================ //
  onDeleteChart () {
    this.setState({ raw: null })
  },
  onDeleteChartCompleted (response) {
    ChartActions.fetchCharts()
  },
  onDeleteChartFailed (error) {
    this.setState({ error: error })
  }
})

export default ChartStore
