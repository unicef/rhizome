import Reflux from 'reflux'
import ChartAPI from 'data/requests/ChartAPI'

const ChartActions = Reflux.createActions({
  'fetchCharts': { children: ['completed', 'failed'] }
})

// API CALLS
// ---------------------------------------------------------------------------
ChartActions.fetchCharts.listenAndPromise(() => ChartAPI.getCharts())

export default ChartActions
