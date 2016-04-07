import _ from 'lodash'
import uuid from 'uuid'
import moment from 'moment'
import Reflux from 'reflux'
import StateMixin from 'reflux-state-mixin'

import ChartActions from 'actions/ChartActions'
import DashboardPageActions from 'actions/DashboardPageActions'
import DatapointActions from 'actions/DatapointActions'
import DatapointStore from 'stores/DatapointStore'
import CampaignStore from 'stores/CampaignStore'
import LocationStore from 'stores/LocationStore'
import IndicatorStore from 'stores/IndicatorStore'
import DataExplorerStoreHelpers from 'stores/DataExplorerStoreHelpers'

import palettes from 'utilities/palettes'

class ChartState {
  constructor () {
    this.uuid = null
    this.type = 'RawData'
    this.title = ''
    this.data = null
    this.data_format = 'pct'
    this.groupBy = 'indicator'
    this.palette = 'traffic_light'
    this.selected_campaigns = []
    this.selected_indicators = []
    this.selected_locations = []
    this.end_date = moment().format('YYYY-MM-DD')
    this.start_date = moment().subtract(1, 'y').format('YYYY-MM-DD')
    this.features = []
    this.loading = false
    this.fetching = false
    this.linkedCampaigns = false
    this.selectTypeMode = true
  }
}

