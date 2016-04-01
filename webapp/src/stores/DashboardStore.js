import _ from 'lodash'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'

import builtins from 'components/organisms/dashboard/builtin'
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
  onFetchDashboards () { console.info('DashboardStore.onFetchDashboards')
    this.trigger(this.dashboards)
  },
  onFetchDashboardsCompleted (response) { console.info('DashboardStore.onFetchDashboardsCompleted')
    const dashboards = response.objects[0].dashboards || response.objects
    this.dashboards.raw = dashboards
    this.dashboards.meta = response.meta
    this.dashboards.index = _.indexBy(this.dashboards.raw, 'id')
    const all_dashboards = builtins.concat(_(dashboards).sortBy('id').reverse().value())
    // Patch the non-comformant API response
    this.dashboards.list = _(all_dashboards).map(dashboard => {
      dashboard.charts = dashboard.charts || dashboard.dashboard_json
      return dashboard
    })
    .reject(_.isNull)
    .value()
    this.trigger(this.dashboards)
  },
  onFetchDashboardsFailed (error) { console.info('DashboardStore.onFetchDashboardsFailed')
    this.setState({ error: error })
  },

  // ===============================  Post Chart  ============================= //
  onPostDashboard () { console.info('DashboardStore.onPostDashboard')
    this.trigger(this.dashboards)
  },
  onPostDashboardCompleted (response) { console.info('DashboardStore.onPostDashboardCompleted')
    DashboardActions.fetchDashboards()
  },
  onPostDashboardFailed (error) { console.info('DashboardStore.onPostDashboardFailed')
    this.setState({ error: error })
  },

  // ===============================  Delete Dashboard  ============================ //
  onDeleteDashboard () { console.info('DashboardStore.onDeleteDashboard')
    this.trigger(this.dashboards)
  },
  onDeleteDashboardCompleted (response) { console.info('DashboardStore.onDeleteDashboardCompleted')
    DashboardActions.fetchDashboards()
  },
  onDeleteDashboardFailed (error) { console.info('DashboardStore.onDeleteDashboardFailed')
    this.setState({ error: error })
  }
})

export default DashboardStore
