import Reflux from 'reflux'
import ChartAPI from 'data/requests/ChartAPI'
import api from 'data/api'

const ChartActions = Reflux.createActions({
  'fetchCharts': { children: ['completed', 'failed'], asyncResult: true },
  'fetchChart': { children: ['completed', 'failed'], asyncResult: true },
  'fetchMapFeatures': { children: ['completed', 'failed'], asyncResult: true },
  'saveChart': 'saveChart',
  'setPalette': 'setPalette',
  'setType': 'setType',
  'setTitle': 'setTitle',
  'setDateRange': 'setDateRange',
  'setIndicatorIds': 'setIndicatorIds',
  'setCampaignIds': 'setCampaignIds',
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

ChartActions.fetchMapFeatures.listen(location_ids => {
  ChartActions.fetchMapFeatures.promise(
    api.geo({parent_location_id__in: location_ids}, null, {'cache-control': 'max-age=604800, public'})
  )
})

export default ChartActions
