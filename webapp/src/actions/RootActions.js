import Reflux from 'reflux'
import api from 'data/api'

const RootActions = Reflux.createActions({
  'fetchAllCharts': { children: ['completed', 'failed'] },
  'fetchAllDashboards': { children: ['completed', 'failed'] }
})

// API CALLS
// ---------------------------------------------------------------------------
RootActions.fetchAllCharts.listenAndPromise(() => api.get_chart(null, null, {'cache-control': 'no-cache'}))
RootActions.fetchAllDashboards.listenAndPromise(api.get_dashboard)

export default RootActions
