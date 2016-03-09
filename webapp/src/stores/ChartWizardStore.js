import Reflux from 'reflux'
import _ from 'lodash'
import moment from 'moment'

import ChartWizardActions from 'actions/ChartWizardActions'

import api from 'data/api'
import ChartDataInit from 'data/chartDataInit'
import builderDefinitions from 'stores/chartBuilder/builderDefinitions'
import treeify from 'data/transform/treeify'
import ancestryString from 'data/transform/ancestryString'

let ChartWizardStore = Reflux.createStore({
  listenables: ChartWizardActions,
  data: {
    chart: {
      options: null,
      data: [],
      def: {},
      yFormatValue: 0,
      xFormatValue: 0
    },
    locations: {
      raw: null,
      index: null,
      filtered: [],
      list: [],
      selected: []
    },
    indicators: {
      raw: null,
      index: null,
      filtered: [],
      list: [],
      order: [],
      selected: []
    },
    campaigns: {
      raw: null,
      index: null,
      filtered: [],
      list: [],
      selected: []
    },
    offices: {
      raw: null,
      index: null,
      filtered: [],
      list: [],
      selected: []
    },
    countries: {
      raw: null,
      index: null,
      list: [],
      selected: []
    },
    location_lpd_statuses: [
      {value: 'lpd-1', 'title': 'LPD 1', location_ids: []},
      {value: 'lpd-2', 'title': 'LPD 2', location_ids: []},
      {value: 'lpd-3', 'title': 'LPD 3', location_ids: []}
    ],
    title: '',
    groupByValue: 0,
    locationLevelValue: 0,
    timeValue: 0,
    canDisplayChart: false,
    isLoading: true,
    rawData: null,
    rawTags: null,
    startDate: null,
    endDate: null
  },
  LAYOUT_PREVIEW: 0,

  filterIndicatorByCountry (indicators, countries) {
    let countryId = countries.map(c => c.id)
    if (countryId.length) {
      return indicators.filter(indicator => {
        let officeId = indicator.office_id.filter(id => !!id)
        return countryId.map(id => officeId.indexOf(id) >= 0).reduce((a, b) => a && b, true)
      })
    } else {
      return []
    }
  },

  filterCampaignByCountry (campaigns, countries) {
    let countryId = countries.map(c => c.id)
    return campaigns.filter(campaign => countryId.indexOf(campaign.office_id) >= 0)
  },

  applyChartDef (chartDef) {
    this.data.locationLevelValue = Math.max(_.findIndex(builderDefinitions.locationLevels, { value: chartDef.location_depth }), 0)
    this.data.groupByValue = Math.max(_.findIndex(builderDefinitions.groups, { value: chartDef.groupBy }), 0)
    this.data.timeValue = Math.max(_.findIndex(this.data.timeRangeFilteredList, { json: chartDef.timeRange }), 0)
    this.data.chart.yFormatValue = Math.max(_.findIndex(builderDefinitions.formats, { value: chartDef.yFormat }), 0)
    this.data.chart.xFormatValue = Math.max(_.findIndex(builderDefinitions.formats, { value: chartDef.xFormat }), 0)
    this.data.chart.def.location_depth = builderDefinitions.locationLevels[this.data.locationLevelValue].value
    this.data.chart.def.groupBy = builderDefinitions.groups[this.data.groupByValue].value
    this.data.chart.def.yFormat = builderDefinitions.formats[this.data.chart.yFormatValue].value
    this.data.chart.def.xFormat = builderDefinitions.formats[this.data.chart.xFormatValue].value
  },

  getInitialState () {
    return this.data
  },

  //===========================================================================//
  //                              INITIALIZATION                               //
  //===========================================================================//
  async onInitialize: function (chart) {
    this.data.chart.def = chart.chart_json ? _.clone(chart.chart_json) : chart
    this.data.title = chart.title

    this.initializeLocations()
    this.initializeIndicators()

    api.office().then(response => {
      this.data.offices.index = _.indexBy(response.objects, 'id')
      this.initializeCountries(this.data.offices.index)
      this.initializeCampaigns(this.data.offices.index)
    })
    this.data.lists.chartTypeFilteredList = builderDefinitions.charts
    this.applyChartDef(this.data.chart.def)

    this.previewChart()
  },

  onClear () {
    this.data = {
      title: '',
      indicatorList: [],
      selected_indicators: [],
      indicatorFilteredList: [],
      countries: [],
      countrySelected: [],
      location: [],
      locationList: [],
      locationFilteredList: [],
      campaignFilteredList: [],
      chartTypeFilteredList: [],
      groupByValue: 0,
      locationLevelValue: 0,
      timeValue: 0,
      yFormatValue: 0,
      xFormatValue: 0,
      canDisplayChart: false,
      isLoading: true,
      chartDef: {},
      rawData: null,
      rawIndicators: null,
      rawTags: null
    }
  },

  //===========================================================================//
  //                                 LOCATIONS                                 //
  //===========================================================================//
  async initializeLocations () {
    const locations = {}
    locations.raw = await api.locations()
    locations.index = _.indexBy(locations.raw.objects, 'id')
    locations.list = _(locations.raw.objects).map(location => {
        return {
          'title': location.name,
          'value': location.id,
          'parent': location.parent_location_id
        }
      })
      .sortBy('title')
      .reverse()
      .thru(_.curryRight(treeify)('value'))
      .map(ancestryString)
      .value()
    locations.filtered = locations.list

    const selected_location_ids = this.data.chart.def.location_ids
    if (selected_location_ids) {
      if (Array.isArray(selected_location_ids)) {
        locations.selected  = selected_location_ids.map(id => locations.index[id])
      } else {
        locations.selected = [locations.index[selected_location_ids]]
      }
    } else {
      this.data.locations.selected = []
    }
    this.data.lpds = this.getLocationLpdStatuses(_.toArray(this.data.locations.index))
    this.data.locations = locations
    this.trigger(this.data)
  },

  getLocationLpdStatuses: function (locationIndex) {
    locationIndex.forEach(location => {
      if (location.lpd_status === 1) {
        this.data.location_lpd_statuses[0].location_ids.push(location.id)
      } else if (location.lpd_status === 2) {
        this.data.location_lpd_statuses[1].location_ids.push(location.id)
      } else if (location.lpd_status === 3) {
        this.data.location_lpd_statuses[2].location_ids.push(location.id)
      }
    })
  },

  addLocationsByLpdStatus: function (index) {
    let locations_to_add = this.data.location_lpd_statuses.find( lpd_status => lpd_status.value === index)
    _.forEach(locations_to_add.location_ids, location_id => {
      if (this.data.locations.selected.map(item => item.id).indexOf(location_id) >= 0) return
      this.data.locations.selected.push(this.data.locations.index[location_id])
    })
    this.previewChart()
  },

  filterLocationByCountry: function (locations, countries) {
    let countryId = countries.map(c => c.id)
    return locations.filter(location => countryId.indexOf(location.value) >= 0 || countryId.indexOf(location.office_id) >= 0)
  },

  onAddLocation: function (index) {
    if (this.data.locations.selected.map(item => item.id).indexOf(index) >= 0) return
    if (typeof index === 'string' && index.indexOf('lpd') > -1) {
      this.addLocationsByLpdStatus(index)
    } else {
      this.data.locations.selected.push(this.data.locations.index[index])
    }
    this.previewChart()
  },

  onRemoveLocation: function (index) {
    _.remove(this.data.locations.selected, { id: index })
    this.previewChart()
  },

  onClearSelectedLocations: function () {
    this.data.locations.selected = []
    this.previewChart()
  },

  onChangeLocationLevelRadio: function (value) {
    this.data.locationLevelValue = value
    this.previewChart()
  },

  //===========================================================================//
  //                                 INDICATORS                                //
  //===========================================================================//
  async initializeIndicators () {
    let indicators = {}
    let indicators_response = await api.indicators(null, null, { 'cache-control': 'no-cache' })
    indicators.raw = indicators_response.objects
    let indicator_tags_response = await api.get_indicator_tag(null, null, { 'cache-control': 'no-cache' })
    let indicatorTree = api.buildIndicatorsTree(indicators.raw, indicator_tags_response.objects, true, true)

    indicators.filtered = indicators.raw
    indicators.index = _.indexBy(indicators.raw, 'id')
    indicators.list = _.sortBy(indicatorTree, 'title')
    indicators.selected = this.data.chart.def.indicator_ids.map(id => indicators.index[id])
    this.data.indicators = indicators
    this.trigger(this.data)
  },

  onAddFirstIndicator: function (index) {
    this.data.indicators.selected[0] = this.data.indicators.index[index]
    this.previewChart()
  },

  onAddIndicator: function (index) {
    if (this.data.indicators.selected.map(indicator => indicator.id).indexOf(index) >= 0) return
    this.data.indicators.selected.push(this.data.indicators.index[index])
    this.data.chart.def.y = index
    this.previewChart()
  },

  onReorderIndicator: function (reorderedIndicators) {
    this.data.indicators.selected = reorderedIndicators
    this.previewChart()
  },

  onRemoveIndicator: function (id) {
    _.remove(this.data.indicators.selected, {id: id})
    this.previewChart()
  },

  onClearSelectedIndicators: function () {
    this.data.indicators.selected = []
    this.previewChart()
  },

  //===========================================================================//
  //                                 COUNTRIES                                 //
  //===========================================================================//
  async initializeCountries (offices_index) {
    let countries = {list: []}
    this.data.country = offices_index[0]
    countries.list.forEach((country, index) => {
      country.value = country.title = country.name
      country.index = index
    })
    countries.index = _.indexBy(countries.list, _.property('id'))
    countries.selected = (this.data.chart.def.countries || []).map(country => countries.index[country])
    this.data.countries = countries
    this.trigger(this.data)
  },

  onChangeCountry: function (index) {
    _.includes(this.data.countries.selected, this.data.countries.list[index])
      ? _.remove(this.data.countries.selected, this.data.countries.list[index])
      : this.data.countries.selected.push(this.data.countries.list[index])

    this.data.indicators.filtered = this.filterIndicatorByCountry(this.indicators, this.data.countries.selected)
    let indicatorTree = api.buildIndicatorsTree(this.data.indicators.filtered, this.data.rawTags.objects, true, true)

    this.data.indicators.list = _.sortBy(indicatorTree, 'title')
    this.data.indicators.selected = this.filterIndicatorByCountry(this.data.indicators.selected, this.data.countries.selected)
    this.data.locations.filtered = this.filterLocationByCountry(this.data.locations.list, this.data.countries.selected)
    this.data.locations.selected = this.filterLocationByCountry(this.data.locations.selected, this.data.countries.selected)
    this.data.campaigns.filtered = this.filterCampaignByCountry(this.data.campaigns.list, this.data.countries.selected)
    this.previewChart()
  },

  //===========================================================================//
  //                                 CAMPAIGNS                                 //
  //===========================================================================//
  async initializeCampaigns (offices_index) {
    let campaigns = {}
    let campaigns_response = await api.campaign()
    campaigns.raw = campaigns_response.objects
    campaigns.index = _.indexBy(this.data.campaigns.list, 'id')
    campaigns.list = _(campaigns.raw)
      .map(campaign => {
        return _.assign({}, campaign, {
          'start_date': moment(campaign.start_date, 'YYYY-MM-DD').toDate(),
          'end_date': moment(campaign.end_date, 'YYYY-MM-DD').toDate(),
          'office': offices_index[campaign.office_id]
        })
      })
      .sortBy(_.method('start_date.getTime'))
      .reverse()
      .value()
    campaigns.filtered = campaigns.list

    if (this.data.chart.def.campaignValue && campaigns.index[this.data.chart.def.campaignValue]) {
      campaigns.selected = campaigns.index[this.data.chart.def.campaignValue]
    } else {
      campaigns.selected = campaigns.filtered.length > 0 ? campaigns.filtered[0] : null
    }

    if (!this.data.chart.def.endDate){
      this.data.chart.def.endDate = moment().format('YYYY-MM-DD')
    }

    if (!this.data.chart.def.startDate){
      this.data.chart.def.startDate = moment().subtract(1, 'y').format('YYYY-MM-DD')
    }
    this.data.campaigns = campaigns
    this.trigger(this.data)
  },

  onAddCampaign: function (index) {
    this.data.campaigns.selected = this.data.campaigns.index[index]
    this.previewChart()
  },

  //===========================================================================//
  //                                  CHART                                    //
  //===========================================================================//
  onUpdateDateRangePicker: function (key, value) {
    var fullKey = key + 'Date'
    this.data[fullKey] = value
    this.data.chart.def[fullKey] = value
    this.previewChart()
  },

  onEditTitle: function (value) {
    this.data.title = value
  },

  onChangeChart: function (value) {
    if (value === 'ChoroplethMap') {
      this.data.locationLevelValue = _.findIndex(builderDefinitions.locationLevels, {value: 'sublocations'})
    }
    this.data.chart.def.type = value
    this.data.chart.def.x = this.data.indicators.selected[0].id
    this.data.chart.def.y = this.data.indicators.selected[1] ? this.data.indicators.selected[1].id : 0
    this.data.chart.def.z = this.data.indicators.selected[2] ? this.data.indicators.selected[2].id : 0
    this.data.chart.data = []

    this.previewChart()
  },

  onChangeGroupRadio: function (value) {
    this.data.groupByValue = value
    this.data.chart.def.groupBy = builderDefinitions.groups[value].value
    this.previewChart()
  },

  onChangeYFormatRadio: function (value) {
    this.data.chart.yFormatValue = value
    this.data.chart.def.yFormat = builderDefinitions.formats[value].value
    this.previewChart()
  },

  onChangeXFormatRadio: function (value) {
    this.data.chart.xFormatValue = value
    this.data.chart.def.xFormat = builderDefinitions.formats[value].value
    this.previewChart()
  },

  onChangeYAxis: function (value) {
    this.data.indicators.selected[1] = this.data.indicators.index[value]
    this.data.chart.def.y = value
    this.previewChart()
  },

  onChangeZAxis: function (value) {
    this.data.indicators.selected[2] = this.data.indicators.index[value]
    this.data.chart.def.z = value
    this.previewChart()
  },

  onChangePalette: function (key) {
    this.data.chart.def.palette = key
    this.previewChart()
  },

  onSetXYAxisLabel: function (xAxisLabel, yAxisLabel) {
    this.data.chart.def.xLabel = xAxisLabel
    this.data.chart.def.yLabel = yAxisLabel
    this.previewChart()
  },

  onSaveChart: function (callback) {
    if (!this.data.title){
      window.alert('Please add a Title to your chart')
      return
    }

    callback(
      _.merge(
        this.data.chart.def,
        {
          indicators_ids: this.data.indicators.selected.map(item => {
            return item.id
          }),
          groupBy: builderDefinitions.groups[this.data.groupByValue].value,
          locations: builderDefinitions.locationLevels[this.data.locationLevelValue].value,
          countries: this.data.countries.selected.map(country => country.id),
          location_ids: this.data.locations.selected.map(location => location.id),
          yFormat: builderDefinitions.formats[this.data.chart.yFormatValue].value,
          xFormat: builderDefinitions.formats[this.data.chart.xFormatValue].value
        }, (source, override) => {
          return override
        }
      )
    )
  },

  _fetchRawData: function (options) {
    api.datapoints(options, null, {'cache-control': 'no-cache'})
      .then(response => {
        if (!response.objects || response.objects.length < 1) {
          this.data.rawData = null
        } else {
          this.data.rawData = response
        }
        this.trigger(this.data)
      })
  },

  _prepRawDataQuery: function (campaign, locations, indicators) {
    this.data.rawData = null
    this.trigger(this.data)

    let options = {indicator__in: []}
    if (locations.length > 0) options.location_id__in = _.map(locations, 'id')
    if (this.data.chart.def.startDate) options.campaign_start = moment(this.data.chart.def.startDate).format('YYYY-M-D')
    if (this.data.chart.def.endDate) options.campaign_end = moment(this.data.chart.def.endDate).format('YYYY-M-D')

    indicators.forEach(indicator => {
      options.indicator__in.push(indicator.id)
    })

    return options
  },

  async previewChart  () {
    // We use the short_name for ordering becuase that is what defines the xDomain in table.js
    this.data.indicators.order = this.data.indicators.selected.map(indicator => indicator.short_name)

    if (!(this.data.indicators.selected.length && this.data.campaigns.selected && this.data.locations.selected.length)) {
      this.data.canDisplayChart = false
      this.data.isLoading = false
      this.trigger(this.data)
      return
    }

    if (this.data.chart.def.type === 'RawData') {
      let options = this._prepRawDataQuery(this.data.campaign, this.data.locations.selected, this.data.indicators.selected)
      this._fetchRawData(options)
      return
    }

    this.data.isLoading = true
    this.trigger(this.data)

    this.data.chart.def.location_ids = this.data.locations.selected.map(location => location.id)
    this.data.chart.def.indicator_ids = this.data.indicators.selected.map(indicator => indicator.id)
    let responses = await ChartDataInit.getPromises()
    ChartDataInit.fetchChart(this.data.chart.def, this.LAYOUT_PREVIEW, responses).then(chart => {
      console.log('chart after fetching', chart)
      this.data.canDisplayChart = true
      this.data.isLoading = false
      this.data.chart.options = chart.options
      this.data.chart.data = chart.data
      this.trigger(this.data)
    })
  }
})

export default ChartWizardStore
