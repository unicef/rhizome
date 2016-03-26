import Reflux from 'reflux'
import ChartAPI from 'data/requests/ChartAPI'
import api from 'data/api'

const DataExplorerActions = Reflux.createActions({
  'fetchChart': { children: ['completed', 'failed'] },
  'fetchMapFeatures': { children: ['completed', 'failed'] },
  'getChart': 'getChart',
  'saveChart': 'saveChart',
  // Chart Params
  'setTitle': 'setTitle',
  'setPalette': 'setPalette',
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
DataExplorerActions.fetchChart.listenAndPromise(chart_id => ChartAPI.getChart(chart_id))

DataExplorerActions.fetchMapFeatures.listen(location_ids => {
  DataExplorerActions.fetchMapFeatures.promise(
    api.geo({parent_location_id__in: location_ids}, null, {'cache-control': 'max-age=604800, public'})
  )
})

export default DataExplorerActions
