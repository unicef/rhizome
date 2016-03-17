import _ from 'lodash'
import moment from 'moment'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'

import ChartActions from 'actions/ChartActions'
import DatapointActions from 'actions/DatapointActions'
import builderDefinitions from 'components/molecules/charts_d3/utils/builderDefinitions'
import DatapointStore from 'stores/DatapointStore'
import CampaignStore from 'stores/CampaignStore'
import LocationStore from 'stores/LocationStore'
import IndicatorStore from 'stores/IndicatorStore'
import ChartStoreHelpers from 'stores/ChartStoreHelpers'

import palettes from 'components/molecules/charts_d3/utils/palettes'

var ChartStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: ChartActions,

  chart: {
    def: {
      color: palettes['traffic_light'],
      type: 'RawData',
      indicator_ids: [],
      location_ids: [],
      selected_indicators: [],
      selected_locations: [],
      countries: [],
      groupBy: 'indicator',
      timeRange: null,
      end_date: moment().format('YYYY-MM-DD'),
      start_date: moment().subtract(1, 'y').format('YYYY-MM-DD'),
      title: 'New Chart',
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
      z: 0
    },
    data: null,
    loading: false
  },

  init () {
    this.listenTo(DatapointStore, this.onDatapointStore)
    this.listenTo(IndicatorStore, this.onIndicatorStore)
    this.listenTo(CampaignStore, this.onCampaignStore)
    this.listenTo(LocationStore, this.onLocationStore)
  },

  getInitialState () {
    return this.chart
  },

  // =========================================================================== //
  //                               API CALL HANDLERS                             //
  // =========================================================================== //

  // ===============================  Fetch Chart  ============================= //
  onFetchChart () {
    this.setState({ loading: true })
  },
  onFetchChartCompleted (response) {
    this.chart.def = response.chart_json
    this.chart.def.id = response.id
    this.chart.def.title = response.title
    DatapointActions.fetchDatapoints(this.chart.def)
    this.setState(this.chart)
  },
  onFetchChartFailed (error) {
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

  onSetIndicatorIds (indicator_ids) {
    this.chart.def.indicator_ids = indicator_ids
    this.chart.def.selected_indicators = indicator_ids.map(id => this.indicators.index[id])
    this.chart.def.headers = this.chart.def.selected_indicators
    this.chart.def.xDomain = this.chart.def.headers.map(indicator => indicator.short_name)
    this.updateChart()
  },

  onSetLocationIds (location_ids) {
    this.chart.def.location_ids = location_ids
    this.chart.def.selected_locations = location_ids.map(id => this.locations.index[id])
    this.updateChart()
  },

  onSetCampaignIds (campaign_ids) {
    this.chart.def.campaign_ids = campaign_ids
    this.chart.def.selected_campaigns = campaign_ids.map(id => this.campaigns.index[id])
    this.updateChart()
  },

  onSetType (type) {
    if (type === 'ChoroplethMap') {
      this.chart.def.locationLevelValue = _.findIndex(builderDefinitions.locationLevels, {value: 'sublocations'})
    }
    this.chart.def.type = type
    this.updateChart()
  },

  onSetPalette (palette) {
    this.chart.def.palette = palette
    this.trigger(this.chart)
  },

  onSetTitle (title) {
    this.chart.def.title = title
    this.trigger(this.chart)
  },

  // =========================================================================== //
  //                            OTHER STORE DEPENDECIES                          //
  // =========================================================================== //
  onDatapointStore (datapoints) {
    this.datapoints = datapoints
    this.chart.def.parent_location_map = _.indexBy(datapoints.meta.parent_location_map, 'name')
    this.chart.def.default_sort_order = datapoints.meta.default_sort_order
    // this.chart.data = _(datapoints.raw)
    //   .flatten()
    //   .sortBy(_.method('campaign.start_date.getTime'))
    //   .map(this.melt)
    //   .flatten()
    //   .value()
    this.chart.data = this.getChartFormattedData()
    this.trigger(this.chart)
  },

  onIndicatorStore (indicators) {
    this.indicators = indicators
  },

  onLocationStore (locations) {
    this.locations = locations
  },

  onCampaignStore (campaigns) {
    this.campaigns = campaigns
  },

  // =========================================================================== //
  //                                   UTILITIES                                 //
  // =========================================================================== //
  updateChart () {
    if (this.chartParamsAreReady()) {
      DatapointActions.fetchDatapoints({
        indicator_ids: this.chart.def.indicator_ids,
        location_ids: this.chart.def.location_ids,
        start_date: this.chart.def.start_date,
        end_date: this.chart.def.end_date,
        type: this.chart.def.type
      })
    } else {
      this.chart.data = this.getChartFormattedData()
      this.trigger(this.chart)
    }
  },

  getChartFormattedData () {
    const chart_def = this.chart.def
    const datapoints = this.datapoints.raw
    const selected_locations = this.chart.def.location_ids.map(id => this.locations.index[id])
    const selected_indicators = this.chart.def.indicator_ids.map(id => this.indicators.index[id])
    const selected_locations_index = this.locations.index
    const selected_indicators_index = this.indicators.index
    const lower = moment(chart_def.start_date, 'YYYY-MM-DD')
    const upper = moment(chart_def.end_date, 'YYYY-MM-DD')
    const layout = 1 // hard coded for now
    const groups = chart_def.groupBy === 'indicator' ? _.indexBy(selected_indicators, 'id') : _.indexBy(selected_locations, 'id')

    // const selected_indicator_ids = selected_indicators.map(_.property('id'))
    // const meltPromise = this.meltFurther(datapoints, selected_indicator_ids)

    switch (chart_def.type) {
      case 'LineChart':
        return ChartStoreHelpers.getLineChartData(meltPromise, lower, upper, groups, chart_def, layout)
      case 'PieChart':
        return ChartStoreHelpers.getPieChartData(meltPromise, selected_indicators, layout)
      case 'ChoroplethMap':
        return ChartStoreHelpers.getChoroplethMapData(meltPromise, selected_locations_index, selected_indicators, chart_def, layout)
      case 'ColumnChart':
        return ChartStoreHelpers.getColumnChartData(meltPromise, lower, upper, groups, chart_def, layout)
      case 'ScatterChart':
        return ChartStoreHelpers.getScatterChartData(datapoints, selected_locations_index, selected_indicators_index, chart_def, layout)
      case 'BarChart':
        return ChartStoreHelpers.getBarChartData(datapoints, selected_locations_index, selected_indicators_index, chart_def, layout)
      case 'TableChart':
        return ChartStoreHelpers.getTableChartData(datapoints, selected_locations_index, selected_indicators_index, chart_def, layout)
      default:
        console.log('No such chart type: ' + chart_def.type)
    }
  },

  chartParamsAreReady () {
    const selectedLocationsReady = !_.isEmpty(this.chart.def.location_ids)
    const selectedIndicatorsReady = !_.isEmpty(this.chart.def.indicator_ids)
    const startDateReady = !_.isEmpty(this.chart.def.start_date)
    const endDateReady = !_.isEmpty(this.chart.def.end_date)
    return selectedLocationsReady && selectedIndicatorsReady && startDateReady && endDateReady
  },

  melt (datapoint) {
    const base = _.omit(datapoint, 'indicators')
    return datapoint.indicators.map(i => _.assign({indicator: i.indicator, value: i.value}, base))
  }

  // meltFurther (datapoints, indicatorArray) {
  //   const dataset = data.objects
  //   const baseIndicators = indicatorArray.map(indicator => {
  //     return { indicator: indicator + '', value: 0 }
  //   })
  //   const o = _(dataset).map(d => {
  //     const base = _.omit(d, 'indicators')
  //     const indicatorFullList = _.assign(_.cloneDeep(baseIndicators), d.indicators)
  //     return indicatorFullList.map(indicator => {
  //       return _.assign({}, base, indicator)
  //     })
  //   })
  //   .flatten()
  //   .value()

  //   return o
  // }

})

export default ChartStore
