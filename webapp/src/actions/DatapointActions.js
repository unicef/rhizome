import _ from 'lodash'
import Reflux from 'reflux'
import api from 'utilities/api'

import builderDefinitions from 'components/d3chart/utils/builderDefinitions'

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
  const type = params.type
  const needsLocationChildren = _.indexOf(builderDefinitions.multi_location_charts, params.type) !== -1
  let query = {
    campaign__in: params.campaign__in || params.campaign_ids,
    indicator__in: params.indicator_ids,
    location_id__in: !needsLocationChildren || !type ? params.location_ids : null,
    campaign_start: params.start_date,
    campaign_end: params.end_date,
    chart_type: params.type,
    chart_uuid: params.uuid,
    show_missing_data: params.show_missing_data,
    group_by_time: params.group_by_time,
    source_name: params.source_name,
    parent_location_id__in: needsLocationChildren ? params.location_ids : null,
    filter_indicator: params.indicator_filter ? params.indicator_filter.type : null,
    filter_value: params.indicator_filter ? params.indicator_filter.value : null,
    location_level: type === 'TableChart' ? 'District' : null
  }

  return query
}

export default DatapointActions
