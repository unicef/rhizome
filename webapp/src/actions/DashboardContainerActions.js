import Reflux from 'reflux'
import api from 'utilities/api'

const DashboardContainerActions = Reflux.createActions({
  'fetchDashboard': { children: ['completed', 'failed'] },
  'addRow': 'addRow',
  'moveRowUp': 'moveRowUp',
  'moveRowDown': 'moveRowDown',
  'setCampaign': 'setCampaign',
  'setLocation': 'setLocation',
  'setIndicatorFilter': 'setIndicatorFilter',
  'selectChart': 'selectChart',
  'removeChart': 'removeChart',
  'selectRowLayout': 'selectRowLayout',
  'toggleEditMode': 'toggleEditMode',
  'setDashboardTitle': 'setDashboardTitle',
  'saveDashboard': 'saveDashboard'
})

// API CALLS
// ---------------------------------------------------------------------------
DashboardContainerActions.fetchDashboard.listenAndPromise(dashboard_id => {
  const fetch = api.endPoint('/custom_dashboard/' + dashboard_id, 'GET', 1)
  return fetch(null, null, {'cache-control': 'no-cache'})
})

export default DashboardContainerActions
