import Reflux from 'reflux'
import DashboardAPI from 'data/requests/DashboardAPI'

const DashboardPageActions = Reflux.createActions({
  'fetchDashboard': { children: ['completed', 'failed'] },
  'addRow': 'addRow',
  'removeChart': 'removeChart',
  'selectRowLayout': 'selectRowLayout',
  'toggleEditMode': 'toggleEditMode',
  'setDashboardTitle': 'setDashboardTitle',
  'saveDashboard': 'saveDashboard'
})

// API CALLS
// ---------------------------------------------------------------------------
DashboardPageActions.fetchDashboard.listenAndPromise(dashboard_id => DashboardAPI.getDashboard(dashboard_id))

export default DashboardPageActions
