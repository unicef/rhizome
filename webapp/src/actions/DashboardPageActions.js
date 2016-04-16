import Reflux from 'reflux'
import DashboardAPI from 'data/requests/DashboardAPI'
import ChartAPI from 'data/requests/ChartAPI'
import api from 'data/api'

const DashboardPageActions = Reflux.createActions({
  'fetchChart': { children: ['completed', 'failed'] }, // I think we can get rid of this
  'fetchDashboard': { children: ['completed', 'failed'] },
  'fetchMapFeatures': { children: ['completed', 'failed'] },
  'toggleCampaignLink': 'toggleCampaignLink',
  'toggleEditMode': 'toggleEditMode',
  'toggleChartEditMode': 'toggleChartEditMode',
  'toggleSelectTypeMode': 'toggleSelectTypeMode',
  // Dashboard Actions
  'setDashboardTitle': 'setDashboardTitle',
  'saveDashboard': 'saveDashboard',
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
  'setType': 'setType',
  'setDateRange': 'setDateRange',
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
DashboardPageActions.fetchChart.listenAndPromise(chart_id => ChartAPI.getChart(chart_id))
DashboardPageActions.fetchDashboard.listenAndPromise(dashboard_id => DashboardAPI.getDashboard(dashboard_id))

DashboardPageActions.fetchMapFeatures.listen(location_ids => {
  DashboardPageActions.fetchMapFeatures.promise(
    api.geo({parent_location_id__in: location_ids}, null, {'cache-control': 'max-age=604800, public'})
  )
})

export default DashboardPageActions
