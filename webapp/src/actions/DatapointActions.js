import _ from 'lodash'
import Reflux from 'reflux'
import api from 'data/api'

import builderDefinitions from 'components/molecules/charts/utils/builderDefinitions'

const DatapointActions = Reflux.createActions({
  'fetchDatapoints': { children: ['completed', 'failed'], asyncResult: true },
  'clearDatapoints': 'clearDatapoints'
})

// API CALLS
// ---------------------------------------------------------------------------
DatapointActions.fetchDatapoints.listen(params => {
  console.log('params', params)
  const query = _prepDatapointsQuery(params)
  DatapointActions.fetchDatapoints.promise(api.datapoints(query))
})

// DatapointActions.fetchFilteredDatapoints.listen(chart_def => {
//   DatapointActions.fetchFilteredDatapoints.promise(
//     api.post_chart(chart_def)
//   )
// })
  // getFilteredDatapoints (options) {
  //   let fetch = api.endPoint('/datapoint/', 'get', 1)
  //   return new Promise(function (fulfill, reject) {
  //     fetch(options, null, {'cache-control': 'no-cache'}).then(datapoint => fulfill(datapoint))
  //   })
  // }

// ACTION HELPERS
// ---------------------------------------------------------------------------
const _prepDatapointsQuery = (params) => {
  const type = params.type
  const chartShowsOneCampaign = _.indexOf(builderDefinitions.single_campaign_charts, params.type) !== -1
  const needsChildrenLocations = type === 'MapChart' || type === 'BubbleMap' || type === 'TableChart'
  console.log('type', type)
  console.log('params', params)
  let query = {
    campaign__in: params.campaign__in,
    indicator__in: params.indicator_ids,
    location_id__in: !chartShowsOneCampaign || !type ? params.location_ids : null,
    campaign_start: params.start_date,
    campaign_end: params.end_date,
    chart_type: params.type,
    chart_uuid: params.uuid,
    show_missing_data: params.show_missing_data,
    source_name: params.source_name,
    parent_location_id__in: chartShowsOneCampaign ? params.location_ids : null,
    filter_indicator: params.indicator_filter ? params.indicator_filter.type : null,
    filter_value: params.indicator_filter ? params.indicator_filter.value : null,
    location_level: type === 'TableChart' ? 'District' : null
  }

  // if (needsChildrenLocations) {
  //   query['parent_location_id__in'] = params.location_ids
  // } else {
  //   query['location_id__in'] = params.location_ids || params.location_id__in
  // }

  console.log('query', query)
  return query
}

export default DatapointActions
