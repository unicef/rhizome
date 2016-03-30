import Reflux from 'reflux'
import api from 'data/api'

const DashboardActions = Reflux.createActions({
  'fetchDashboards': { children: ['completed', 'failed'] },
  'postDashboard': { children: ['completed', 'failed'] },
  'initialize': 'initialize',
  'setDashboard': 'setDashboard',
  'navigate': 'navigate'
})

// API CALLS
// ---------------------------------------------------------------------------
DashboardActions.fetchDashboards.listenAndPromise(api.get_dashboard)
DashboardActions.postDashboard.listen(
	dashboard_def => DashboardActions.postDashboard.promise(api.post_dashboard(dashboard_def))
)

export default DashboardActions
