import Reflux from 'reflux'
import api from 'data/api'
import DashboardAPI from 'data/requests/DashboardAPI'

const DashboardActions = Reflux.createActions({
  'fetchDashboards': { children: ['completed', 'failed'] },
  'postDashboard': { children: ['completed', 'failed'] },
  'deleteDashboard': { children: ['completed', 'failed'] }
})

// API CALLS
// ---------------------------------------------------------------------------
DashboardActions.fetchDashboards.listenAndPromise(api.get_dashboard)
DashboardActions.deleteDashboard.listenAndPromise(DashboardAPI.deleteDashboard)
DashboardActions.postDashboard.listen(
	dashboard_def => DashboardActions.postDashboard.promise(api.post_dashboard(dashboard_def))
)

export default DashboardActions
