import Reflux from 'reflux'

const DashboardPageActions = Reflux.createActions({
  'fetchDashboard': {children: ['completed', 'failed']}
})

export default DashboardPageActions
