import Reflux from 'reflux'
import ChartAPI from 'data/requests/ChartAPI'
import api from 'data/api'

const ChartActions = Reflux.createActions({
  'fetchCharts': { children: ['completed', 'failed'], asyncResult: true },
  'fetchChart': { children: ['completed', 'failed'], asyncResult: true },
  'fetchChartDatapoints': { children: ['completed', 'failed'], asyncResult: true },
  'setSelectedLocations': 'setSelectedLocations',
  'setSelectedIndicators': 'setSelectedIndicators',
  'setSelectedCampaign': 'setSelectedCampaign'
})

// API CALLS
// ---------------------------------------------------------------------------
ChartActions.fetchCharts.listenAndPromise(() => {
  return ChartAPI.getCharts()
})

ChartActions.fetchChart.listen(chart_id => {
  ChartActions.fetchChart.promise(ChartAPI.getChart(chart_id))
})

ChartActions.fetchChartDatapoints.listen(chartDef => {
  const query = _prepDatapointsQuery(chartDef)
  ChartActions.fetchChartDatapoints.promise(api.datapoints(query))
})

// ACTION HELPERS
// ---------------------------------------------------------------------------
const _prepDatapointsQuery = (chartDef) => {
  let query = {
    indicator__in: chartDef.indicator_ids,
    campaign_start: chartDef.startDate,
    campaign_end: chartDef.endDate,
    chart_type: chartDef.type
  }

  if (chartDef.type === 'ChoroplethMap') {
    query['parent_location_id__in'] = chartDef.location_ids
  } else {
    query['location_id__in'] = chartDef.location_ids
  }
  return query
}

export default ChartActions
