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
    this.setState({ loading: true })
  },
  onFetchChartsCompleted (response) {
    this.charts.meta = response.meta
    this.charts.raw = response.objects[0].charts || response.objects
    this.charts.list = this.charts.raw.map(c => {
      c.chart_json = JSON.parse(c.chart_json)
      return c
    })
    this.charts.index = _.indexBy(this.charts.raw, 'id')
    this.trigger(this.charts)
  },
  onFetchChartsFailed (error) {
    this.setState({ error: error })
  }
})

export default ChartStore
