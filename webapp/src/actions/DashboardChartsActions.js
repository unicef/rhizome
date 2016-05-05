import Reflux from 'reflux'
import api from 'data/api'

const DashboardChartsActions = Reflux.createActions({
  'fetchChart': { children: ['completed', 'failed'] }, // I think we can get rid of this
  'fetchMapFeatures': { children: ['completed', 'failed'] },
  'toggleCampaignLink': 'toggleCampaignLink',
  'toggleChartEditMode': 'toggleChartEditMode',
  'exitEditMode': 'exitEditMode',
  'exitSelectTypeMode': 'exitSelectTypeMode',
  'toggleSelectTypeMode': 'toggleSelectTypeMode',
  // Dashboard Actions
  'addChart': 'addChart',
  'selectChart': 'selectChart',
  'duplicateChart': 'duplicateChart',
  'removeChart': 'removeChart',
  'getChart': 'getChart',
  'saveChart': 'saveChart',
  // Chart Params
  'setChartTitle': 'setChartTitle',
  'setPalette': 'setPalette',
  'setGroupBy': 'setGroupBy',
  'setGroupByTime': 'setGroupByTime',
  'setType': 'setType',
  'setDateRange': 'setDateRange',
  'setIndicatorFilter': 'setIndicatorFilter',
  'setIndicatorColor': 'setIndicatorColor',
  'updateTypeParams': 'updateTypeParams',
  // Locations
  'setLocations': 'setLocations',
  'selectLocation': 'selectLocation',
  'deselectLocation': 'deselectLocation',
  'clearSelectedLocations': 'clearSelectedLocations',
  // Indicators
  'setIndicators': 'setIndicators',
  'selectIndicator': 'selectIndicator',
  'deselectIndicator': 'deselectIndicator',
  'reorderIndicator': 'reorderIndicator',
  'clearSelectedIndicators': 'clearSelectedIndicators',
  // Campaigns
  'setCampaigns': 'setCampaigns',
  'selectCampaign': 'selectCampaign',
  'deselectCampaign': 'deselectCampaign',
  'clearSelectedCampaigns': 'clearSelectedCampaigns'
})

// API CALLS
// ---------------------------------------------------------------------------
DashboardChartsActions.fetchChart.listenAndPromise(chart_id => {
  const fetch = api.endPoint('/custom_chart/' + chart_id, 'GET', 1)
  return fetch(null, null, {'cache-control': 'no-cache'})
})

DashboardChartsActions.fetchMapFeatures.listen(location_ids => {
  DashboardChartsActions.fetchMapFeatures.promise(
    api.geo({parent_location_id__in: location_ids}, null, {'cache-control': 'max-age=604800, public'})
  )
})

export default DashboardChartsActions