var DashboardPageStore = Reflux.createStore({
  mixins: [StateMixin.store],

  listenables: DashboardPageActions,

  dashboard: {
    title: '',
    charts: {}
  },

  init () {
    this.listenTo(DatapointStore, this.onDatapointStore)
    this.joinTrailing(LocationStore, IndicatorStore, CampaignStore, this.onGetInintialStores)
  },

  getInitialState () {
    return this.dashboard
  },

  // =========================================================================== //
  //                            REGULAR ACTION HANDLERS                          //
  // =========================================================================== //
  // =================================  Layout  ================================ //
  onToggleSelectTypeMode (uuid) {
    const chart = this.dashboard.charts[uuid]
    chart.selectTypeMode = !chart.selectTypeMode
    this.trigger(this.dashboard)
  },

  // =================================  Charts  ================================ //
  onAddChart () { // console.info('- Store.onAddChart')
    const new_chart = new ChartState()
    new_chart.uuid = uuid.v4()
    this.dashboard.charts[new_chart.uuid] = new_chart
    DashboardPageActions.setCampaigns(this.campaigns.raw[0], new_chart.uuid)
    this.trigger(this.dashboard)
  },
  onSelectChart (chart, uuid) { // console.info('- Store.onSelectChart')
    this.trigger(this.dashboard)
    const new_chart = this.meltChart(chart)
    this.dashboard.charts[new_chart.uuid] = new_chart
    delete this.dashboard.charts[uuid]
    DashboardPageActions.setType(new_chart.type, new_chart.uuid)
    this.trigger(this.dashboard)
  },
  onDuplicateChart (chart_uuid) { // console.info('- Store.onDuplicateChart')
    const chart = this.dashboard.charts[chart_uuid]
    const new_chart = Object.assign(new ChartState(), chart)
    new_chart.uuid = uuid.v4()
    new_chart.selected_indicators = chart.selected_indicators.slice(0)
    new_chart.selected_campaigns = chart.selected_campaigns.slice(0)
    new_chart.selected_locations = chart.selected_locations.slice(0)
    this.dashboard.charts[new_chart.uuid] = new_chart
    this.trigger(this.dashboard)
  },
  onRemoveChart (uuid) { // console.info('- Store.onRemoveChart')
    if (confirm('Are you sure you want to remove this chart?')) {
      delete this.dashboard.charts[uuid]
      this.trigger(this.dashboard)
    }
  },

  // =============================  Indicators  ============================ //
  onSetIndicators (indicators, uuid) { // console.info('- Store.onSetIndicators')
    this.toggleLoading(uuid)
    if (_.isNull(indicators)) {
      this.dashboard.charts[uuid].selected_indicators = []
    } else if (_.isArray(indicators)) {
      this.dashboard.charts[uuid].selected_indicators = indicators.map(ind => this.couldBeId(ind) ? this.indicators.index[ind] : ind)
    } else {
      this.dashboard.charts[uuid].selected_indicators = this.couldBeId(indicators) ? [this.indicators.index[indicators]] : [indicators]
    }
    this.updateChart(uuid)
  },
  onSelectIndicator (id, uuid) { // console.info('- Store.onSelectIndicator')
    this.toggleLoading(uuid)
    this.dashboard.charts[uuid].selected_indicators.push(this.indicators.index[id])
    this.updateChart(uuid)
  },
  onDeselectIndicator (id, uuid) { // console.info('- Store.onDeselectIndicator')
    this.toggleLoading(uuid)
    _.remove(this.dashboard.charts[uuid].selected_indicators, {id: id})
    this.updateChart(uuid)
  },
  onReorderIndicator (selected_indicators, uuid) { // console.info('- Store.onReorderIndicator')
    this.toggleLoading(uuid)
    this.dashboard.charts[uuid].selected_indicators = selected_indicators
    this.updateChart(uuid)
  },
  onClearSelectedIndicators (uuid) { // console.info('- Store.onClearSelectedIndicators')
    this.toggleLoading(uuid)
    this.dashboard.charts[uuid].selected_indicators = []
    this.updateChart(uuid)
  },

  // =============================  Locations  ============================ //
  onSetLocations (locations, uuid) { // console.info('- Store.onSetLocations')
    this.toggleLoading(uuid)
    if (_.isNull(locations)) {
      this.dashboard.charts[uuid].selected_locations = []
    } else if (_.isArray(locations)) {
      this.dashboard.charts[uuid].selected_locations = locations.map(location => this.couldBeId(location) ? this.locations.index[location] : location)
    } else {
      this.dashboard.charts[uuid].selected_locations = this.couldBeId(locations) ? [this.locations.index[locations]] : [locations]
    }
    this.updateChart(uuid)
  },
  onSelectLocation (id, uuid) { // console.info('- Store.onSelectLocation')
    this.toggleLoading(uuid)
    if (typeof id === 'string' && id.indexOf('lpd') > -1) {
      return this.addLocationsByLpdStatus(id, uuid)
    }
    this.dashboard.charts[uuid].selected_locations.push(this.locations.index[id])
    this.updateChart(uuid)
  },
  addLocationsByLpdStatus (id, uuid) {
    let locations_to_add = this.locations.lpd_statuses.find(lpd_status => lpd_status.value === id)
    locations_to_add.location_ids.forEach(location_id => {
      if (this.dashboard.charts[uuid].selected_locations.map(item => item.id).indexOf(location_id) >= 0) {
        return
      }
      this.dashboard.charts[uuid].selected_locations.push(this.locations.index[location_id])
    })
    this.updateChart(uuid)
  },
  onDeselectLocation (id, uuid) { // console.info('- Store.onDeselectLocation')
    this.toggleLoading(uuid)
    _.remove(this.dashboard.charts[uuid].selected_locations, {id: id})
    this.updateChart(uuid)
  },
  onClearSelectedLocations (uuid) { // console.info('- Store.onClearSelectedLocations')
    this.toggleLoading(uuid)
    this.dashboard.charts[uuid].selected_locations = []
    this.updateChart(uuid)
  },

  // =============================  Campaigns  ============================ //
  onSetCampaigns (campaigns, uuid) { // console.info('- Store.onSetCampaigns')
    this.toggleLoading(uuid)
    if (this.dashboard.charts[uuid].linkedCampaigns) {
      _.toArray(this.dashboard.charts).forEach(chart => {
        if (chart.linkedCampaigns) {
          this.assignCampaigns(campaigns, chart.uuid)
        }
        this.updateChart(chart.uuid)
      })
    } else {
      this.assignCampaigns(campaigns, uuid)
      this.updateChart(uuid)
    }
  },
  onSelectCampaign (id, uuid) { // console.info('- Store.onSelectCampaign')
    this.toggleLoading(uuid)
    this.dashboard.charts[uuid].selected_campaigns.push(this.campaigns.index[id])
    this.updateChart(uuid)
  },
  onDeselectCampaign (id, uuid) { // console.info('- Store.onDeselectCampaign')
    this.toggleLoading(uuid)
    _.remove(this.dashboard.charts[uuid].selected_campaigns, {id: id})
    this.updateChart(uuid)
  },
  onClearSelectedCampaigns (uuid) { // console.info('- Store.onClearSelectedCampaigns')
    this.toggleLoading(uuid)
    this.dashboard.charts[uuid].selected_campaigns = []
    this.updateChart(uuid)
  },
  onToggleCampaignLink (uuid) { // console.info('- Store.onToggleCampaignLink')
    this.toggleLoading(uuid)
    const current_chart = this.dashboard.charts[uuid]
    if (current_chart.linkedCampaigns) {
      current_chart.linkedCampaigns = false
      return this.trigger(this.dashboard)
    }
    _.toArray(this.dashboard.charts).forEach(chart => chart.linkedCampaigns = true)
    _.toArray(this.dashboard.charts).forEach(chart => DashboardPageActions.setCampaigns(current_chart.selected_campaigns, chart.uuid))
  },
  assignCampaigns (campaigns, uuid) {
    if (_.isArray(campaigns)) {
      this.dashboard.charts[uuid].selected_campaigns = campaigns.map(campaign => this.couldBeId(campaign) ? this.campaigns.index[campaign] : campaign)
    } else {
      this.dashboard.charts[uuid].selected_campaigns = this.couldBeId(campaigns) ? [this.campaigns.index[campaigns]] : [campaigns]
    }
    this.dashboard.charts[uuid].start_date = this.dashboard.charts[uuid].selected_campaigns[0].start_date
    this.dashboard.charts[uuid].end_date = this.dashboard.charts[uuid].selected_campaigns[0].end_date
    if (this.dashboard.charts[uuid].start_date === this.dashboard.charts[uuid].end_date) {
      this.dashboard.charts[uuid].start_date = moment(this.dashboard.charts[uuid].start_date).subtract(1, 'M').format('YYYY-MM-DD')
      this.dashboard.charts[uuid].end_date = moment(this.dashboard.charts[uuid].start_date).add(1, 'M').format('YYYY-MM-DD')
    }
  },

  // ============================  Chart Properties =========================== //
  onSetDateRange (key, value, uuid) { // console.info('- Store.onSetDateRange')
    this.toggleLoading(uuid)
    const full_key = key + '_date'
    this.dashboard.charts[uuid][full_key] = value
    this.updateChart(uuid)
  },
  onSetType (type, uuid) { // console.info('- Store.onSetType')
    this.toggleLoading(uuid)
    this.dashboard.charts[uuid].type = type
    this.dashboard.charts[uuid].selectTypeMode = false
    this.updateChart(uuid)
  },
  onSetPalette (palette, uuid) { // console.info('- Store.onSetPalette')
    this.dashboard.charts[uuid].palette = palette
    this.dashboard.charts[uuid].colors = palettes[palette]
    this.trigger(this.dashboard)
  },
  onSetGroupBy (grouping, uuid) { // console.info('- Store.onSetGroupBy')
    this.toggleLoading(uuid)
    this.dashboard.charts[uuid].groupBy = grouping
    this.dashboard.charts[uuid].selected_indicators = [this.dashboard.charts[uuid].selected_indicators[0]]
    this.dashboard.charts[uuid].selected_locations = [this.dashboard.charts[uuid].selected_locations[0]]
    this.updateChart(uuid)
  },
  onSetDashboardTitle (title) { // console.info('- Store.onSetDashboardTitle')
    this.dashboard.title = title
    this.trigger(this.dashboard)
  },
  onSetChartTitle (title, uuid) { // console.info('- Store.onSetChartTitle')
    this.dashboard.charts[uuid].title = title
    this.trigger(this.dashboard)
  },
  onSaveChart (uuid) { // console.info('- Store.saveChart')
    if (!this.dashboard.charts[uuid].title) {
      return window.alert('Please add a Title to your chart')
    }
    ChartActions.postChart({
      id: this.dashboard.charts[uuid].id,
      title: this.dashboard.charts[uuid].title,
      chart_json: JSON.stringify({
        type: this.dashboard.charts[uuid].type,
        start_date: this.dashboard.charts[uuid].start_date,
        end_date: this.dashboard.charts[uuid].end_date,
        campaign_ids: this.dashboard.charts[uuid].selected_campaigns.map(campaign => campaign.id),
        location_ids: this.dashboard.charts[uuid].selected_locations.map(location => location.id),
        indicator_ids: this.dashboard.charts[uuid].selected_indicators.map(indicator => indicator.id)
      })
    })
  },

  // =========================================================================== //
  //                               API CALL HANDLERS                             //
  // =========================================================================== //
  // =============================  Fetch Dashboard  =========================== //
  onFetchDashboard (uuid) { // console.info('Store.onFetchDashboard')
    // supposed to fetch dashboard?
    this.trigger(this.dashboard)
  },
  onFetchDashboardCompleted (response) { // console.info('Store.onFetchDashboardCompleted')
    this.dashboard.title = response.title
    response.charts.forEach(chart => {
      const new_chart = this.meltChart(chart)
      this.dashboard.charts[chart.uuid] = new_chart
      DashboardPageActions.setType(new_chart.type, new_chart.uuid)
    })
    this.trigger(this.dashboard)
  },
  onFetchDashboardFailed (error) { // console.info('Store.onFetchDashboardFailed')
    this.setState({ error: error })
  },

  // ============================  Fetch Map Features  ========================= //
  onFetchMapFeatures (uuid) {
    this.dashboard.charts[uuid].loading = true
    this.trigger(this.dashboard)
  },
  onFetchMapFeaturesCompleted (response) { // console.info('Store.onFetchMapFeaturesCompleted')
    const currently_fetching_charts = _.toArray(this.dashboard.charts).filter(chart => chart.fetching_map)
    const uuid = currently_fetching_charts[0].uuid
    this.dashboard.charts[uuid].features = response.objects.features
    this.dashboard.charts[uuid].loading = true
    this.dashboard.charts[uuid].fetching_map = false
    this.fetchDatapoints(uuid)
  },
  onFetchMapFeaturesFailed (error) {
    this.setState({ error: error })
  },

  // =========================================================================== //
  //                            OTHER STORE DEPENDECIES                          //
  // =========================================================================== //
  onGetInintialStores (locations, indicators, campaigns) {
    this.indicators = indicators[0]
    this.locations = locations[0]
    this.campaigns = campaigns[0]
  },

  onDatapointStore (datapoints) {
    // console.info('--- Store.onDatapointStore')
    const currently_fetching_charts = _.toArray(this.dashboard.charts).filter(chart => chart.fetching)
    const uuid = currently_fetching_charts[0].uuid

    if (_.isEmpty(datapoints.raw)) {
      this.dashboard.charts[uuid].data = []
      return this.trigger(this.dashboard)
    }
    this.dashboard.charts[uuid].datapoints = datapoints
    this.dashboard.charts[uuid].parent_location_map = _.indexBy(datapoints.meta.parent_location_map, 'name')
    this.dashboard.charts[uuid].default_sort_order = datapoints.meta.default_sort_order
    this.dashboard.charts[uuid] = this.formatChartByType(uuid)
    this.dashboard.charts[uuid].loading = false
    this.dashboard.charts[uuid].fetching = false
    this.trigger(this.dashboard)
  },

  // =========================================================================== //
  //                                   UTILITIES                                 //
  // =========================================================================== //
  meltChart (chart) {
    const new_chart = new ChartState()
    new_chart.id = chart.id
    new_chart.uuid = chart.uuid
    new_chart.title = chart.title
    new_chart.type = chart.chart_json.type
    new_chart.start_date = chart.chart_json.start_date
    new_chart.end_date = chart.chart_json.end_date
    new_chart.selected_indicators = chart.chart_json.indicator_ids.map(id => this.indicators.index[id])
    new_chart.selected_locations = chart.chart_json.location_ids.map(id => this.locations.index[id])
    new_chart.selected_campaigns = chart.chart_json.campaign_ids.map(id => this.campaigns.index[id])
    new_chart.selectTypeMode = false
    return new_chart
  },

  updateChart (uuid) { // console.info('-- Store.updateChart' + (this.chartParamsAreReady(uuid) ? ' (Params Ready!)' : ''))
    if (this.dashboard.charts[uuid].data !== null) {
      DatapointActions.clearDatapoints()
      this.dashboard.charts[uuid].data = null
      this.trigger(this.dashboard)
    }
    if (this.chartParamsAreReady(uuid)) {
      this.dashboard.charts[uuid].fetching = true
      if (this.dashboard.charts[uuid].type === 'ChoroplethMap' || this.dashboard.charts[uuid].type === 'MapChart') {
        this.dashboard.charts[uuid].fetching_map = true
        return DashboardPageActions.fetchMapFeatures(this.dashboard.charts[uuid].selected_locations.map(location => location.id))
      }
      this.fetchDatapoints(uuid)
    } else {
      this.dashboard.charts[uuid].loading = false
      this.trigger(this.dashboard)
    }
  },

  fetchDatapoints (uuid) {
    DatapointActions.fetchDatapoints({
      indicator_ids: this.dashboard.charts[uuid].selected_indicators.map(indicator => indicator.id),
      location_ids: this.dashboard.charts[uuid].selected_locations.map(location => location.id),
      start_date: this.dashboard.charts[uuid].start_date,
      end_date: this.dashboard.charts[uuid].end_date,
      type: this.dashboard.charts[uuid].type
    })
  },

  formatChartByType (uuid) { // console.info('---- Store.formatChartByType')
    const chart = this.dashboard.charts[uuid]
    const datapoints = this.dashboard.charts[uuid].datapoints.raw
    const melted_datapoints = this.melt(datapoints, chart.selected_indicators)
    const layout = 1 // hard coded for now
    if (chart.type === 'RawData') {
      chart.data = datapoints
      return chart
    } else if (chart.type === 'ChoroplethMap') {
      return DataExplorerStoreHelpers.formatChoroplethMap(melted_datapoints, chart, this.locations.index, this.indicators.index, layout)
    } else if (chart.type === 'TableChart') {
      return DataExplorerStoreHelpers.formatTableChart(datapoints, chart, this.locations.index, this.indicators.index)
    } else {
      chart.data = melted_datapoints
      return chart
    }
  },

  chartParamsAreReady (uuid) {
    const campaignsReady = !_.isEmpty(this.dashboard.charts[uuid].selected_campaigns)
    const selectedLocationsReady = !_.isEmpty(this.dashboard.charts[uuid].selected_locations)
    const selectedIndicatorsReady = !_.isEmpty(this.dashboard.charts[uuid].selected_indicators)
    const startDateReady = !_.isEmpty(this.dashboard.charts[uuid].start_date)
    const endDateReady = !_.isEmpty(this.dashboard.charts[uuid].end_date)
    return selectedLocationsReady && selectedIndicatorsReady && startDateReady && endDateReady && campaignsReady
  },

  melt (datapoints, selected_indicators) {
    const selected_indicator_ids = selected_indicators.map(_.property('id'))
    const baseIndicators = selected_indicator_ids.map(id => ({ indicator: id + '', value: 0 }))
    const melted_datapoints = _(datapoints).map(datapoint => {
      const base = _.omit(datapoint, 'indicators')
      const indicatorFullList = _.assign(_.cloneDeep(baseIndicators), datapoint.indicators)
      return indicatorFullList.map(indicator => _.assign({}, base, indicator))
    })
      .flatten()
      .value()
    melted_datapoints.forEach(melted_datapoint => {
      melted_datapoint.indicator = this.indicators.index[parseInt(melted_datapoint.indicator, 0)]
      melted_datapoint.location = this.locations.index[melted_datapoint.location]
    })
    return melted_datapoints
  },

  couldBeId (value) {
    return _.isNumber(value) || _.isString(value)
  },

  toggleLoading (uuid) { // console.info('Store.toggleLoading')
    this.dashboard.charts[uuid].loading = true
    this.trigger(this.dashboard)
  }

})

export default DashboardPageStore
