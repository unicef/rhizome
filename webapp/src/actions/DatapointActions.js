import Reflux from 'reflux'
import api from 'data/api'

const DatapointActions = Reflux.createActions({
  'fetchDatapoints': { children: ['completed', 'failed'], asyncResult: true }
})

// API CALLS
// ---------------------------------------------------------------------------
DatapointActions.fetchDatapoints.listen(chartDef => {
  const query = _prepDatapointsQuery(chartDef)
  DatapointActions.fetchDatapoints.promise(api.datapoints(query))
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

export default DatapointActions
