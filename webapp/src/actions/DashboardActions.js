import Reflux from 'reflux'
import api from 'utilities/api'

const DashboardActions = Reflux.createActions({
  'fetchDashboards': { children: ['completed', 'failed'] },
  'postDashboard': { children: ['completed', 'failed'] },
  'deleteDashboard': { children: ['completed', 'failed'] }
})

// API CALLS
// ---------------------------------------------------------------------------
DashboardActions.fetchDashboards.listenAndPromise(api.get_dashboard)
DashboardActions.postDashboard.listenAndPromise(api.post_dashboard)
DashboardActions.deleteDashboard.listenAndPromise(dashboard_id => {
  const fetch = api.endPoint('/custom_dashboard/' + dashboard_id, 'delete', 1)
  return fetch(null, null, {'cache-control': 'no-cache'})
})

export default DashboardActions
