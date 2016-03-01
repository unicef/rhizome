import Reflux from 'reflux'
import ChartAPI from 'data/requests/ChartAPI'

const ChartActions = Reflux.createActions({
  'prepChartData': 'prepChartData',
  'fetchCharts': { children: ['completed', 'failed'], asyncResult: true }
})

ChartActions.fetchCharts.listenAndPromise(() => {
  return ChartAPI.getCharts()
})

export default ChartActions
