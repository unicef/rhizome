import _ from 'lodash'
import d3 from 'd3'
import moment from 'moment'

import ChartInfo from 'components/molecules/charts_d3/ChartInfo'

/**
 * Return the facet value for a datum given a path.
**/
export function getFacet (datum, path) {
  var facet = _.get(datum, path)

  // Handle pieces of the application that replace IDs with their
  // corresponding objects, and those that don't. For example, if the facet path
  // is 'indicator', but the datum has the indicator ID replaced by the
  // definition we try a number of properties. If the indicator hasn't been
  // replaced, we just use the ID.
  if (_.isPlainObject(facet)) {
    facet = _(['short_name', 'name', 'title', 'id'])
      .map(_.propertyOf(facet))
      .reject(f => _.isUndefined(f))
      .first()
  }

  return facet
}

/**
 * Recursively determine if child is a child of parent location.
 */
export function childOf (parent, child) {
  return child && child.parent
    ? parent.id === child.parent.id || childOf(parent, child.parent)
    : !!child.parent_location_id && parent.id === child.parent_location_id
}

export function inChart (chart, campaign, location, datum) {
  var dt = moment(datum.campaign.start_date).valueOf()
  var end = moment(campaign.start_date, 'YYYY-MM-DD')
  var start = -Infinity

  if (!_.isNull(_.get(chart, 'timeRange', null))) {
    start = end.clone().subtract(chart.timeRange).valueOf()
  }

  var inPeriod = dt >= start && dt <= end.valueOf()

  var inlocation = false

  switch (chart.locations) {
    case 'sublocations':

      inlocation = childOf(location, datum.location) || datum.location.location_type_id === 3
      // FIXME --> this ( || datum.location.location_type_id === 3 )
      // should read something like ... || there exist no shapes below this...
      // however since we have only district level shape data.. this works
      // for now.

      if (!_.isEmpty(chart.level)) {
        inlocation = inlocation && chart.level === datum.location.location_type
      }
      break

    case 'type':
      inlocation = datum.location.location_type === location.location_type
      break

    default:
      inlocation = location.id === datum.location.id
      break
  }

  return _.includes(chart.indicators, datum.indicator.id) && inPeriod && inlocation
}

export function choropleth (chart, data, campaign, features) {
  // Make sure we only get data for the current campaign maps can't
  // display historical data. Index by location for quick lookup.

  var dataIdx = _(data)
    .filter(d => d.campaign.id === campaign.id)
    .indexBy('location.id')
    .value()

  _.each(features, f => {
    var d = dataIdx[f.properties.location_id]
    if (d) {
      f.properties[d.indicator.id] = d.value
    }
  })

  return features
}

export function series (chart, data) {
  return _(data)
    .groupBy(_.partial(getFacet, _, _.get(chart, 'groupBy')))
    .map((originalValues, name) => {
      var values = _.reject(originalValues, d => !d.value || d.value === 0 || !_.isFinite(d.value))
      return { name, values }
    })
    .value()
}

function stackedData (chart, data) {
  var s = series(chart, data)
  var x

  switch (chart.type) {
    case 'BarChart':
      x = chart.groupBy === 'indicator' ? 'location.name' : 'indicator.short_name'
      break

    default:
      x = 'campaign.start_date'
      break
  }

  var domain = _(data)
    .filter(d => _.isFinite(d.value))
    .pluck(x)
    .uniq()
    .value()

  _.each(s, function (dataSeries) {
    var missing = _.difference(domain, _.pluck(dataSeries.values, x))

    _.each(missing, function (xval) {
      var o = { value: 0 }
      _.set(o, x, xval)
      dataSeries.values.push(o)
    })
  })

  return s
}

function column (chart, data) {
  var s = stackedData(chart, data)
  var stack = d3.layout.stack()
    .offset('zero')
    .values(d => d.values)
    .x(d => d.campaign.start_date)
    .y(d => d.value)

  return stack(s)
}

function scatter (chart, data, campaign) {
  return _(data)
    .filter(d => d.campaign.id === campaign.id)
    .groupBy('location.id')
    .map(values => {
      return _.reduce(values, (result, d) => {
        _.defaults(result, d)

        result[d.indicator.id] = d.value

        return _.omit(result, 'indicator', 'value')
      }, {})
    })
    .filter(d => _(d).omit('location', 'campaign').values().all(_.isFinite))
    .value()
}

function table (chart, data, campaign, features, indicators, locations, dashboard) {
  const indicatorIndex = _.indexBy(indicators, 'id')
  const tableChartIndicators = chart.indicators.map(id => indicatorIndex[id])
  return ChartInfo.getChartInfo(chart, data[0], locations, tableChartIndicators)
}

var process = {
  'BarChart': stackedData,
  'ChoroplethMap': choropleth,
  'ColumnChart': column,
  'HeatMapChart': series,
  'LineChart': series,
  'ScatterChart': scatter,
  'TableChart': table
}

function dashboardInit (dashboard, data, location, campaign, locationList, campaignList, indicators, features, responses) {
  var results = {}

  var indicatorsById = _.indexBy(indicators, 'id')
  var locationsById = _.indexBy(locationList, 'id')
  var campaignsById = _.indexBy(campaignList, 'id')

  // Merge location metadata into the properties object of each geographic feature
  _.each(features, function (f) {
    var id = f.properties.location_id
    _.assign(f.properties, locationsById[id])
  })

  // Fill in indicators and locations on all the data objects. If we haven't
  // loaded indicators yet, continue displaying charts as if we have no data
  _.each(data, function (d) {
    var ind = indicatorsById[d.indicator]
    if (ind) {
      d.indicator = ind
    }

    var reg = locationsById[d.location]
    if (reg) {
      d.location = reg
    }
  })

  var selectedCampaign = campaign
  var selectedLocation = location

  // Build up an object representing the data where each property of the object
  // corresponse to a section in the dashboard. Each section is an object where
  // each property corresponds to a chart. Each chart is an array of the data
  // that can be used by that chart

  var tableChartResponse = {}
  if (responses) {
    tableChartResponse = responses.filter(r => r.meta.chart_type === 'TableChart')
  }

  _.each(dashboard.charts, (chart, i) => {
    var sectionName = _.get(chart, 'section', '__none__')
    var chartName = _.get(chart, 'id', _.camelCase(chart.title))
    var section = _.get(results, sectionName, {})

    if (chart.location_ids) {
      var chartLocation = locationsById[chart.location_ids]
      if (chartLocation) location = chartLocation
    } else {
      location = selectedLocation
    }

    if (chart.campaignValue) {
      var chartCampaign = campaignsById[chart.campaignValue]
      if (chartCampaign) campaign = chartCampaign
    } else {
      campaign = selectedCampaign
    }

    var datumInChart = _.partial(inChart, chart, campaign, location)
    var chartData = _.filter(data, datumInChart)

    if (chart.type === 'TableChart') {
      chartData = tableChartResponse
    }

    var processedChart = _.get(process, chart.type, _.constant(chartData))(
      chart,
      chartData,
      campaign,
      features,
      indicators,
      locationList,
      dashboard
    )

    section[chartName] = processedChart
    results[sectionName] = section
  })

  if (_.size(results) < 2) {
    // Use a simple array if there is only one section
    results = _(results).values().flatten().first()
  }

  return results
}

export default {
  dashboardInit: dashboardInit
}
