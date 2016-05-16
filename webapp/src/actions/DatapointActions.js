import Reflux from 'reflux'
import api from 'utilities/api'

const DatapointActions = Reflux.createActions({
  'fetchDatapoints': { children: ['completed', 'failed'], asyncResult: true },
  'clearDatapoints': 'clearDatapoints'
})

// API CALLS
// ---------------------------------------------------------------------------
DatapointActions.fetchDatapoints.listen(params => {
  const query = _prepDatapointsQuery(params)
  const fetch = api.endPoint('/datapoint/')
  DatapointActions.fetchDatapoints.promise(
    fetch(query, null, {'cache-control': 'no-cache'})
  )
})

// ACTION HELPERS
// ---------------------------------------------------------------------------
const _prepDatapointsQuery = (params) => {
  const type = params.type
  let query = {
    campaign__in: params.campaign__in || params.campaign_ids,
    indicator__in: params.indicator_ids,
    location_id__in: params.location_ids,
    location_depth: params.location_depth,
    campaign_start: params.start_date,
    campaign_end: params.end_date,
    chart_type: params.type,
    chart_uuid: params.uuid,
    show_missing_data: params.show_missing_data,
    group_by_time: params.group_by_time,
    source_name: params.source_name,
    filter_indicator: params.indicator_filter ? params.indicator_filter.type : null,
    filter_value: params.indicator_filter ? params.indicator_filter.value : null,
    location_level: type === 'TableChart' ? 'District' : null
  }

  return query
}

export default DatapointActions
