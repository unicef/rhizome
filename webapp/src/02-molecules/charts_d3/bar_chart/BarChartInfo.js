import _ from 'lodash'
import aspects from '02-molecules/charts_d3/utils/aspects'
import chartOptionsHelpers from '02-molecules/charts_d3/utils/chartOptionsHelpers'
import util from '02-molecules/charts_d3/bar_chart/util'
import path from '02-molecules/charts_d3/bar_chart/path'

const processBarChart = (data, locations, indicators, chartDef, layout) => {
  if (!data || data.length === 0) {
    return { options: null, data: null }
  }
  const indicatorsIndex = _.indexBy(indicators, 'id')
  const locationsIndex = _.indexBy(locations, 'id')
  const datapoints = _(data)
    .thru(util.unpivot)
    .forEach(d => {
      d.indicator = indicatorsIndex[d.indicator]
      d.location = locationsIndex[d.location]
    })
    .groupBy(d => {
      return d.indicator.id
    }).value()

  const locationMapping = {
    'value': 'x',
    'location.name': 'y'
  }

  let chartOptions = {
    aspect: aspects[layout].barChart,
    offset: 'zero',
    yFormat: String,
    xLabel: chartDef.xLabel,
    yLabel: chartDef.yLabel
  }
  chartOptions = chartOptionsHelpers.generateMarginForAxisLabel(chartOptions)
  const chartData = barData(datapoints, _.pluck(indicators, 'id'), locationMapping, _getIndicator)
  return { options: chartOptions, data: chartData }
}

const barData = (datapoints, indicators, properties, series) => {
  return _(datapoints)
    .pick(indicators)
    .values()
    .flatten()
    .map(mapProperties(properties))
    .thru(filterMissing)
    .thru(makeSeries(series))
    .value()
}

const mapProperties = (mapping) => {
  return d => {
    const datum = _.clone(d)
    _.forEach(mapping, (to, from) => {
      path.set(datum, to, path.get(datum, from))
    })

    return datum
  }
}

const filterMissing = (data) => {
  return _(data)
    .groupBy('y')
    .filter(v => {
      return _(v).pluck('x').some(_.partial(util.defined, _, _.identity))
    })
    .values()
    .flatten()
    .forEach(d => {
      if (!util.defined(d.x)) {
        d.x = 0
      }
    })
    .value()
}

const makeSeries = (getSeries) => {
  return data => {
    return _(data)
      .groupBy(getSeries)
      .map((v, k) => {
        return {
          name: k,
          values: v
        }
      })
      .value()
  }
}

const _getIndicator = (d) => {
  return d.indicator.short_name
}

export default processBarChart
