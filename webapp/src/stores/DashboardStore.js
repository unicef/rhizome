import _ from 'lodash'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'

import DashboardActions from 'actions/DashboardActions'

var DashboardStore = Reflux.createStore({

  listenables: [DashboardActions],

  mixins: [StateMixin.store],

  dashboards: {
    list: null,
    meta: null,
    raw: null,
    index: null
  },

  getInitialState () {
    return this.dashboards
  },

  // =========================================================================== //
  //                               API CALL HANDLERS                             //
  // =========================================================================== //
  // =============================  Fetch Dashboards  ========================== //
  onFetchDashboards () {
    this.trigger(this.dashboards)
  },
  onFetchDashboardsCompleted (response) {
    const dashboards = response.objects[0].dashboards || response.objects
    this.dashboards.raw = dashboards
    this.dashboards.meta = response.meta
    this.dashboards.index = _.indexBy(this.dashboards.raw, 'id')
    // Patch the non-comformant API response
    this.dashboards.list = _(dashboards).map(dashboard => {
      dashboard.charts = dashboard.charts || dashboard.dashboard_json
      return dashboard
    })
    .reject(_.isNull)
    .value()
    this.trigger(this.dashboards)
  },
  onFetchDashboardsFailed (error) {
    this.setState({ error: error })
  },

  // ===============================  Post Chart  ============================= //
  onPostDashboard () {
    this.trigger(this.dashboards)
  },
  onPostDashboardCompleted (response) {
    DashboardActions.fetchDashboards()
  },
  onPostDashboardFailed (error) {
    this.setState({ error: error })
  },

  // ===============================  Delete Dashboard  ============================ //
  onDeleteDashboard () {
    this.trigger(this.dashboards)
  },
  onDeleteDashboardCompleted (response) {
    DashboardActions.fetchDashboards()
  },
  onDeleteDashboardFailed (error) {
    this.setState({ error: error })
  }
})

export default DashboardStore
