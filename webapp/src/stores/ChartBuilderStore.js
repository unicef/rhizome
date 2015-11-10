'use strict'
var Reflux = require('reflux/src')
var ChartBuilderActions = require('actions/ChartBuilderActions')

var _ = require('lodash')
var treeify = require('data/transform/treeify')
var ancestoryString = require('data/transform/ancestryString')
var api = require('data/api')
var d3 = require('d3')
var moment = require('moment')
var colors = require('colors')
var Vue = require('vue') // for tooltip display
var processChartData = require('./chartBuilder/processChartData')

function melt (data, indicatorArray) {
  var dataset = data.objects
  var baseIndicators = _.map(indicatorArray, function (indicator) {
    return { indicator: indicator + '', value: 0 }
  })
  var o = _(dataset)
    .map(function (d) {
      var base = _.omit(d, 'indicators')
      var indicatorFullList = _.assign(_.cloneDeep(baseIndicators), d.indicators)
      return _.map(indicatorFullList, function (indicator) {
        return _.assign({}, base, indicator)
      })
    })
    .flatten()
    .value()
  return o
}
function _groupBySeries (data, groups, groupBy) {
  return _(data)
    .groupBy(groupBy)
    .map(function (d, ind) {
      return seriesObject(
        _.sortBy(d, _.method('campaign.start_date.getTime')),
        ind,
        null,
        groups
      )
    })
    .value()
}

function seriesObject (d, ind, collection, indicators) {
  return {
    name: indicators[ind].name,
    values: d
  }
}
var canDisplayChart = function () {
  if (this.indicatorsSelected.length > 0 && this.campaignSelected.id && this.chartData.length > 0) {
    return true
  } else {
    return false
  }
}
var canDisplayChartReason = function () {
  var reason
  if (this.indicatorsSelected.length === 0) {
    reason = 'Please select at least one indicator'
  } else if (!this.campaignSelected.id) {
    reason = 'Please select a campaign'
  } else if (this.chartData.length === 0) {
    reason = 'No data to display'
  } else {
    reason = ''
  }
  return reason
}

function _columnData (data, groups, groupBy) {
  var columnData = _(data)
    .groupBy(groupBy)
    .map(_.partialRight(seriesObject, groups))
    .value()
  var largestGroup = []
  _.each(columnData, function (series) {
    if (series.values.length > largestGroup.length) {
      largestGroup = series.values
    }
  })
  var baseGroup = _.map(largestGroup, function (group) {
    return {
      campaign: group.campaign,
      value: 0,
      y: 0,
      y0: 0
    }
  })
  _.each(columnData, function (series) {
    var baseGroupValues = _.merge(_.cloneDeep(baseGroup), _.fill(Array(baseGroup.length), { location: series.values[0].location, indicator: series.values[0].indicator }))
    series.values = _.assign(baseGroupValues, _.cloneDeep(series.values))
  })

  var stack = d3.layout.stack()
    .order('default')
    .offset('zero')
    .values(function (d) { return d.values })
    .x(function (d) { return d.campaign.start_date })
    .y(function (d) { return d.value })

  return stack(columnData)
}

function formatTimeRange (val) {
  switch (val) {
    case 'pastYear':
      return {'years': 1}
      break
    case '3Months':
      return {'months': 2}
      break
    case 'current':
      return {'months': 0}
      break
    case 'allTime':
      return null
      break
    default:
      return {'months': 0}
      break
  }
}

