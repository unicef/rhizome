import _ from 'lodash'
import uuid from 'uuid'
import moment from 'moment'
import Reflux from 'reflux'

import builderDefinitions from 'components/d3chart/utils/builderDefinitions'
import ChartActions from 'actions/ChartActions'
import DashboardChartsActions from 'actions/DashboardChartsActions'
import DatapointActions from 'actions/DatapointActions'
import DatapointStore from 'stores/DatapointStore'
import CampaignStore from 'stores/CampaignStore'
import LocationStore from 'stores/LocationStore'
import IndicatorStore from 'stores/IndicatorStore'

import palettes from 'utilities/palettes'

class ChartState {
  constructor () {
    this.uuid = null
    this.type = 'RawData'
    this.type_params = {}
    this.title = ''
    this.data = null
    this.datapoints = null
    this.data_format = 'pct'
    this.groupBy = 'indicator'
    this.groupByTime = 'campaign'
    this.location_depth = 0
    this.palette = 'traffic_light'
    this.locations_index = null
    this.indicators_index = null
    this.indicator_filter = null
    this.selected_campaigns = []
    this.selected_indicators = []
    this.selected_locations = []
    this.end_date = moment().format('YYYY-MM-DD')
    this.start_date = moment().subtract(1, 'y').format('YYYY-MM-DD')
    this.features = []
    this.loading = false
    this.linkedCampaigns = false
    this.selectTypeMode = true
    this.editMode = true
    this.saving = false
    this.indicator_colors = {}
  }
}

