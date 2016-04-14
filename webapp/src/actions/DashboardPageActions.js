import Reflux from 'reflux'
import DashboardAPI from 'data/requests/DashboardAPI'

const DashboardPageActions = Reflux.createActions({
  'fetchDashboard': { children: ['completed', 'failed'] },
  'toggleEditMode': 'toggleEditMode',
  'setDashboardTitle': 'setDashboardTitle',
  'saveDashboard': 'saveDashboard'
})

// API CALLS
// ---------------------------------------------------------------------------
DashboardPageActions.fetchDashboard.listenAndPromise(dashboard_id => DashboardAPI.getDashboard(dashboard_id))

export default DashboardPageActions
