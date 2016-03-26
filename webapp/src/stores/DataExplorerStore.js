import _ from 'lodash'
import moment from 'moment'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'

import DataExplorerActions from 'actions/DataExplorerActions'
import DatapointActions from 'actions/DatapointActions'
import builderDefinitions from 'components/molecules/charts/utils/builderDefinitions'
import DatapointStore from 'stores/DatapointStore'
import CampaignStore from 'stores/CampaignStore'
import LocationStore from 'stores/LocationStore'
import IndicatorStore from 'stores/IndicatorStore'
import DataExplorerStoreHelpers from 'stores/DataExplorerStoreHelpers'

import palettes from 'components/molecules/charts/utils/palettes'

var DataExplorerStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: DataExplorerActions,

  chart: {
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
    countries: [],
    headers: [],
    parent_location_map: null,
    cellSize: 36,
    fontSize: 14,
    margin: { top: 40, right: 40, bottom: 40, left: 40 },
    cellFontSize: 14,
    colors: palettes['traffic_light'],
    groupBy: 'indicator',
    locationLevelValue: _.findIndex(builderDefinitions.locationLevels, {value: 'sublocations'}),
    timeRange: null,
    default_sort_order: null,
    x: 0,
    xFormat: ',.0f',
    y: 0,
    yFormat: ',.0f',
    z: 0,
    loading: false
  },

  init () {
    this.listenTo(DatapointStore, this.onDatapointStore)
    this.joinTrailing(LocationStore, IndicatorStore, CampaignStore, this.onGetInintialStores)
  },

  getInitialState () {
    return this.chart
  },

  // =========================================================================== //
  //                               API CALL HANDLERS                             //
  // =========================================================================== //
  // ==============================  Fetch Chart  =========================== //
  onFetchChart (id) {
    this.setState({ data: null, loading: true })
  },
  onFetchChartCompleted (response) {
    const chart_json = typeof response.chart_json === 'string' ? JSON.parse(response.chart_json) : response.chart_json
    this.chart.id = response.id
    this.chart.title = response.title
    this.chart.type = chart_json.type
    this.chart.start_date = chart_json.start_date
    this.chart.end_date = chart_json.end_date
    this.chart.selected_indicators = chart_json.indicator_ids.map(id => this.indicators.index[id])
    this.chart.selected_locations = chart_json.location_ids.map(id => this.locations.index[id])
    this.chart.selected_campaigns = chart_json.campaign_ids.map(id => this.campaigns.index[id])
    this.chart.loading = false
    this.updateChart()
  },
  onFetchChartFailed (error) {
    this.setState({ error: error })
  },

  // ============================  Fetch Map Features  ========================= //
  onFetchMapFeatures () {
    this.setState({ loading: true })
  },
  onFetchMapFeaturesCompleted (response) {
    this.chart.features = response.objects.features
  },
  onFetchMapFeaturesFailed (error) {
    this.setState({ error: error })
  },

  // =========================================================================== //
  //                            REGULAR ACTION HANDLERS                          //
  // =========================================================================== //
  onSetDateRange (key, value) {
    console.info('- Store.onSetDateRange')
    const full_key = key + '_date'
    this.chart.def[full_key] = value
    this.updateChart()
  },

  // =============================  Indicators  ============================ //
  onSetIndicators (indicators) {
    console.info('- Store.onSetIndicators')
    this.toggleLoading()
    if (_.isNull(indicators)) {
      this.chart.selected_indicators = []
    } else if (_.isArray(indicators)) {
      this.chart.selected_indicators = indicators.map(ind => this.couldBeId(ind) ? this.indicators.index[ind] : ind)
    } else {
      this.chart.selected_indicators = this.couldBeId(indicators) ? [this.indicators.index[indicators]] : [indicators]
    }
    this.updateChart()
  },
  onSelectIndicator (id) {
    console.info('- Store.onSelectIndicator')
    this.toggleLoading()
    this.chart.selected_indicators.push(this.indicators.index[id])
    this.updateChart()
  },
  onDeselectIndicator (id) {
    console.info('- Store.onDeselectIndicator')
    this.toggleLoading()
    _.remove(this.chart.selected_indicators, {id: id})
    this.updateChart()
  },
  onReorderIndicator (selected_indicators) {
    console.info('- Store.onReorderIndicator')
    this.toggleLoading()
    this.chart.selected_indicators = selected_indicators
    this.updateChart()
  },
  onClearSelectedIndicators () {
    console.info('- Store.onClearSelectedIndicators')
    this.toggleLoading()
    this.chart.selected_indicators = []
    this.updateChart()
  },

  // =============================  Locations  ============================ //
  onSetLocations (locations) {
    console.info('- Store.onSetLocations')
    this.toggleLoading()
    if (_.isNull(locations)) {
      this.chart.selected_locations = []
    } else if (_.isArray(locations)) {
      this.chart.selected_locations = locations.map(location => this.couldBeId(location) ? this.locations.index[location] : location)
    } else {
      this.chart.selected_locations = this.couldBeId(locations) ? [this.locations.index[locations]] : [locations]
    }
    this.updateChart()
  },
  onSelectLocation (id) {
    console.info('- Store.onSelectLocation')
    this.toggleLoading()
    if (typeof id === 'string' && id.indexOf('lpd') > -1) {
      return this.addLocationsByLpdStatus(id)
    }
    this.chart.selected_locations.push(this.locations.index[id])
    this.updateChart()
  },
  addLocationsByLpdStatus (index) {
    let locations_to_add = this.locations.lpd_statuses.find(lpd_status => lpd_status.value === index)
    locations_to_add.location_ids.forEach(location_id => {
      if (this.chart.selected_locations.map(item => item.id).indexOf(location_id) >= 0) {
        return
      }
      this.chart.selected_locations.push(this.locations.index[location_id])
    })
    this.updateChart()
  },
  onDeselectLocation (id) {
    console.info('- Store.onDeselectLocation')
    this.toggleLoading()
    _.remove(this.chart.selected_locations, {id: id})
    this.updateChart()
  },
  onClearSelectedLocations () {
    console.info('- Store.onClearSelectedLocations')
    this.toggleLoading()
    this.chart.selected_locations = []
    this.updateChart()
  },

  // =============================  Campaigns  ============================ //
  onSetCampaigns (campaigns) {
    console.info('- Store.onSetCampaigns')
    this.toggleLoading()
    if (_.isArray(campaigns)) {
      this.chart.selected_campaigns = campaigns.map(campaign => this.couldBeId(campaign) ? this.campaigns.index[campaign] : campaign)
    } else {
      this.chart.selected_campaigns = this.couldBeId(campaigns) ? [this.campaigns.index[campaigns]] : [campaigns]
    }
    this.chart.start_date = this.chart.selected_campaigns[0].start_date
    this.chart.end_date = this.chart.selected_campaigns[0].end_date
    if (this.chart.start_date === this.chart.end_date) {
      this.chart.start_date = moment(this.chart.start_date).subtract(1, 'M').format('YYYY-MM-DD')
      this.chart.end_date = moment(this.chart.start_date).add(1, 'M').format('YYYY-MM-DD')
    }
    this.updateChart()
  },
  onSelectCampaign (id) {
    console.info('- Store.onSelectCampaign')
    this.toggleLoading()
    this.chart.selected_campaigns.push(this.campaigns.index[id])
    this.updateChart()
  },
  onDeselectCampaign (id) {
    console.info('- Store.onDeselectCampaign')
    this.toggleLoading()
    _.remove(this.chart.selected_campaigns, {id: id})
    this.updateChart()
  },
  onClearSelectedCampaigns () {
    console.info('- Store.onClearSelectedCampaigns')
    this.toggleLoading()
    this.chart.selected_campaigns = []
    this.updateChart()
  },

  // ============================  Chart Properties =========================== //
  onSetType (type) {
    console.info('- Store.onSetType')
    this.toggleLoading()
    this.chart.type = type
    this.updateChart()
  },
  onSetPalette (palette) {
    console.info('- Store.onSetPalette')
    this.chart.palette = palette
    this.chart.colors = palettes[palette]
    this.trigger(this.chart)
  },
  onSetTitle (title) {
    console.info('- Store.onSetTitle')
    this.chart.title = title
    this.trigger(this.chart)
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
    if (_.isEmpty(datapoints.raw)) {
      this.chart.data = []
      return this.trigger(this.chart)
    }
    this.datapoints = datapoints
    this.chart.parent_location_map = _.indexBy(datapoints.meta.parent_location_map, 'name')
    this.chart.default_sort_order = datapoints.meta.default_sort_order
    this.chart = this.formatChartByType()
    this.chart.loading = false
    this.trigger(this.chart)
  },

  // =========================================================================== //
  //                                   UTILITIES                                 //
  // =========================================================================== //
  updateChart () {
  console.info('-- Store.updateChart' + (this.chartParamsAreReady() ? ' (Params Ready!)' : ''))
    if (this.chart.data !== null) {
      DatapointActions.clearDatapoints()
      this.chart.data = null
      this.trigger(this.chart)
    }
    if (this.chartParamsAreReady()) {
      if (this.chart.type === 'ChoroplethMap') {
        DataExplorerActions.fetchMapFeatures(this.chart.selected_locations.map(location => location.id))
      }
      DatapointActions.fetchDatapoints({
        indicator_ids: this.chart.selected_indicators.map(indicator => indicator.id),
        location_ids: this.chart.selected_locations.map(location => location.id),
        start_date: this.chart.start_date,
        end_date: this.chart.end_date,
        type: this.chart.type
      })
    } else {
      this.chart.loading = false
      this.trigger(this.chart)
    }
  },

  formatChartByType () {
    console.info('---- Store.formatChartByType')
    const chart = this.chart
    const datapoints = this.datapoints.raw
    if (chart.type === 'RawData') {
      chart.data = datapoints
      return chart
    }
    const selected_locations_index = _.indexBy(this.chart.selected_locations, 'id')
    const selected_indicators_index = _.indexBy(this.chart.selected_indicators, 'id')
    const groups = chart.groupBy === 'indicator' ? selected_indicators_index : selected_locations_index
    const layout = 1 // hard coded for now
    const melted_datapoints = this.melt(datapoints, this.chart.selected_indicators)

    switch (chart.type) {
      case 'LineChart':
        return DataExplorerStoreHelpers.formatLineChart(melted_datapoints, chart, groups, layout)
      // case 'PieChart':
        // return DataExplorerStoreHelpers.formatPieChart(melted_datapoints, this.chart.selected_indicators, layout)
      case 'ChoroplethMap':
        return DataExplorerStoreHelpers.formatChoroplethMap(melted_datapoints, chart, this.locations.index, this.indicators.index, layout)
      // case 'ColumnChart':
        // return DataExplorerStoreHelpers.formatColumnChart(melted_datapoints, lower, upper, groups, chart.def, layout)
      // case 'ScatterChart':
        // return DataExplorerStoreHelpers.formatScatterChart(datapoints, selected_locations_index, selected_indicators_index, chart.def, layout)
      // case 'BarChart':
        // return DataExplorerStoreHelpers.formatBarChart(datapoints, selected_locations_index, selected_indicators_index, chart.def, layout)
      case 'TableChart':
        return DataExplorerStoreHelpers.formatTableChart(datapoints, chart, this.locations.index, this.indicators.index)
      default:
    }
  },

  chartParamsAreReady () {
    const campaignsReady = !_.isEmpty(this.chart.selected_campaigns)
    const selectedLocationsReady = !_.isEmpty(this.chart.selected_locations)
    const selectedIndicatorsReady = !_.isEmpty(this.chart.selected_indicators)
    const startDateReady = !_.isEmpty(this.chart.start_date)
    const endDateReady = !_.isEmpty(this.chart.end_date)
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

  toggleLoading () {
    this.chart.loading = true
    this.trigger(this.chart)
  }

})

export default DataExplorerStore
