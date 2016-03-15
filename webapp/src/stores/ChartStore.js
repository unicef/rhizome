import _ from 'lodash'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'
import ChartActions from 'actions/ChartActions'
import DatapointActions from 'actions/DatapointActions'
import DatapointStore from 'stores/DatapointStore'

var ChartStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: ChartActions,

  init () {
    this.listenTo(DatapointStore, this.onDatapointStore)
  },

  chart: {
    def: {
      type: 'RawData',
      indicator_ids: [28, 34],
      location_ids: [1],
      countries: [],
      groupBy: 'indicator',
      timeRange: null,
      x: 0,
      xFormat: ',.0f',
      y: 0,
      yFormat: ',.0f',
      z: 0
    },
    data: null,
    loading: false
  },

  getInitialState () {
    return this.chart
  },

  // =========================================================================== //
  //                               API CALL HANDLERS                             //
  // =========================================================================== //

  // ===============================  Fetch Chart  ============================= //
  onFetchChart () {
    this.setState({ loading: true })
  },
  onFetchChartCompleted (response) {
    this.chart.def = response.chart_json
    this.chart.def.id = response.id
    this.chart.def.title = response.title
    DatapointActions.fetchDatapoints(this.chart.def)
    this.setState(this.chart)
  },
  onFetchChartFailed (error) {
    this.setState({ error: error })
  },

  // =========================================================================== //
  //                            REGULAR ACTION HANDLERS                          //
  // =========================================================================== //
  onSetDateRange (key, value) {
    this.chart.def.start_date = value
    this.trigger(this.chart)
  },

  // =========================================================================== //
  //                            OTHER STORE DEPENDECIES                          //
  // =========================================================================== //
  onDatapointStore (datapoints) {
    this.chart.data = _(datapoints.raw)
      .flatten()
      .sortBy(_.method('campaign.start_date.getTime'))
      .map(this.melt)
      .flatten()
      .value()
    this.setState(this.chart)
  },

  // =========================================================================== //
  //                                   UTILITIES                                 //
  // =========================================================================== //
  melt (datapoint) {
    const base = _.omit(datapoint, 'indicators')
    return datapoint.indicators.map(i => _.assign({indicator: i.indicator, value: i.value}, base))
  }
})

export default ChartStore
