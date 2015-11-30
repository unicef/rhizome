import _ from 'lodash'
import d3 from 'd3'
import moment from 'moment'
import api from 'data/api'
import path from 'vue/src/parsers/path'
import util from 'util/data'

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

function seriesObject (d, ind, collection, groups) {
  return {
    name: groups[ind].name,
    values: d
  }
}

function value (datapoint) {
  if (datapoint && datapoint.hasOwnProperty('value')) {
    return datapoint.value
  }
  return null
}

var tooltipDiv = document.createElement('div') // Vue needs a el to bind to to hold tooltips outside the svg, seems like the least messy solution
document.body.appendChild(tooltipDiv)

function _columnData (data, groups, groupBy) {
  var columnData = _(data)
    .groupBy(groupBy)
    .map(_.partialRight(seriesObject, groups))
    .value()
  var baseCampaigns = []
  _.each(columnData, function (series) {
    _.each(series.values, function (value) { // build the base campaign array that includes all campaigns present in any datapoint, used to fill in missing values so the stacked chart doesn't have gaps
      if (!_.find(baseCampaigns, function (campaign) { return campaign.id === value.campaign.id })) {
        baseCampaigns.push(value.campaign)
      }
    })
    _.each(series.values, function (val) { // replace all null values with 0, caused d3 rect rendering errors in the chart
      if (_.isNull(val.value)) {
        val.value = 0
      }
    })
  })
  baseCampaigns = _.sortBy(baseCampaigns, _.method('campaign.start_date.getTime'))
  _.each(columnData, function (series) {
    _.each(baseCampaigns, function (baseCampaign, index) {
      if (!_.find(series.values, function (value) { return value.campaign.id === baseCampaign.id })) {
        series.values.splice(index, 0, { campaign: baseCampaign, location: series.values[0].location, indicator: series.values[0].indicator, value: 0 })
      }
    })
    series.values = _.sortBy(series.values, _.method('campaign.start_date.getTime'))
  })
  var stack = d3.layout.stack()
    .order('default')
    .offset('zero')
    .values(function (d) { return d.values })
    .x(function (d) { return d.campaign.start_date })
    .y(function (d) { return d.value })

  return stack(columnData)
}
function _barData (datapoints, indicators, properties, series) {
  return _(datapoints)
    .pick(indicators)
    .values()
    .flatten()
    .map(_mapProperties(properties))
    .thru(_filterMissing)
    .thru(_makeSeries(series))
    .value()
}
function _mapProperties (mapping) {
  return function (d) {
    var datum = _.clone(d)

    _.forEach(mapping, function (to, from) {
      path.set(datum, to, path.get(datum, from))
    })

    return datum
  }
}
function _filterMissing (data) {
  return _(data)
    .groupBy('y')
    .filter(function (v) {
      return _(v).pluck('x').some(_.partial(util.defined, _, _.identity))
    })
    .values()
    .flatten()
    .forEach(function (d) {
      if (!util.defined(d.x)) {
        d.x = 0
      }
    })
    .value()
}
function _makeSeries (getSeries) {
  return function (data) {
    return _(data)
      .groupBy(getSeries)
      .map(function (v, k) {
        return {
          name: k,
          values: v
        }
      })
      .value()
  }
}
function _getIndicator (d) {
  return d.indicator.short_name
}

const aspects = {
  0: {
    lineChart: 2.664831804,
    pieChart: 1,
    choroplethMap: 1,
    columnChart: 2.664831804,
    scatterChart: 2.664831804,
    barChart: 2.664831804
  },
  1: {
    lineChart: 2.664831804,
    pieChart: 1,
    choroplethMap: 1,
    columnChart: 2.664831804,
    scatterChart: 2.664831804,
    barChart: 2.664831804
  },
  2: {
    lineChart: 1,
    pieChart: 1,
    choroplethMap: 1,
    columnChart: 1,
    scatterChart: 1,
    barChart: 1.5
  },
  3: {
    lineChart: 1,
    pieChart: 1,
    choroplethMap: 1,
    columnChart: 1,
    scatterChart: 1,
    barChart: 1
  }
}