var chartOptions = {
  domain: null,
  values: _.property('values'),
  x: _.property('campaign.start_date'),
  y: _.property('value'),
  yFormat: d3.format(',.0f')
}
module.exports = Reflux.createStore({
  data: {
    locationList: [],
    indicatorList: [],
    campaignList: [],
    indicatorsSelected: [],// [{ description: '% missed children due to refusal', short_name: 'Refused', indicator_bounds: [], id: 166, slug: '-missed-children-due-to-refusal', name: '% missed children due to refusal'}],
    campaignSelected: { office_id: 2, start_date: '2014-02-01', id: 137, end_date: '2014-02-01', slug: 'afghanistan-february-2014' },
    locationSelected: { parent_location_id: null, office_id: 1, location_type_id: 1, id: 12907, name: 'Nigeria' },// { id: null, title: null},
    aggregatedlocations: [],
    title: "",
    description: "",
    locationRadios: [{ value: 'selected', title: 'Selected location only' }, { value: 'type', title: 'locations with the same type' }, { value: 'sublocations', title: 'Sublocations 1 level below selected' }],
    locationRadioValue: 2,
    groupByRadios: [{ value: 'indicator', title: 'Indicators' }, { value: 'location', title: 'locations' }],
    groupByRadioValue: 1,
    timeRadios: function () {
      var self = this
      var radios = [{ value: 'allTime', title: 'All Time' }, { value: 'pastYear', title: 'Past Year' }, { value: '3Months', title: 'Past 3 Months' }, { value: 'current', title: 'Current Campaign' }]
      var timeRadios = _.filter(radios, function (radio) { return self.chartTypes[self.selectedChart].timeRadios.indexOf(radio.value) > -1 })
      if (timeRadios.length - 1 < this.timeRadioValue) {
        this.timeRadioValue = 0
      }
      return timeRadios
    },

    formatRadios: function () {
      return [{
        value: ',.0f',
        title: 'Integer'
      }, {
        value: ',.4f',
        title: 'Real Number'
      }, {
        value: '%',
        title: 'Percentage'
      }]
    },
    formatRadioValue: 0,
    xFormatRadioValue: 0,
    timeRadioValue: 2,
    chartTypes: require('./chartBuilder/builderDefinitions'),
    selectedChart: 0,
    chartData: [],
    chartOptions: chartOptions,
    canDisplayChart: canDisplayChart,
    canDisplayChartReason: canDisplayChartReason,
    xAxis: 0,
    yAxis: 0,
    loading: false,
    chartDefinition: function () {
      var formatOpts = this.formatRadios()
      var xFormat = formatOpts[this.xFormatRadioValue].value
      var yFormat = formatOpts[this.formatRadioValue].value

      return {
        title: this.title,
        type: this.chartTypes[this.selectedChart].name,
        indicators: _.map(this.indicatorsSelected, _.property('id')),
        locations: this.locationRadios[this.locationRadioValue].value,
        groupBy: this.groupByRadios[this.groupByRadioValue].value,
        x: this.xAxis,
        y: this.yAxis,
        xFormat: xFormat,
        yFormat: yFormat,
        timeRange: formatTimeRange(this.timeRadios()[this.timeRadioValue].value),
        id: this.id
      }
    }
  },

  listenables: [ChartBuilderActions],

  getInitialState: function () {
    return this.data
  },

  onInitialize: function (chartDef, location, campaign) {
    this.data.locationSelected = location
    this.data.campaignSelected = campaign
    this.resetChartDef()

    var self = this
    var locationPromise = api.locations().then(function (items) {
      self._locationIndex = _.indexBy(items.objects, 'id')
      self.data.locationList = _(items.objects)
      .map(function (location) {
        return {
          'title': location.name,
          'value': location.id,
          'parent': location.parent_location_id
        }
      })
      .sortBy('title')
      .reverse() // I do not know why this works, but it does
      .thru(_.curryRight(treeify)('value'))
      .map(ancestoryString)
      .value()
      self.trigger(self.data)
      self.aggregateLocations()
    })

    api.indicatorsTree().then(function (items) {
      self._indicatorIndex = _.indexBy(items.flat, 'id')
      self.data.indicatorList = _(items.objects)
        .sortBy('title')
        .value()
      if (chartDef) {
        self.applyChartDef(chartDef)
      }
      self.trigger(self.data)
    })

    Promise.all([api.campaign(), api.office()])
      .then(_.spread(function (campaigns, offices) {
        var officeIdx = _.indexBy(offices.objects, 'id')

        self.data.campaignList = _(campaigns.objects)
          .map(function (campaign) {
            return _.assign({}, campaign, {
              'start_date': moment(campaign.start_date, 'YYYY-MM-DD').toDate(),
              'end_date': moment(campaign.end_date, 'YYYY-MM-DD').toDate(),
              'office': officeIdx[campaign.office_id]
            })
          })
          .sortBy(_.method('start_date.getTime'))
          .reverse()
          .value()

        self._campaignIndex = _.indexBy(self.data.campaignList, 'id')

        self.trigger(self.data)
      }))
  },
  onAddIndicatorSelection: function (value) {
    this.data.indicatorsSelected.push(this._indicatorIndex[value])
    this.trigger(this.data)
    this.getChartData()
  },
  onRemoveIndicatorSelection: function (id) {
    _.remove(this.data.indicatorsSelected, { id: id })
    this.trigger(this.data)
    this.getChartData()
  },
  onUpdateTitle: function (value) {
    this.data.title = value
    // this.trigger(this.data)
  },
  onUpdateDescription: function (value) {
    this.data.description = value
    this.trigger(this.data)
  },
  onSelectShowLocationRadio: function (value) {
    this.data.locationRadioValue = value
    this.trigger(this.data)
    this.aggregateLocations()
  },
  onSelectGroupByRadio: function (value) {
    this.data.groupByRadioValue = value
    this.trigger(this.data)
    this.getChartData()
  },
  onSelectTimeRadio: function (value) {
    this.data.timeRadioValue = value
    this.trigger(this.data)
    this.getChartData()
  },
  onSelectFormatRadio: function (value) {
    this.data.formatRadioValue = value
    this.data.chartOptions.yFormat = d3.format(this.data.formatRadios()[value].value)
    this.trigger(this.data)
    this.getChartData()
  },
  onSelectXFormatRadio: function (value) {
    this.data.xFormatRadioValue = value
    this.data.chartOptions.xFormat = d3.format(this.data.formatRadios()[value].value)
    this.trigger(this.data)
    this.getChartData()
  },
  onSelectChart: function (value) {
    this.data.selectedChart = value
    this.data.chartData = []
    // this.data.chartOptions = chartOptions
    this.trigger(this.data)
    this.getChartData()
  },
  onAddCampaignSelection: function (value) {
    this.data.campaignSelected = this._campaignIndex[value]
    this.trigger(this.data)
    this.getChartData()
  },
  onAddLocationSelection: function (value) {
    this.data.locationSelected = this._locationIndex[value]
    this.trigger(this.data)
    this.aggregateLocations()
  },
  onSelectXAxis: function (value) {
    this.data.xAxis = value
    this.getChartData()
  },
  onSelectYAxis: function (value) {
    this.data.yAxis = value
    this.getChartData()
  },
  applyChartDef: function (chartDef) {
    var self = this
    this.data.xAxis = chartDef.x
    this.data.yAxis = chartDef.y
    this.data.id = chartDef.id

    this.data.selectedChart = _.findIndex(this.data.chartTypes, { name: chartDef.type })
    this.data.indicatorsSelected = _.map(chartDef.indicators, function (id) {
      return self._indicatorIndex[id]
    })
    this.data.title = chartDef.title
    this.data.locationRadioValue = _.findIndex(this.data.locationRadios, { value: chartDef.locations })
    this.data.groupByRadioValue = _.findIndex(this.data.groupByRadios, { value: chartDef.groupBy })
    this.data.formatRadioValue = _.findIndex(this.data.formatRadios(), { value: _.get(chartDef, 'yFormat', ',.0f') })
    this.data.xFormatRadioValue = _.findIndex(this.data.formatRadios(), { value: _.get(chartDef, 'xFormat', ',.0f') })

    var timeString = JSON.stringify(chartDef.timeRange)
    var timeValue

    if (timeString === '{\'months\':2}') {
      timeValue = '3Months'
    } else if (timeString === '{\'years\':1}') {
      timeValue = 'pastYear'
    } else if (timeString === '{\'months\':0}') {
      timeValue = 'current'
    } else {
      timeValue = 'allTime'
    }

    // Ensure non-negative value for timeRadioValue because findIndex might
    // return -1 if it can't find the timeValue in the array of options
    this.data.timeRadioValue = Math.max(_.findIndex(this.data.timeRadios(), { value: timeValue }), 0)
    this.trigger(this.data)
  },
  resetChartDef: function () {
    this.data.selectedChart = 0
    this.data.indicatorsSelected = []
    this.data.title = ''
    this.data.locationRadioValue = 0
    this.data.groupByRadioValue = 0
    this.data.timeRadioValue = 0
    this.trigger(this.data)
  },
  aggregateLocations: function () {
    var locations
    var locationSelected = this.data.locationSelected
    var locationRadioValue = this.data.locationRadios[this.data.locationRadioValue].value
    if (locationRadioValue === 'selected') {
      locations = [locationSelected]
    } else if (locationRadioValue === 'type') {
      if (locationSelected.parent_location_id && locationSelected.parent_location_id !== 'None') {
        locations = _.filter(this.locationIndex, { location_type_id: locationSelected.location_type_id, office_id: locationSelected.office_id })
      } else {
        locations = _.filter(this._locationIndex, { location_type_id: this.data.locationSelected.location_type_id })
      }
    } else if (locationRadioValue === 'sublocations') {
      locations = _.filter(this._locationIndex, { parent_location_id: locationSelected.id })
    }
    this.data.aggregatedLocations = locations
    if (this.canFetchChartData()) {
      this.getChartData()
    }
  },
  canFetchChartData: function () {
    if (this.data.indicatorsSelected.length > 0 && this.data.campaignSelected.id) {
      return true
    } else {
      return false
    }
  },
  // Since upper is always the end of the month for the given campaign, it doesn't need it's on compute function, but the lower bound changes based on the time radios the are selected
  getLower:  function (start) {
    var range = this.data.timeRadios()[this.data.timeRadioValue].value
    if (range === 'current') {
      return start.clone().startOf('month')
    } else if (range === '3Months') {
      return start.clone().startOf('month').subtract(3, 'month')
    } else if (range === 'pastYear') {
      return start.clone().startOf('month').subtract(1, 'year')
    } else if (range === 'allTime') {
      return null
    }
  },
  getChartData: function () {
    if (!this.data.indicatorsSelected.length) {
      return
    }
    this.data.loading = true
    this.trigger(this.data) // send the loading parameter to the view
    var selectedChart = this.data.chartTypes[this.data.selectedChart].name
    var groupBy = this.data.groupByRadios[this.data.groupByRadioValue].value
    var self = this
    var indicatorsIndex = _.indexBy(this.data.indicatorsSelected, 'id')//
    var locationsIndex = _.indexBy(this.data.aggregatedLocations, 'id')
    var groups = (groupBy === 'indicator' ? indicatorsIndex : locationsIndex)
    var start = moment(this.data.campaignSelected.start_date)
    var lower = this.getLower(start)// .subtract(1, 'year')
    var upper = start.clone().startOf('month')
    var indicatorArray = _.map(this.data.indicatorsSelected, _.property('id'))
    var q = {
      indicator__in: indicatorArray,
      location__in: _.map(this.data.aggregatedLocations, _.property('id')),
      campaign_start: (lower ? lower.format('YYYY-MM-DD') : null),
      campaign_end: upper.format('YYYY-MM-DD')
    }

    processChartData
    .init(api.datapoints(q), selectedChart, this.data.indicatorsSelected, this.data.aggregatedLocations, lower, upper, groups, groupBy, this.data.xAxis, this.data.yAxis)
    .then(function (chart) {
      self.data.loading = false
      self.data.chartOptions = chart.options
      self.data.chartData = chart.data
      self.trigger(self.data)
    })
  }
})
