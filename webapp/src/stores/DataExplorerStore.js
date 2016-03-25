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
    data_format: 'pct',
    colors: palettes['traffic_light'],
    type: 'RawData',
    features: [],
    selected_campaigns: [],
    selected_indicators: [],
    selected_locations: [],
    countries: [],
    groupBy: 'indicator',
    timeRange: null,
    end_date: moment().format('YYYY-MM-DD'),
    start_date: moment().subtract(1, 'y').format('YYYY-MM-DD'),
    title: 'Untitled',
    cellSize: 36,
    fontSize: 14,
    margin: { top: 40, right: 40, bottom: 40, left: 40 },
    cellFontSize: 14,
    headers: [],
    parent_location_map: null,
    default_sort_order: null,
    x: 0,
    xFormat: ',.0f',
    y: 0,
    yFormat: ',.0f',
    z: 0,
    data: null,
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
    this.setState({ data: null })
  },
  onFetchChartCompleted (response) {
    const chart_json = typeof response.chart_json === 'string' ? JSON.parse(response.chart_json) : response.chart_json
    this.chart.campaign_ids = chart_json.campaign_ids
    this.chart.start_date = chart_json.start_date
    this.chart.end_date = chart_json.end_date
    this.chart.id = response.id
    this.chart.title = response.title
    this.chart.selected_locations = chart_json.campaign_ids.map(id => this.campaigns.index[id])
    this.chart.selected_locations = chart_json.location_ids.map(id => this.locations.index[id])
    this.chart.selected_indicators = chart_json.indicator_ids.map(id => this.indicators.index[id])
    this.chart.headers = this.chart.selected_indicators
    this.chart.xDomain = this.chart.headers.map(indicator => indicator.short_name)
    this.chart.x = this.chart.selected_indicators[0]
    this.chart.y = this.chart.selected_indicators[1] ? this.chart.selected_indicators[1].id : 0
    this.chart.z = this.chart.selected_indicators[2] ? this.chart.selected_indicators[2].id : 0
    DataExplorerActions.setType(chart_json.type)
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
    this.updateChart()
  },
  onFetchMapFeaturesFailed (error) {
    this.setState({ error: error })
  },

  // =========================================================================== //
  //                            REGULAR ACTION HANDLERS                          //
  // =========================================================================== //
  onSetDateRange (key, value) {
    const full_key = key + '_date'
    this.chart.def[full_key] = value
    this.updateChart()
  },

  // =============================  Set Indicators  ============================ //
  onSetIndicators (indicators) {
    if (_.isArray(indicators)) {
      this.chart.selected_indicators = indicators.map(ind => this.couldBeId(ind) ? this.indicators.index[ind] : ind)
    } else {
      this.chart.selected_indicators = this.couldBeId(indicators) ? [this.indicators.index[indicators]] : [indicators]
    }
    this.chart.headers = this.chart.selected_indicators
    this.chart.xDomain = this.chart.headers.map(indicator => indicator.short_name)
    this.chart.x = this.chart.selected_indicators[0]
    this.chart.y = this.chart.selected_indicators[1] ? this.chart.selected_indicators[1].id : 0
    this.chart.z = this.chart.selected_indicators[2] ? this.chart.selected_indicators[2].id : 0
    this.updateChart()
  },

  // =============================  Set Locations  ============================ //
  onSetLocations (locations) {
    if (_.isArray(locations)) {
      this.chart.selected_locations = locations.map(location => this.couldBeId(location) ? this.locations.index[location] : location)
    } else {
      this.chart.selected_locations = this.couldBeId(locations) ? [this.locations.index[locations]] : [locations]
    }
    if (this.chart.type === 'ChoroplethMap') {
      this.chart.locationLevelValue = _.findIndex(builderDefinitions.locationLevels, {value: 'sublocations'})
      return DataExplorerActions.fetchMapFeatures(this.chart.selected_locations.map(location => location.id))
    }
    this.updateChart()
  },

  // =============================  Set Campaigns  ============================ //
  onSetCampaigns (campaigns) {
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

  // ===============================  Set Type  ============================= //
  onSetType (type) {
    this.chart.type = type
    this.chart.data = null
    if (type === 'ChoroplethMap') {
      this.chart.locationLevelValue = _.findIndex(builderDefinitions.locationLevels, {value: 'sublocations'})
      return DataExplorerActions.fetchMapFeatures(this.chart.selected_locations.map(location => location.id))
    }
    if (type === 'TableChart') {
      this.chart.start_date = this.chart.selected_campaigns[0].start_date
      this.chart.end_date = this.chart.selected_campaigns[0].end_date
      if (this.chart.end_date === this.chart.end_date) {
        this.chart.start_date = moment(this.chart.start_date).subtract(1, 'M').format('YYYY-MM-DD')
        this.chart.end_date = moment(this.chart.start_date).add(1, 'M').format('YYYY-MM-DD')
      }
    }
    this.updateChart()
  },

  onSetPalette (palette) {
    this.chart.palette = palette
    this.trigger(this.chart)
  },

  onSetTitle (title) {
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
    this.datapoints = datapoints
    this.chart.parent_location_map = _.indexBy(datapoints.meta.parent_location_map, 'name')
    this.chart.default_sort_order = datapoints.meta.default_sort_order
    this.chart = this.formatChartByType()
    this.trigger(this.chart)
  },

  // =========================================================================== //
  //                                   UTILITIES                                 //
  // =========================================================================== //
  updateChart () {
    if (this.chartParamsAreReady()) {
      DatapointActions.fetchDatapoints({
        indicator_ids: this.chart.selected_indicators.map(indicator => indicator.id),
        location_ids: this.chart.selected_locations.map(location => location.id),
        start_date: this.chart.start_date,
        end_date: this.chart.end_date,
        type: this.chart.type
      })
    } else {
      this.chart.data = null
      this.trigger(this.chart)
    }
  },

  formatChartByType () {
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
  }

})

export default DataExplorerStore
