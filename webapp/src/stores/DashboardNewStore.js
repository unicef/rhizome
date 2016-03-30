import _ from 'lodash'
import uuid from 'uuid'
import moment from 'moment'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'

import ChartActions from 'actions/ChartActions'
import DashboardNewActions from 'actions/DashboardNewActions'
import DatapointActions from 'actions/DatapointActions'
import format from 'utilities/format'
import DatapointStore from 'stores/DatapointStore'
import CampaignStore from 'stores/CampaignStore'
import LocationStore from 'stores/LocationStore'
import IndicatorStore from 'stores/IndicatorStore'
import DataExplorerStoreHelpers from 'stores/DataExplorerStoreHelpers'

import palettes from 'components/molecules/charts/utils/palettes'

class ChartState {
  constructor () {
    this.uuid = null
    this.type = 'RawData'
    this.title = 'Untitled'
    this.data = null
    this.data_format = 'pct'
    this.selected_campaigns = []
    this.selected_indicators = []
    this.selected_locations = []
    this.end_date = moment().format('YYYY-MM-DD')
    this.start_date = moment().subtract(1, 'y').format('YYYY-MM-DD')
    this.features = []
    this.loading = false
    this.fetching = false
  }
}

var DashboardNewStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: DashboardNewActions,

  chart_template: {
    uuid: null,
    type: 'RawData',
    title: 'Untitled',
    data: null,
    data_format: 'pct',
    selected_campaigns: [],
    selected_indicators: [],
    selected_locations: [],
    end_date: moment().format('YYYY-MM-DD'),
    start_date: moment().subtract(1, 'y').format('YYYY-MM-DD'),
    features: [],
    loading: false,
    fetching: false,
    fetching_map: false,
  },

  charts: {},

  init () {
    this.listenTo(DatapointStore, this.onDatapointStore)
    this.joinTrailing(LocationStore, IndicatorStore, CampaignStore, this.onGetInintialStores)
  },

  getInitialState () {
    return this.charts
  },

  // =========================================================================== //
  //                            REGULAR ACTION HANDLERS                          //
  // =========================================================================== //
  // =================================  Charts  ================================ //
  onAddChart (type) { console.info('- Store.onAddChart')
    const new_chart = new ChartState
    new_chart.type = type
    new_chart.title = format.unCamelCase(type)
    new_chart.uuid = uuid.v4()
    this.charts[new_chart.uuid] = new_chart
    DashboardNewActions.setCampaigns(this.campaigns.raw[0], new_chart.uuid)
    this.trigger(this.charts)
  },
  onRemoveChart (uuid) { console.info('- Store.onRemoveChart')
    if (confirm('Are you sure you want to remove this chart?')) {
      delete this.charts[uuid]
      this.trigger(this.charts)
    }
  },

  // =============================  Indicators  ============================ //
  onSetIndicators (indicators, uuid) { console.info('- Store.onSetIndicators')
    this.toggleLoading(uuid)
    if (_.isNull(indicators)) {
      this.charts[uuid].selected_indicators = []
    } else if (_.isArray(indicators)) {
      this.charts[uuid].selected_indicators = indicators.map(ind => this.couldBeId(ind) ? this.indicators.index[ind] : ind)
    } else {
      this.charts[uuid].selected_indicators = this.couldBeId(indicators) ? [this.indicators.index[indicators]] : [indicators]
    }
    this.updateChart(uuid)
  },
  onSelectIndicator (id, uuid) { console.info('- Store.onSelectIndicator')
    this.toggleLoading(uuid)
    this.charts[uuid].selected_indicators.push(this.indicators.index[id])
    this.updateChart(uuid)
  },
  onDeselectIndicator (id, uuid) { console.info('- Store.onDeselectIndicator')
    this.toggleLoading(uuid)
    _.remove(this.charts[uuid].selected_indicators, {id: id})
    this.updateChart(uuid)
  },
  onReorderIndicator (selected_indicators, uuid) { console.info('- Store.onReorderIndicator')
    this.toggleLoading(uuid)
    this.charts[uuid].selected_indicators = selected_indicators
    this.updateChart(uuid)
  },
  onClearSelectedIndicators (uuid) { console.info('- Store.onClearSelectedIndicators')
    this.toggleLoading(uuid)
    this.charts[uuid].selected_indicators = []
    this.updateChart(uuid)
  },

  // =============================  Locations  ============================ //
  onSetLocations (locations, uuid) { console.info('- Store.onSetLocations')
    this.toggleLoading(uuid)
    if (_.isNull(locations)) {
      this.charts[uuid].selected_locations = []
    } else if (_.isArray(locations)) {
      this.charts[uuid].selected_locations = locations.map(location => this.couldBeId(location) ? this.locations.index[location] : location)
    } else {
      this.charts[uuid].selected_locations = this.couldBeId(locations) ? [this.locations.index[locations]] : [locations]
    }
    this.updateChart(uuid)
  },
  onSelectLocation (id, uuid) {console.info('- Store.onSelectLocation')
    this.toggleLoading(uuid)
    if (typeof id === 'string' && id.indexOf('lpd') > -1) {
      return this.addLocationsByLpdStatus(id)
    }
    this.charts[uuid].selected_locations.push(this.locations.index[id])
    this.updateChart(uuid)
  },
  addLocationsByLpdStatus (uuid) {
    let locations_to_add = this.locations.lpd_statuses.find(lpd_status => lpd_status.value === index)
    locations_to_add.location_ids.forEach(location_id => {
      if (this.charts[uuid].selected_locations.map(item => item.id).indexOf(location_id) >= 0) {
        return
      }
      this.charts[uuid].selected_locations.push(this.locations.index[location_id])
    })
    this.updateChart(uuid)
  },
  onDeselectLocation (id, uuid) {console.info('- Store.onDeselectLocation')
    this.toggleLoading(uuid)
    _.remove(this.charts[uuid].selected_locations, {id: id})
    this.updateChart(uuid)
  },
  onClearSelectedLocations (uuid) {console.info('- Store.onClearSelectedLocations')
    this.toggleLoading(uuid)
    this.charts[uuid].selected_locations = []
    this.updateChart(uuid)
  },

  // =============================  Campaigns  ============================ //
  onSetCampaigns (campaigns, uuid) {console.info('- Store.onSetCampaigns')
    this.toggleLoading(uuid)
    if (_.isArray(campaigns)) {
      this.charts[uuid].selected_campaigns = campaigns.map(campaign => this.couldBeId(campaign) ? this.campaigns.index[campaign] : campaign)
    } else {
      this.charts[uuid].selected_campaigns = this.couldBeId(campaigns) ? [this.campaigns.index[campaigns]] : [campaigns]
    }
    this.charts[uuid].start_date = this.charts[uuid].selected_campaigns[0].start_date
    this.charts[uuid].end_date = this.charts[uuid].selected_campaigns[0].end_date
    if (this.charts[uuid].start_date === this.charts[uuid].end_date) {
      this.charts[uuid].start_date = moment(this.charts[uuid].start_date).subtract(1, 'M').format('YYYY-MM-DD')
      this.charts[uuid].end_date = moment(this.charts[uuid].start_date).add(1, 'M').format('YYYY-MM-DD')
    }
    this.updateChart(uuid)
  },
  onSelectCampaign (id, uuid) { console.info('- Store.onSelectCampaign')
    this.toggleLoading(uuid)
    this.charts[uuid].selected_campaigns.push(this.campaigns.index[id])
    this.updateChart(uuid)
  },
  onDeselectCampaign (id, uuid) { console.info('- Store.onDeselectCampaign')
    this.toggleLoading(uuid)
    _.remove(this.charts[uuid].selected_campaigns, {id: id})
    this.updateChart(uuid)
  },
  onClearSelectedCampaigns (uuid) { console.info('- Store.onClearSelectedCampaigns')
    this.toggleLoading(uuid)
    this.charts[uuid].selected_campaigns = []
    this.updateChart(uuid)
  },

  // ============================  Chart Properties =========================== //
  onSetDateRange (key, value, uuid) { console.info('- Store.onSetDateRange')
    const full_key = key + '_date'
    this.charts[uuid][full_key] = value
    this.updateChart(uuid)
  },
  onSetType (type, uuid) { console.info('- Store.onSetType')
    this.toggleLoading(uuid)
    this.charts[uuid].type = type
    this.updateChart(uuid)
  },
  onSetPalette (palette, uuid) { console.info('- Store.onSetPalette')
    this.charts[uuid].palette = palette
    this.charts[uuid].colors = palettes[palette]
    this.trigger(this.charts)
  },
  onSetTitle (title, uuid) { console.info('- Store.onSetTitle')
    this.charts[uuid].title = title
    this.trigger(this.charts)
  },
  onSaveChart (uuid) { console.info('- Store.saveChart')
    if (!this.charts[uuid].title) {
      return window.alert('Please add a Title to your chart')
    }
    ChartActions.postChart({
      id: this.charts[uuid].id,
      title: this.charts[uuid].title,
      chart_json: JSON.stringify({
        type: this.charts[uuid].type,
        start_date: this.charts[uuid].start_date,
        end_date: this.charts[uuid].end_date,
        campaign_ids: this.charts[uuid].selected_campaigns.map(campaign => campaign.id),
        location_ids: this.charts[uuid].selected_locations.map(location => location.id),
        indicator_ids: this.charts[uuid].selected_indicators.map(indicator => indicator.id)
      })
    })
  },

  // =========================================================================== //
  //                               API CALL HANDLERS                             //
  // =========================================================================== //
  // ============================  Fetch Map Features  ========================= //
  onFetchMapFeatures (uuid) {
    this.charts[uuid].loading = true
    this.trigger(this.charts)
  },
  onFetchMapFeaturesCompleted (response) {
    const currently_fetching_charts = _.toArray(this.charts).filter(chart => chart.fetching_map)
    const uuid = currently_fetching_charts[0].uuid
    this.charts[uuid].features = response.objects.features
    this.charts[uuid].loading = true
    this.charts[uuid].fetching_map = false
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
    console.info('--- Store.onDatapointStore')
    const currently_fetching_charts = _.toArray(this.charts).filter(chart => chart.fetching)
    const uuid = currently_fetching_charts[0].uuid

    if (_.isEmpty(datapoints.raw)) {
      this.charts[uuid].data = []
      return this.trigger(this.charts)
    }
    this.datapoints = datapoints
    this.charts[uuid].parent_location_map = _.indexBy(datapoints.meta.parent_location_map, 'name')
    this.charts[uuid].default_sort_order = datapoints.meta.default_sort_order
    this.charts[uuid] = this.formatChartByType(uuid)
    this.charts[uuid].loading = false
    this.charts[uuid].fetching = false
    this.trigger(this.charts)
  },

  // =========================================================================== //
  //                                   UTILITIES                                 //
  // =========================================================================== //
  updateChart (uuid) {  console.info('-- Store.updateChart' + (this.chartParamsAreReady(uuid) ? ' (Params Ready!)' : ''))
    if (this.charts[uuid].data !== null) {
      DatapointActions.clearDatapoints()
      this.charts[uuid].data = null
      this.trigger(this.charts)
    }
    if (this.chartParamsAreReady(uuid)) {
      this.charts[uuid].fetching = true
      if (this.charts[uuid].type === 'ChoroplethMap') {
        this.charts[uuid].fetching_map = true
        DashboardNewActions.fetchMapFeatures(this.charts[uuid].selected_locations.map(location => location.id))
      }
      DatapointActions.fetchDatapoints({
        indicator_ids: this.charts[uuid].selected_indicators.map(indicator => indicator.id),
        location_ids: this.charts[uuid].selected_locations.map(location => location.id),
        start_date: this.charts[uuid].start_date,
        end_date: this.charts[uuid].end_date,
        type: this.charts[uuid].type
      })
    } else {
      this.charts[uuid].loading = false
      this.trigger(this.charts)
    }
  },

  formatChartByType (uuid) {  console.info('---- Store.formatChartByType')
    const chart = this.charts[uuid]
    const datapoints = this.datapoints.raw
    if (chart.type === 'RawData') {
      chart.data = datapoints
      return chart
    }
    const selected_locations_index = _.indexBy(this.charts[uuid].selected_locations, 'id')
    const selected_indicators_index = _.indexBy(this.charts[uuid].selected_indicators, 'id')
    const groups = chart.groupBy === 'indicator' ? selected_indicators_index : selected_locations_index
    const layout = 1 // hard coded for now
    const melted_datapoints = this.melt(datapoints, this.charts[uuid].selected_indicators)

    switch (chart.type) {
      case 'LineChart':
        return DataExplorerStoreHelpers.formatLineChart(melted_datapoints, chart, groups, layout)
      // case 'PieChart':
        // return DataExplorerStoreHelpers.formatPieChart(melted_datapoints, this.charts[uuid].selected_indicators, layout)
      case 'ChoroplethMap':
        return DataExplorerStoreHelpers.formatChoroplethMap(melted_datapoints, chart, this.locations.index, this.indicators.index, layout)
      // case 'ColumnChart':
        // return DataExplorerStoreHelpers.formatColumnChart(melted_datapoints, lower, upper, groups, chart, layout)
      // case 'ScatterChart':
        // return DataExplorerStoreHelpers.formatScatterChart(datapoints, selected_locations_index, selected_indicators_index, chart, layout)
      // case 'BarChart':
        // return DataExplorerStoreHelpers.formatBarChart(datapoints, selected_locations_index, selected_indicators_index, chart, layout)
      case 'TableChart':
        return DataExplorerStoreHelpers.formatTableChart(datapoints, chart, this.locations.index, this.indicators.index)
      default:
    }
  },

  chartParamsAreReady (uuid) {
    const campaignsReady = !_.isEmpty(this.charts[uuid].selected_campaigns)
    const selectedLocationsReady = !_.isEmpty(this.charts[uuid].selected_locations)
    const selectedIndicatorsReady = !_.isEmpty(this.charts[uuid].selected_indicators)
    const startDateReady = !_.isEmpty(this.charts[uuid].start_date)
    const endDateReady = !_.isEmpty(this.charts[uuid].end_date)
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

  toggleLoading (uuid) { console.log('Store.toggleLoading')
    this.charts[uuid].loading = true
    this.trigger(this.charts)
  }

})

export default DashboardNewStore