export default {
  init: function (dataPromise, chartType, indicators, locations, lower, upper, groups, groupBy, xAxis, yAxis, zAxis, layout) {
    let indicatorArray = _.map(indicators, _.property('id'))
    let meltPromise = dataPromise.then(data => { return melt(data, indicatorArray) })
    let chartProcessors = {
      LineChart: {
        fn: this.processLineChart,
        para: [meltPromise, lower, upper, groups, groupBy, layout]
      },
      PieChart: {
        fn: this.processPieChart,
        para: [meltPromise, indicators, layout]
      },
      ChoroplethMap: {
        fn: this.processChoroplethMap,
        para: [meltPromise, locations, indicators, xAxis, yAxis, zAxis, layout]
      },
      ColumnChart: {
        fn: this.processColumnChart,
        para: [meltPromise, lower, upper, groups, groupBy, layout]
      },
      ScatterChart: {
        fn: this.processScatterChart,
        para: [dataPromise, locations, indicators, xAxis, yAxis, layout]
      },
      BarChart: {
        fn: this.processBarChart,
        para: [dataPromise, locations, indicators, layout]
      }
    }
    return chartProcessors[chartType].fn(...chartProcessors[chartType].para)
  },
  processLineChart: function (dataPromise, lower, upper, groups, groupBy, layout) {
    return dataPromise.then(function (data) {
      if (!data || data.length === 0) {
        return { options: null, data: null }
      }
      if (!lower) { // set the lower bound from the lowest datapoint value
        var sortedDates = _.sortBy(data, _.method('campaign.start_date.getTime'))
        lower = moment(_.first(sortedDates).campaign.start_date)
      }
      var chartOptions = {
        domain: _.constant([lower.toDate(), upper.toDate()]),
        aspect: aspects[layout].lineChart,
        values: _.property('values'),
        x: _.property('campaign.start_date'),
        xFormat: (d) => { return moment(d).format('MMM YYYY') },
        y: _.property('value')
      }
      var chartData = _groupBySeries(data, groups, groupBy)
      return { options: chartOptions, data: chartData }
    })
  },
  processPieChart: function (dataPromise, indicators, layout) {
    var idx = _.indexBy(indicators, 'id')

    return dataPromise.then(function (data) {
      if (!data || data.length === 0) {
        return { options: null, data: null }
      }
      var total = _(data).map(function (n) { return n.value }).sum()
      var chartOptions = {
        aspect: aspects[layout].pieChart,
        domain: _.constant([0, total]),
        name: d => _.get(idx, '[' + d.indicator + '].name', ''),
        margin: {
          top: 0,
          right: 200,
          bottom: 0,
          left: 0
        }
      }
      return { options: chartOptions, data: data }
    })
  },
  processChoroplethMap: function (dataPromise, locations, indicators, xAxis, yAxis, zAxis, layout) {
    var locationsIndex = _.indexBy(locations, 'id')
    return Promise.all([dataPromise, api.geo({ location__in: _.map(locations, function (location) { return location.id }) }, null, {'cache-control': 'max-age=604800, public'})])
    .then(_.spread(function (data, border) {
      var chartOptions = {
        aspect: aspects[layout].choroplethMap,
        name: d => _.get(locationsIndex, '[' + d.properties.location_id + '].name', ''),
        border: border.objects.features
      }
      if (!data || data.length === 0) {
        return { options: chartOptions, data: border.objects.features }
      }

      let indicatorIndex = _(data).groupBy('indicator').value()
      let index = _.indexBy(indicatorIndex[xAxis], 'location')
      let bubbleIndex = null
      let gradientIndex = null
      if (yAxis) {
        let maxValue = 5000
        let bubbleValues = indicatorIndex[yAxis].map(v => v.value)
        bubbleIndex = _.indexBy(indicatorIndex[yAxis], 'location')
        chartOptions.maxBubbleValue = Math.min(Math.max(...bubbleValues), maxValue)
        chartOptions.bubbleValue = _.property('properties.bubbleValue')
      }
      if (zAxis) {
        gradientIndex = _.indexBy(indicatorIndex[zAxis], 'location')
        chartOptions.indicatorName = _.result(_.find(indicators, d => { return d.id === zAxis }), 'short_name')
        chartOptions.stripeValue = _.property('properties.stripeValue')
      }

      var chartData = _.map(border.objects.features, function (feature) {
        var location = _.get(index, feature.properties.location_id)
        let properties = {value: _.get(location, 'value')}
        if (yAxis) {
          let bubbleLocation = _.get(bubbleIndex, feature.properties.location_id)
          properties.bubbleValue = _.get(bubbleLocation, 'value')
        }
        if (zAxis) {
          let gradientLocation = _.get(gradientIndex, feature.properties.location_id)
          properties.stripeValue = _.get(gradientLocation, 'value')
        }
        return _.merge({}, feature, {properties: properties})
      })

      return { options: chartOptions, data: chartData }
    }))
  },
  processColumnChart: function (dataPromise, lower, upper, groups, groupBy, layout) {
    return dataPromise.then(function (data) {
      if (!data || data.length === 0) {
        return { options: null, data: null }
      }
      if (!lower) { // set the lower bound from the lowest datapoint value
        var sortedDates = _.sortBy(data, _.method('campaign.start_date.getTime'))
        lower = moment(_.first(sortedDates).campaign.start_date)
      }
      var columnScale = _.map(d3.time.scale()
          .domain([lower.valueOf(), upper.valueOf()])
          .ticks(d3.time.month, 1),
        _.method('getTime')
      )
      var chartData = _columnData(data, groups, groupBy)

      var chartOptions = {
        aspect: aspects[layout].columnChart,
        values: _.property('values'),
        domain: _.constant(columnScale),
        x: function (d) {
          var start = d.campaign.start_date
          return moment(start).startOf('month').toDate().getTime()
        },
        xFormat: function (d) { return moment(d).format('MMM YYYY') }
      }
      return { options: chartOptions, data: chartData }
    })
  },
  processScatterChart: function (dataPromise, locations, indicators, xAxis, yAxis, layout) {
    var locationsIndex = _.indexBy(locations, 'id')

    return dataPromise.then(function (data) {
      if (!data || data.length === 0) {
        return { options: null, data: null }
      }
      var domain = d3.extent(_(data.objects)
        .pluck('indicators')
        .flatten()
        .filter(function (d) {
          return +d.indicator === xAxis
        })
        .pluck('value')
        .value()
      )
      var range = d3.extent(_(data.objects)
        .pluck('indicators')
        .flatten()
        .filter(function (d) {
          return +d.indicator === yAxis
        })
        .pluck('value')
        .value()
      )

      var chartData = _(data.objects)
        .map(function (d) {
          var index = _.indexBy(d.indicators, 'indicator')

          return {
            id: d.location,
            name: locationsIndex[d.location].name,
            x: value(index[xAxis]),
            y: value(index[yAxis])
          }
        })
        .filter(function (d) {
          return _.isFinite(d.x) && _.isFinite(d.y)
        })
        .value()
      var showTooltip = function () {}
      var hideTooltip = function () {}
      var chartOptions = {
        aspect: aspects[layout].scatterChart,
        domain: _.constant(domain),
        onMouseOut: hideTooltip,
        onMouseOver: showTooltip,
        range: _.constant(range),
        xLabel: 'Caregiver Awareness',
        yLabel: 'Missed Children'
      }
      return { options: chartOptions, data: chartData }
    })
  },
  processBarChart: function (dataPromise, locations, indicators, layout) {
    return dataPromise.then(function (data) {
      if (!data || data.length === 0) {
        return { options: null, data: null }
      }
      var indicatorsIndex = _.indexBy(indicators, 'id')
      var locationsIndex = _.indexBy(locations, 'id')
      var datapoints = _(data)
        .thru(util.unpivot)
        .forEach(function (d) {
          d.indicator = indicatorsIndex[d.indicator]
          d.location = locationsIndex[d.location]
        })
        .groupBy(function (d) {
          return d.indicator.id
        }).value()

      var locationMapping = {
        'value': 'x',
        'location.name': 'y'
      }

      var chartOptions = {
        aspect: aspects[layout].barChart,
        offset: 'zero',
        yFormat: String
      }
      var chartData = _barData(datapoints, _.pluck(indicators, 'id'), locationMapping, _getIndicator)
      return { options: chartOptions, data: chartData }
    })
  }
}
