import Reflux from 'reflux'
import api from 'data/api'

const DashboardActions = Reflux.createActions({
  'fetchDashboards': { children: ['completed', 'failed'] },
  'postDashboard': { children: ['completed', 'failed'] },
  'deleteDashboard': { children: ['completed', 'failed'] }
})

// API CALLS
// ---------------------------------------------------------------------------
DashboardActions.fetchDashboards.listenAndPromise(api.get_dashboard)
DashboardActions.deleteDashboard.listenAndPromise(dashboard_id => {
  const fetch = api.endPoint('/custom_dashboard/' + dashboard_id, 'delete', 1)
  return fetch(null, null, {'cache-control': 'no-cache'})
})
DashboardActions.postDashboard.listen(
	dashboard_def => DashboardActions.postDashboard.promise(api.post_dashboard(dashboard_def))
)

export default DashboardActions
