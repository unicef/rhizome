import Reflux from 'reflux'
import api from 'data/api'

const DatapointActions = Reflux.createActions({
  'fetchDatapoints': { children: ['completed', 'failed'], asyncResult: true },
  'clearDatapoints': 'clearDatapoints'
})

// API CALLS
// ---------------------------------------------------------------------------
DatapointActions.fetchDatapoints.listen(params => {
  const query = _prepDatapointsQuery(params)
  DatapointActions.fetchDatapoints.promise(api.datapoints(query))
})

// ACTION HELPERS
// ---------------------------------------------------------------------------
const _prepDatapointsQuery = (params) => {
  let query = {
    indicator__in: params.indicator_ids,
    campaign_start: params.start_date,
    campaign_end: params.end_date,
    chart_type: params.type,
    chart_uuid: params.uuid
  }

  const type = params.type
  const needsChildrenLocations = type === 'ChoroplethMap' || type === 'MapChart' || type === 'BubbleMap' || type === 'TableChart'

  if (needsChildrenLocations) {
    query['parent_location_id__in'] = params.location_ids
  } else {
    query['location_id__in'] = params.location_ids
  }

  if (type === 'TableChart') {
    query['location_level'] = 'District'
  }

  if (params.indicator_filter) {
    query['filter_indicator'] = params.indicator_filter.type
    query['filter_value'] = params.indicator_filter.value
  }

  return query
}

export default DatapointActions
