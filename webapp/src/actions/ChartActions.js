import Reflux from 'reflux'
import ChartAPI from 'data/requests/ChartAPI'
import api from 'data/api'

const ChartActions = Reflux.createActions({
  'fetchCharts': { children: ['completed', 'failed'] },
  'fetchChart': { children: ['completed', 'failed'] },
  'fetchMapFeatures': { children: ['completed', 'failed'] },
  'postChart': { children: ['completed', 'failed'] },
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
ChartActions.fetchCharts.listenAndPromise(() => ChartAPI.getCharts())

ChartActions.fetchChart.listenAndPromise(chart_id => ChartAPI.getChart(chart_id))

ChartActions.postChart.listen(chart_def => {
  ChartActions.postChart.promise(api.post_chart(chart_def))
})

ChartActions.fetchMapFeatures.listen(location_ids => {
  ChartActions.fetchMapFeatures.promise(
    api.geo({parent_location_id__in: location_ids}, null, {'cache-control': 'max-age=604800, public'})
  )
})

export default ChartActions
