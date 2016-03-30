import Reflux from 'reflux'
import ChartAPI from 'data/requests/ChartAPI'
import api from 'data/api'

const ChartActions = Reflux.createActions({
  'fetchCharts': { children: ['completed', 'failed'] },
  'deleteChart': { children: ['completed', 'failed'] },
  'postChart': { children: ['completed', 'failed'] }
})

// API CALLS
// ---------------------------------------------------------------------------
ChartActions.fetchCharts.listenAndPromise(() => api.get_chart(null, null, {'cache-control': 'no-cache'}))
ChartActions.deleteChart.listenAndPromise(ChartAPI.deleteChart)
ChartActions.postChart.listen(chart_def => ChartActions.postChart.promise(api.post_chart(chart_def)))

export default ChartActions
