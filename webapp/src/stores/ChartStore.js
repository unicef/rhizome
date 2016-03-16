import _ from 'lodash'
import moment from 'moment'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'
import ChartActions from 'actions/ChartActions'
import DatapointActions from 'actions/DatapointActions'
import builderDefinitions from 'components/molecules/charts_d3/utils/builderDefinitions'
import DatapointStore from 'stores/DatapointStore'

var ChartStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: ChartActions,

  chart: {
    def: {
      type: 'RawData',
      indicator_ids: [],
      location_ids: [],
      countries: [],
      groupBy: 'indicator',
      timeRange: null,
      end_date: moment().format('YYYY-MM-DD'),
      start_date: moment().subtract(1, 'y').format('YYYY-MM-DD'),
      title: 'New Chart',
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
    this.updateChart()
  },

  onSetLocationIds (location_ids) {
    this.chart.def.location_ids = location_ids
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
    this.chart.data = _(datapoints.raw)
      .flatten()
      .sortBy(_.method('campaign.start_date.getTime'))
      .map(this.melt)
      .flatten()
      .value()
    this.trigger(this.chart)
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
      this.trigger(this.chart)
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
  },

  applyChartDef (chartDef) {
    // this.data.locationLevelValue = Math.max(_.findIndex(builderDefinitions.locationLevels, { value: chartDef.location_depth }), 0)
    // this.data.groupByValue = Math.max(_.findIndex(builderDefinitions.groups, { value: chartDef.groupBy }), 0)
    // this.data.timeValue = Math.max(_.findIndex(this.data.timeRangeFilteredList, { json: chartDef.timeRange }), 0)
    // this.data.yFormatValue = Math.max(_.findIndex(builderDefinitions.formats, { value: chartDef.yFormat }), 0)
    // this.data.xFormatValue = Math.max(_.findIndex(builderDefinitions.formats, { value: chartDef.xFormat }), 0)

    // this.data.chartDef.location_depth = builderDefinitions.locationLevels[this.data.locationLevelValue].value
    // this.data.chartDef.groupBy = builderDefinitions.groups[this.data.groupByValue].value
    // // this.data.chartDef.timeRange = this.data.timeRangeFilteredList[this.data.timeValue].json
    // this.data.chartDef.yFormat = builderDefinitions.formats[this.data.yFormatValue].value
    // this.data.chartDef.xFormat = builderDefinitions.formats[this.data.xFormatValue].value
  }

})

export default ChartStore
