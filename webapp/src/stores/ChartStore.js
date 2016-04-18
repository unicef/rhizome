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
    index: null,
    loading: false
  },

  getInitialState: function () {
    return this.charts
  },

  // =========================================================================== //
  //                               API CALL HANDLERS                             //
  // =========================================================================== //
  // ===============================  Fetch Charts  ============================ //
  onFetchCharts: function () {
    this.setState({ raw: null })
  },
  onFetchChartsCompleted: function (response) {
    this.charts.loading = false
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
  onFetchChartsFailed: function (error) {
    this.setState({ error: error })
  },

  // ===============================  Post Chart  ============================= //
  onPostChart: function () {
    this.setState({ raw: null, loading: true })
  },
  onPostChartCompleted: function (response) {
    ChartActions.fetchCharts()
  },
  onPostChartFailed: function (error) {
    this.setState({ error: error })
  },

  // ===============================  Delete Chart  ============================ //
  onDeleteChart: function () {
    this.setState({ raw: null })
  },
  onDeleteChartCompleted: function (response) {
    ChartActions.fetchCharts()
  },
  onDeleteChartFailed: function (error) {
    this.setState({ error: error })
  }

})

export default ChartStore
