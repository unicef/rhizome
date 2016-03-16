import Reflux from 'reflux'
import ChartAPI from 'data/requests/ChartAPI'

const ChartActions = Reflux.createActions({
  'fetchCharts': { children: ['completed', 'failed'], asyncResult: true },
  'fetchChart': { children: ['completed', 'failed'], asyncResult: true },
  'setPalette': 'setPalette',
  'setType': 'setType',
  'setTitle': 'setTitle',
  'setDateRange': 'setDateRange',
  'setIndicatorIds': 'setIndicatorIds',
  'setLocationIds': 'setLocationIds'
})

// API CALLS
// ---------------------------------------------------------------------------
ChartActions.fetchCharts.listenAndPromise(() => {
  return ChartAPI.getCharts()
})

ChartActions.fetchChart.listen(chart_id => {
  ChartActions.fetchChart.promise(ChartAPI.getChart(chart_id))
})

export default ChartActions
