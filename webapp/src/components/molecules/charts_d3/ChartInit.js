import _ from 'lodash'
import moment from 'moment'

export function choropleth (chart, data, campaign, features) {
  // Make sure we only get data for the current campaign maps can't
  // display historical data. Index by location for quick lookup.

  const dataIdx = _(data).filter(d => d.campaign.id === campaign.id).indexBy('location.id').value()

  features.forEach(f => {
    const d = dataIdx[f.properties.location_id]
    if (d) f.properties[d.indicator.id] = d.value
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

function table (chart, data, campaign, features, indicators, locations) {
  const indicatorIndex = _.indexBy(indicators, 'id')
  const tableChartIndicators = chart.indicators.map(id => indicatorIndex[id])
  return ChartInfo.getChartInfo(chart, data[0], locations, tableChartIndicators)
}

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

function chartInit (chart, datapoints, location, campaign, locations_index, campaigns_index, indicators_index, features) {
  // Merge location metadata into the properties object of each geographic feature // TO DO
  // features.forEach(f => _.assign(f.properties, locations_index[f.properties.location_id]))

  // Fill in indicators and locations on all the datapoints objects. If we haven't
  // loaded indicators yet, continue displaying charts as if we have no datapoints
  datapoints.forEach(d => {
    d.indicator = indicators_index[d.indicator] ? indicators_index[d.indicator] : d.indicator
    d.location = locations_index[d.location] ? locations_index[d.location] : d.location
  })

  if (chart.location_ids && chart.location_ids.length === 1) {
    location = locations_index[chart.location_ids]
  }

  if (chart.campaignValue && campaigns_index[chart.campaignValue]) {
    campaign = campaigns_index[chart.campaignValue]
  }

  let chartData = datapoints.filter(datapoint => inChart(chart, campaign, location, datapoint))

  return _.get(process, chart.type, _.constant(chartData))(
    chart,
    chartData,
    campaign,
    features,
    indicators_index,
    locations_index
  )
}

export default {
  chartInit: chartInit
}