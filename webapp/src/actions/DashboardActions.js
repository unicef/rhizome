import Reflux from 'reflux'
import api from 'data/api'

const DashboardActions = Reflux.createActions({
  'fetchDashboards': { children: ['completed', 'failed'] },
  'initialize': 'initialize',
  'setDashboard': 'setDashboard',
  'navigate': 'navigate'
})

// API CALLS
// ---------------------------------------------------------------------------
DashboardActions.fetchDashboards.listenAndPromise(api.get_dashboard)

export default DashboardActions
