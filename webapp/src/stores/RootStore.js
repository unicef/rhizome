import _ from 'lodash'
import builtins from 'components/organisms/dashboard/builtin'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'

import RootActions from 'actions/RootActions'

var RootStore = Reflux.createStore({

  listenables: RootActions,

  mixins: [StateMixin.store],

  data: {
    charts: [],
    dashboards: [],
    loading: false
  },

  getInitialState () {
    return this.data
  },

  init () {
    this.getInitialData()
  },

  getInitialData () {
    RootActions.fetchAllCharts()
    RootActions.fetchAllDashboards()
  },

  // =========================================================================== //
  //                               API CALL HANDLERS                             //
  // =========================================================================== //

  // ===============================  Fetch Charts  ============================= //
  onFetchAllCharts () {
    this.setState({ loading: true })
  },
  onFetchAllChartsCompleted (response) {
    this.data.charts = response.objects
    this.data.loading = false
    this.trigger(this.data)
  },
  onFetchAllChartsFailed (error) {
    this.setState({ error: error })
  },

  // ===============================  Fetch Dashboards  ============================= //
  onFetchAllDashboards () {
    this.setState({ loading: true })
  },
  onFetchAllDashboardsCompleted (response) {
    const all_dashboards = builtins.concat(_(response.objects).sortBy('id').reverse().value())
    // Patch the non-comformant API response
    this.data.dashboards = _(all_dashboards).map(dashboard => {
      dashboard.charts = dashboard.charts || dashboard.dashboard_json
      return dashboard
    })
    .reject(_.isNull)
    .value()
    this.trigger(this.data)
  },
  onFetchAllDashboardsFailed (error) {
    this.setState({ error: error })
  }

})

export default RootStore
