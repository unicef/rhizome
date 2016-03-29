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
import DashboardNewStoreHelpers from 'stores/DashboardNewStoreHelpers'

import palettes from 'components/molecules/charts/utils/palettes'

var DashboardNewStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: DashboardNewActions,

  chart_template: {
    uuid: uuid.v4(),
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
    fetching: false
  },

  charts: [
    {
      uuid: uuid.v4(),
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
      fetching: false
    }
  ],

  init () {
    this.listenTo(DatapointStore, this.onDatapointStore)
    this.joinTrailing(LocationStore, IndicatorStore, CampaignStore, this.onGetInintialStores)
  },

  getInitialState () {
    return this.charts
  },

  // =========================================================================== //
  //                               API CALL HANDLERS                             //
  // =========================================================================== //
  // ============================  Fetch Map Features  ========================= //
  onFetchMapFeatures (index) {
    this.charts[index].loading = true
    this.trigger(this.charts)
  },
  onFetchMapFeaturesCompleted (response) {
    this.charts[index].loading = true
    this.charts[index].features = response.objects.features
  },
  onFetchMapFeaturesFailed (error) {
    this.setState({ error: error })
  },

  // =========================================================================== //
  //                            REGULAR ACTION HANDLERS                          //
  // =========================================================================== //
  // =================================  Charts  ================================ //
  onAddChart (type) { console.info('- Store.onAddChart')
    const new_chart = _.assign({}, this.chart_template)
    new_chart.type = type
    new_chart.title = format.unCamelCase(type)
    this.charts.push(new_chart)
    this.trigger(this.charts)
  },
  onRemoveChart (uuid) { console.info('- Store.onRemoveChart')
    if (confirm('Are you sure you want to remove this chart?')) {
      _.remove(this.charts, {uuid: uuid})
      this.trigger(this.charts)
    }
  },

  // =============================  Indicators  ============================ //
  onSetIndicators (indicators, index) {
    console.info('- Store.onSetIndicators')
    this.toggleLoading(index)
    if (_.isNull(indicators)) {
      this.charts[index].selected_indicators = []
    } else if (_.isArray(indicators)) {
      this.charts[index].selected_indicators = indicators.map(ind => this.couldBeId(ind) ? this.indicators.index[ind] : ind)
    } else {
      this.charts[index].selected_indicators = this.couldBeId(indicators) ? [this.indicators.index[indicators]] : [indicators]
    }
    this.updateChart(index)
  },
  onSelectIndicator (id, index) {
    console.info('- Store.onSelectIndicator')
    this.toggleLoading(index)
    this.charts[index].selected_indicators.push(this.indicators.index[id])
    this.updateChart(index)
  },
  onDeselectIndicator (id, index) {
    console.info('- Store.onDeselectIndicator')
    this.toggleLoading(index)
    _.remove(this.charts[index].selected_indicators, {id: id})
    this.updateChart(index)
  },
  onReorderIndicator (selected_indicators, index) {
    console.info('- Store.onReorderIndicator')
    this.toggleLoading(index)
    this.charts[index].selected_indicators = selected_indicators
    this.updateChart(index)
  },
  onClearSelectedIndicators (index) {
    console.info('- Store.onClearSelectedIndicators')
    this.toggleLoading(index)
    this.charts[index].selected_indicators = []
    this.updateChart(index)
  },

  // =============================  Locations  ============================ //
  onSetLocations (locations, index) {
    console.info('- Store.onSetLocations')
    this.toggleLoading(index)
    if (_.isNull(locations)) {
      this.charts[index].selected_locations = []
    } else if (_.isArray(locations)) {
      this.charts[index].selected_locations = locations.map(location => this.couldBeId(location) ? this.locations.index[location] : location)
    } else {
      this.charts[index].selected_locations = this.couldBeId(locations) ? [this.locations.index[locations]] : [locations]
    }
    this.updateChart(index)
  },
  onSelectLocation (id, index) {console.info('- Store.onSelectLocation')
    this.toggleLoading(index)
    if (typeof id === 'string' && id.indexOf('lpd') > -1) {
      return this.addLocationsByLpdStatus(id)
    }
    this.charts[index].selected_locations.push(this.locations.index[id])
    this.updateChart(index)
  },
  addLocationsByLpdStatus (index) {
    let locations_to_add = this.locations.lpd_statuses.find(lpd_status => lpd_status.value === index)
    locations_to_add.location_ids.forEach(location_id => {
      if (this.charts[index].selected_locations.map(item => item.id).indexOf(location_id) >= 0) {
        return
      }
      this.charts[index].selected_locations.push(this.locations.index[location_id])
    })
    this.updateChart(index)
  },
  onDeselectLocation (id, index) {console.info('- Store.onDeselectLocation')
    this.toggleLoading(index)
    _.remove(this.charts[index].selected_locations, {id: id})
    this.updateChart(index)
  },
  onClearSelectedLocations (index) {console.info('- Store.onClearSelectedLocations')
    this.toggleLoading(index)
    this.charts[index].selected_locations = []
    this.updateChart(index)
  },

  // =============================  Campaigns  ============================ //
  onSetCampaigns (campaigns, index) {console.info('- Store.onSetCampaigns')
    this.toggleLoading(index)
    if (_.isArray(campaigns)) {
      this.charts[index].selected_campaigns = campaigns.map(campaign => this.couldBeId(campaign) ? this.campaigns.index[campaign] : campaign)
    } else {
      this.charts[index].selected_campaigns = this.couldBeId(campaigns) ? [this.campaigns.index[campaigns]] : [campaigns]
    }
    this.charts[index].start_date = this.charts[index].selected_campaigns[0].start_date
    this.charts[index].end_date = this.charts[index].selected_campaigns[0].end_date
    if (this.charts[index].start_date === this.charts[index].end_date) {
      this.charts[index].start_date = moment(this.charts[index].start_date).subtract(1, 'M').format('YYYY-MM-DD')
      this.charts[index].end_date = moment(this.charts[index].start_date).add(1, 'M').format('YYYY-MM-DD')
    }
    this.updateChart(index)
  },
  onSelectCampaign (id, index) { console.info('- Store.onSelectCampaign')
    this.toggleLoading(index)
    this.charts[index].selected_campaigns.push(this.campaigns.index[id])
    this.updateChart(index)
  },
  onDeselectCampaign (id, index) { console.info('- Store.onDeselectCampaign')
    this.toggleLoading(index)
    _.remove(this.charts[index].selected_campaigns, {id: id})
    this.updateChart(index)
  },
  onClearSelectedCampaigns (index) { console.info('- Store.onClearSelectedCampaigns')
    this.toggleLoading(index)
    this.charts[index].selected_campaigns = []
    this.updateChart(index)
  },

  // ============================  Chart Properties =========================== //
  onSetDateRange (key, value, index) { console.info('- Store.onSetDateRange')
    const full_key = key + '_date'
    this.chart[full_key] = value
    this.updateChart(index)
  },
  onSetType (type, index) { console.info('- Store.onSetType')
    this.toggleLoading(index)
    this.charts[index].type = type
    this.updateChart(index)
  },
  onSetPalette (palette, index) { console.info('- Store.onSetPalette')
    this.charts[index].palette = palette
    this.charts[index].colors = palettes[palette]
    this.trigger(this.charts)
  },
  onSetTitle (title, index) { console.info('- Store.onSetTitle')
    this.charts[index].title = title
    this.trigger(this.charts)
  },
  onSaveChart (index) { console.info('- Store.saveChart')
    if (!this.charts[index].title) {
      return window.alert('Please add a Title to your chart')
    }
    ChartActions.postChart({
      id: this.charts[index].id,
      title: this.charts[index].title,
      chart_json: JSON.stringify({
        type: this.charts[index].type,
        start_date: this.charts[index].start_date,
        end_date: this.charts[index].end_date,
        campaign_ids: this.charts[index].selected_campaigns.map(campaign => campaign.id),
        location_ids: this.charts[index].selected_locations.map(location => location.id),
        indicator_ids: this.charts[index].selected_indicators.map(indicator => indicator.id)
      })
    })
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
    const index = this.charts.filter(chart => chart.fetching)
    console.log('index', index)
    if (_.isEmpty(datapoints.raw)) {
      this.charts[index].data = []
      return this.trigger(this.charts)
    }
    this.datapoints = datapoints
    this.charts[index].parent_location_map = _.indexBy(datapoints.meta.parent_location_map, 'name')
    this.charts[index].default_sort_order = datapoints.meta.default_sort_order
    this.charts[index] = this.formatChartByType(index)
    this.charts[index].loading = false
    this.charts[index].fetching = false
    this.trigger(this.charts)
  },

  // =========================================================================== //
  //                                   UTILITIES                                 //
  // =========================================================================== //
  updateChart (index) {  console.info('-- Store.updateChart' + (this.chartParamsAreReady(index) ? ' (Params Ready!)' : ''))
    if (this.charts[index].data !== null) {
      DatapointActions.clearDatapoints()
      this.charts[index].data = null
      this.trigger(this.charts)
    }
    if (this.chartParamsAreReady(index)) {
      this.charts[index].fetching = true
      if (this.charts[index].type === 'ChoroplethMap') {
        DashboardNewActions.fetchMapFeatures(this.charts[index].selected_locations.map(location => location.id))
      }
      DatapointActions.fetchDatapoints({
        indicator_ids: this.charts[index].selected_indicators.map(indicator => indicator.id),
        location_ids: this.charts[index].selected_locations.map(location => location.id),
        start_date: this.charts[index].start_date,
        end_date: this.charts[index].end_date,
        type: this.charts[index].type
      })
    } else {
      this.charts[index].loading = false
      this.trigger(this.charts)
    }
  },

  formatChartByType (index) {  console.info('---- Store.formatChartByType')
    const chart = this.charts[index]
    const datapoints = this.datapoints.raw
    if (chart.type === 'RawData') {
      chart.data = datapoints
      return chart
    }
    const selected_locations_index = _.indexBy(this.charts[index].selected_locations, 'id')
    const selected_indicators_index = _.indexBy(this.charts[index].selected_indicators, 'id')
    const groups = chart.groupBy === 'indicator' ? selected_indicators_index : selected_locations_index
    const layout = 1 // hard coded for now
    const melted_datapoints = this.melt(datapoints, this.charts[index].selected_indicators)

    switch (chart.type) {
      case 'LineChart':
        return DashboardNewStoreHelpers.formatLineChart(melted_datapoints, chart, groups, layout)
      // case 'PieChart':
        // return DashboardNewStoreHelpers.formatPieChart(melted_datapoints, this.charts[index].selected_indicators, layout)
      case 'ChoroplethMap':
        return DashboardNewStoreHelpers.formatChoroplethMap(melted_datapoints, chart, this.locations.index, this.indicators.index, layout)
      // case 'ColumnChart':
        // return DashboardNewStoreHelpers.formatColumnChart(melted_datapoints, lower, upper, groups, chart, layout)
      // case 'ScatterChart':
        // return DashboardNewStoreHelpers.formatScatterChart(datapoints, selected_locations_index, selected_indicators_index, chart, layout)
      // case 'BarChart':
        // return DashboardNewStoreHelpers.formatBarChart(datapoints, selected_locations_index, selected_indicators_index, chart, layout)
      case 'TableChart':
        return DashboardNewStoreHelpers.formatTableChart(datapoints, chart, this.locations.index, this.indicators.index)
      default:
    }
  },

  chartParamsAreReady (index) {
    const campaignsReady = !_.isEmpty(this.charts[index].selected_campaigns)
    console.log('campaignsReady', campaignsReady)
    const selectedLocationsReady = !_.isEmpty(this.charts[index].selected_locations)
    console.log('selectedLocationsReady', selectedLocationsReady)
    const selectedIndicatorsReady = !_.isEmpty(this.charts[index].selected_indicators)
    console.log('selectedIndicatorsReady', selectedIndicatorsReady)
    const startDateReady = !_.isEmpty(this.charts[index].start_date)
    console.log('startDateReady', startDateReady)
    const endDateReady = !_.isEmpty(this.charts[index].end_date)
    console.log('endDateReady', endDateReady)
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

  toggleLoading (index) {
    this.charts[index].loading = true
    this.trigger(this.charts)
  }

})

export default DashboardNewStore
