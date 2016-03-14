import _ from 'lodash'
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
      chart_def: null,
      chart_data: null,
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
    const chart_def = response.chart_json
    chart_def.id = response.id
    chart_def.title = response.title
    ChartActions.fetchChartDatapoints(chart_def)
    this.setState({ chart_def: chart_def, loading: false })
  },
  onFetchChartFailed (error) {
    this.setState({ chart_def: error, loading: false })
  },

  // ==========================  Fetch Chart Datapoints  ======================== //
  onFetchChartDatapoints () {
    this.setState({ loading: true })
  },
  onFetchChartDatapointsCompleted (response) {
    const chart_data = _(response.objects)
      .flatten()
      .sortBy(_.method('campaign.start_date.getTime'))
      .map(melt)
      .flatten()
      .value()
    this.setState({ datapoints: response, loading: false, chart_data: chart_data })
  },
  onFetchChartDatapointsFailed (error) {
    this.setState({ datapoints: error, loading: false })
  }
})

function melt (d) {
  const base = _.omit(d, 'indicators')
  return d.indicators.map(i => _.assign({indicator: i.indicator, value: i.value}, base))
}

export default ChartStore
