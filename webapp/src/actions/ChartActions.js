import Reflux from 'reflux'
import api from 'data/api'

const ChartActions = Reflux.createActions({
  'fetchCharts': { children: ['completed', 'failed'] },
  'deleteChart': { children: ['completed', 'failed'] },
  'postChart': { children: ['completed', 'failed'] }
})

// API CALLS
// ---------------------------------------------------------------------------
ChartActions.postChart.listenAndPromise(api.post_chart)
ChartActions.fetchCharts.listenAndPromise(() => api.get_chart(null, null, {'cache-control': 'no-cache'}))
ChartActions.deleteChart.listenAndPromise(chart_id => {
  const fetch = api.endPoint('/custom_chart/' + chart_id, 'delete', 1)
  return fetch(null, null, {'cache-control': 'no-cache'})
})

export default ChartActions