var DashboardChartsStore = Reflux.createStore({

  listenables: DashboardChartsActions,

  charts: {},

  init () {
    this.listenTo(DatapointStore, this.onDatapointStore)
    this.listenTo(ChartActions.postChart.completed, this.onPostChartCompleted)
    this.joinTrailing(LocationStore, IndicatorStore, CampaignStore, this.onGetInintialStores)
  },

  getInitialState: function () {
    return this.charts
  },

  // =========================================================================== //
  //                            REGULAR ACTION HANDLERS                          //
  // =========================================================================== //

  // =================================  Layout  ================================ //
  onToggleChartEditMode: function (uuid) {
    const chart = this.charts[uuid]
    chart.editMode = !chart.editMode
    this.trigger(this.charts)
  },

  onExitEditMode: function (uuid) {
    this.charts[uuid].editMode = false
    this.trigger(this.charts)
  },

  onToggleSelectTypeMode: function (uuid) {
    const chart = this.charts[uuid]
    chart.selectTypeMode = !chart.selectTypeMode
    this.trigger(this.charts)
  },

  onExitSelectTypeMode: function (uuid) {
    this.charts[uuid].selectTypeMode = false
    this.trigger(this.charts)
  },

  // =================================  Charts  ================================ //
  onAddChart: function (chart_uuid) {
    const new_chart = new ChartState()
    new_chart.uuid = chart_uuid || uuid.v4()
    this.charts[new_chart.uuid] = new_chart
    DashboardChartsActions.setCampaigns(this.campaigns.raw[0], new_chart.uuid)
    this.trigger(this.charts)
  },
  onSelectChart: function (chart, uuid) {
    this.trigger(this.charts)
    const new_chart = this.meltChart(chart)
    this.charts[new_chart.uuid] = new_chart
    delete this.charts[uuid]
    DashboardChartsActions.setType(new_chart.type, new_chart.uuid)
    this.trigger(this.charts)
    this._hideSelectChartMenu()
  },
  _hideSelectChartMenu: function () {
    let menus = document.getElementsByClassName('menu')
    for (let menu of menus) { menu.parentNode.removeChild(menu) }
  },
  onDuplicateChart: function (chart_uuid) {
    const chart = this.charts[chart_uuid]
    const new_chart = Object.assign(new ChartState(), chart)
    new_chart.uuid = uuid.v4()
    new_chart.selected_indicators = chart.selected_indicators.slice(0)
    new_chart.selected_campaigns = chart.selected_campaigns.slice(0)
    new_chart.selected_locations = chart.selected_locations.slice(0)
    this.charts[new_chart.uuid] = new_chart
    this.trigger(this.charts)
  },
  onRemoveChart: function (uuid) {
    if (confirm('Are you sure you want to remove this chart?')) {
      delete this.charts[uuid]
      this.trigger(this.charts)
    }
  },
  onSaveChart: function (uuid) {
    const chart = this.charts[uuid]
    if (!chart.title) {
      return window.alert('Please add a Title to your chart')
    }
    this.charts[uuid].saving = true
    this.trigger(this.charts)
    ChartActions.postChart({
      id: chart.id,
      title: chart.title,
      uuid: chart.uuid,
      chart_json: JSON.stringify({
        type: chart.type,
        start_date: chart.start_date,
        end_date: chart.end_date,
        campaign_ids: chart.selected_campaigns.map(campaign => campaign.id),
        location_ids: chart.selected_locations.map(location => location.id),
        indicator_ids: chart.selected_indicators.map(indicator => indicator.id),
        indicator_colors: chart.indicator_colors,
        type_params: chart.type_params,
        groupBy: chart.groupBy,
        groupByTime: chart.groupByTime,
        location_depth: chart.location_depth
      })
    })
  },

  // =============================  Indicators  ============================ //
  onSetIndicators: function (indicators, uuid) {
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
  onSelectIndicator: function (id, uuid) {
    this.toggleLoading(uuid)
    this.charts[uuid].selected_indicators.push(this.indicators.index[id])
    this.updateChart(uuid)
  },
  onDeselectIndicator: function (id, uuid) {
    this.toggleLoading(uuid)
    _.remove(this.charts[uuid].selected_indicators, {id: id})
    this.updateChart(uuid)
  },
  onReorderIndicator: function (selected_indicators, uuid) {
    this.toggleLoading(uuid)
    this.charts[uuid].selected_indicators = selected_indicators
    this.updateChart(uuid)
  },
  onClearSelectedIndicators: function (uuid) {
    this.toggleLoading(uuid)
    this.charts[uuid].selected_indicators = []
    this.updateChart(uuid)
  },
  onSetIndicatorFilter: function (filter, uuid) {
    this.toggleLoading(uuid)
    this.charts[uuid].indicator_filter = filter
    if (filter.value === 0) {
      this.charts[uuid].indicator_filter = null
    }
    this.updateChart(uuid)
  },
  onSetIndicatorColor: function (indicator_id, color, uuid) {
    this.toggleLoading(uuid)
    this.charts[uuid].indicator_colors[indicator_id] = color
    this.updateChart(uuid)
  },

  // =============================  Locations  ============================ //
  onSetLocations: function (locations, uuid) {
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
  onSetLocationDepth: function (location_depth, uuid) {
    this.toggleLoading(uuid)
    this.charts[uuid].location_depth = location_depth
    this.updateChart(uuid)
  },
  onSelectLocation: function (id, uuid) {
    this.toggleLoading(uuid)
    if (typeof id === 'string' && id.indexOf('lpd') > -1) {
      return this.addLocationsByLpdStatus(id, uuid)
    }
    this.charts[uuid].selected_locations.push(this.locations.index[id])
    this.updateChart(uuid)
  },
  addLocationsByLpdStatus: function (id, uuid) {
    let locations_to_add = this.locations.lpd_statuses.find(lpd_status => lpd_status.value === id)
    locations_to_add.location_ids.forEach(location_id => {
      if (this.charts[uuid].selected_locations.map(item => item.id).indexOf(location_id) >= 0) {
        return
      }
      this.charts[uuid].selected_locations.push(this.locations.index[location_id])
    })
    this.updateChart(uuid)
  },
  onDeselectLocation: function (id, uuid) {
    this.toggleLoading(uuid)
    _.remove(this.charts[uuid].selected_locations, {id: id})
    this.updateChart(uuid)
  },
  onClearSelectedLocations: function (uuid) {
    this.toggleLoading(uuid)
    this.charts[uuid].selected_locations = []
    this.updateChart(uuid)
  },

  // =============================  Campaigns  ============================ //
  onSetCampaigns: function (campaigns, uuid) {
    this.toggleLoading(uuid)
    if (this.charts[uuid].linkedCampaigns) {
      _.toArray(this.charts).forEach(chart => {
        if (chart.linkedCampaigns) {
          this._assignCampaigns(campaigns, chart.uuid)
        }
        this.updateChart(chart.uuid)
      })
    } else {
      this._assignCampaigns(campaigns, uuid)
      this.updateChart(uuid)
    }
  },
  onSelectCampaign: function (id, uuid) {
    this.toggleLoading(uuid)
    this.charts[uuid].selected_campaigns.push(this.campaigns.index[id])
    this.updateChart(uuid)
  },
  onDeselectCampaign: function (id, uuid) {
    this.toggleLoading(uuid)
    _.remove(this.charts[uuid].selected_campaigns, {id: id})
    this.updateChart(uuid)
  },
  onClearSelectedCampaigns: function (uuid) {
    this.toggleLoading(uuid)
    this.charts[uuid].selected_campaigns = []
    this.updateChart(uuid)
  },
  onToggleCampaignLink: function (uuid) {
    this.toggleLoading(uuid)
    const current_chart = this.charts[uuid]
    if (current_chart.linkedCampaigns) {
      current_chart.linkedCampaigns = false
      return this.trigger(this.charts)
    }
    _.toArray(this.charts).forEach(chart => chart.linkedCampaigns = true)
    _.toArray(this.charts).forEach(chart => DashboardChartsActions.setCampaigns(current_chart.selected_campaigns, chart.uuid))
  },
  _assignCampaigns: function (campaigns, uuid) {
    if (_.isArray(campaigns)) {
      this.charts[uuid].selected_campaigns = campaigns.map(campaign => this.couldBeId(campaign) ? this.campaigns.index[campaign] : campaign)
    } else {
      this.charts[uuid].selected_campaigns = this.couldBeId(campaigns) ? [this.campaigns.index[campaigns]] : [campaigns]
    }
    const chartShowsOneCampaign = _.indexOf(builderDefinitions.single_campaign_charts, this.charts[uuid].type) !== -1
    if (chartShowsOneCampaign) {
      const campaign_start_date = this.charts[uuid].selected_campaigns[0].start_date
      const campaign_end_date = this.charts[uuid].selected_campaigns[0].end_date
      this.charts[uuid].start_date = moment(campaign_start_date).format('YYYY-MM-DD')
      this.charts[uuid].end_date = moment(campaign_end_date).format('YYYY-MM-DD')
      if (campaign_start_date === campaign_end_date) {
        this.charts[uuid].end_date = moment(campaign_end_date).add(1, 'M').format('YYYY-MM-DD')
      }
    }
  },

  // ============================  Chart Properties =========================== //
  onSetDateRange: function (key, value, uuid) {
    this.toggleLoading(uuid)
    const full_key = key + '_date'
    this.charts[uuid][full_key] = value
    this.updateChart(uuid)
  },
  onSetType: function (type, uuid) {
    this.toggleLoading(uuid)
    this.charts[uuid].type = type
    this.charts[uuid].selectTypeMode = false
    const campaign_ids = this.selected_campaigns ? this.selected_campaigns.map(campaign => campaign.id) : this.campaigns.list[0]
    this._assignCampaigns(campaign_ids, uuid)
    this.updateChart(uuid)
  },
  onSetPalette: function (palette, uuid) {
    this.charts[uuid].palette = palette
    this.charts[uuid].colors = palettes[palette]
    this.trigger(this.charts)
  },
  onSetGroupBy: function (grouping, uuid) {
    this.toggleLoading(uuid)
    this.charts[uuid].groupBy = grouping
    const first_indicator = this.charts[uuid].selected_indicators[0]
    const first_location = this.charts[uuid].selected_locations[0]
    this.charts[uuid].selected_indicators = first_indicator ? [first_indicator] : []
    this.charts[uuid].selected_locations = first_location ? [first_location] : []
    this.updateChart(uuid)
  },
  onSetGroupByTime: function (grouping, uuid) {
    this.toggleLoading(uuid)
    this.charts[uuid].groupByTime = grouping
    this.updateChart(uuid)
  },
  onSetChartTitle: function (title, uuid) {
    this.charts[uuid].title = title
    this.trigger(this.charts)
  },
  onUpdateTypeParams: function (key, value, uuid) {
    this.charts[uuid].type_params[key] = value
    this.trigger(this.charts)
  },

  // =========================================================================== //
  //                               API CALL HANDLERS                             //
  // =========================================================================== //
  // =============================  Fetch Chart  =========================== //
  onFetchChart: function (id) {
    this.trigger(this.charts)
  },
  onFetchChartCompleted: function (chart) {
    chart = chart.meta ? chart.objects : chart
    const new_chart = this.meltChart(chart)
    this.charts[chart.uuid] = new_chart
    DashboardChartsActions.setType(new_chart.type, new_chart.uuid)
    this.trigger(this.charts)
  },
  onFetchChartFailed: function (error) {
    this.setState({ error: error })
  },

  // ============================  Fetch Map Features  ========================= //
  onFetchMapFeatures: function (uuid) {
    this.trigger(this.charts)
  },
  onFetchMapFeaturesCompleted: function (response) {
    const location_depth = parseInt(response.meta.get_params.location_depth) || 0
    const location_id = parseInt(response.meta.get_params.location_id)
    const currently_fetching_charts = _.toArray(this.charts).filter(chart => {
      const depth_matches = parseInt(chart.location_depth) === location_depth
      const location_matches = parseInt(chart.selected_locations[0].id) === location_id
      return chart.fetching_map && location_matches && depth_matches
    })
    const uuid = currently_fetching_charts[0].uuid
    this.charts[uuid].features = response.objects
    this.charts[uuid].loading = true
    this.charts[uuid].fetching_map = false
    this.fetchDatapoints(uuid)
  },
  onFetchMapFeaturesFailed: function (error) {
    this.setState({ error: error })
  },

  // =========================================================================== //
  //                            OTHER STORE DEPENDECIES                          //
  // =========================================================================== //
  onGetInintialStores: function (locations, indicators, campaigns) {
    this.indicators = indicators[0]
    this.locations = locations[0]
    this.campaigns = campaigns[0]
  },

  onDatapointStore: function (datapoints) {
    const uuid = datapoints.meta.chart_uuid
    if (_.isEmpty(datapoints.raw)) {
      this.charts[uuid].data = []
      return this.trigger(this.charts)
    }
    const chart_datapoints = Object.assign({}, datapoints)
    this.charts[uuid].datapoints = chart_datapoints
    this.charts[uuid].data = chart_datapoints.raw
    this.charts[uuid].parent_location_map = _.indexBy(chart_datapoints.meta.parent_location_map, 'name')
    this.charts[uuid].default_sort_order = chart_datapoints.meta.default_sort_order
    this.charts[uuid].loading = false
    this.charts[uuid].locations_index = this.locations.index
    this.charts[uuid].indicators_index = this.indicators.index
    this.trigger(this.charts)
  },

  onPostChartCompleted: function (response) {
    const uuid = response.objects.uuid
    this.charts[uuid].saving = false
    this.trigger(this.charts)
  },

  // =========================================================================== //
  //                                   UTILITIES                                 //
  // =========================================================================== //
  updateChart: function (uuid) {
    if (this.charts[uuid].data !== null) {
      DatapointActions.clearDatapoints()
      this.charts[uuid].data = null
      this.trigger(this.charts)
    }
    if (this.chartParamsAreReady(uuid)) {
      const type = this.charts[uuid].type
      if (type === 'ChoroplethMap' || type === 'MapChart' || type === 'BubbleMap') {
        this.charts[uuid].fetching_map = true
        return DashboardChartsActions.fetchMapFeatures(this.charts[uuid].selected_locations.map(location => location.id), this.charts[uuid].location_depth)
      }
      this.fetchDatapoints(uuid)
    } else {
      this.charts[uuid].loading = false
      this.trigger(this.charts)
    }
  },

  fetchDatapoints: function (uuid) {
    const chart = this.charts[uuid]
    const query = {
      indicator_filter: chart.indicator_filter,
      indicator_ids: chart.selected_indicators.map(indicator => indicator.id),
      location_ids: chart.selected_locations.map(location => location.id),
      location_depth: chart.location_depth,
      group_by_time: chart.groupByTime,
      start_date: chart.start_date,
      end_date: chart.end_date,
      type: chart.type,
      uuid: uuid
    }
    DatapointActions.fetchDatapoints(query)
  },

  meltChart: function (chart) {
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
    new_chart.indicator_colors = chart.chart_json.indicator_colors || {}
    new_chart.type_params = chart.chart_json.type_params || {}
    new_chart.groupBy = chart.chart_json.groupBy
    new_chart.groupByTime = chart.chart_json.groupByTime || 'campaign'
    new_chart.location_depth = chart.chart_json.location_depth || 0
    new_chart.selectTypeMode = false
    new_chart.editMode = false
    return new_chart
  },

  chartParamsAreReady: function (uuid) {
    const campaignsReady = !_.isEmpty(this.charts[uuid].selected_campaigns)
    const selectedLocationsReady = !_.isEmpty(this.charts[uuid].selected_locations)
    const selectedIndicatorsReady = !_.isEmpty(this.charts[uuid].selected_indicators)
    const startDateReady = !_.isEmpty(this.charts[uuid].start_date)
    const endDateReady = !_.isEmpty(this.charts[uuid].end_date)
    return selectedLocationsReady && selectedIndicatorsReady && startDateReady && endDateReady && campaignsReady
  },

  toggleLoading: function (uuid) {
    this.charts[uuid].loading = true
    this.trigger(this.charts)
  },

  couldBeId: function (value) {
    return _.isNumber(value) || _.isString(value)
  }
})

export default DashboardChartsStore
