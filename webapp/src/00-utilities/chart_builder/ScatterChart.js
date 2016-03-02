import _ from 'lodash'
import d3 from 'd3'
import aspects from '00-utilities/chart_builder/aspects'
import chartOptionsHelpers from '00-utilities/chart_builder/chartOptionsHelpers'

const processScatterChart = (data, locations, indicators, chartDef, layout) => {
  const locationsIndex = _.indexBy(locations, 'id')
  let xAxis = chartDef.x
  let yAxis = chartDef.y

  if (!data || data.length === 0) {
    return { options: null, data: null }
  }
  const domain = d3.extent(_(data.objects)
    .pluck('indicators')
    .flatten()
    .filter(d => {
      return +d.indicator === xAxis
    })
    .pluck('value')
    .value()
  )
  const range = d3.extent(_(data.objects)
    .pluck('indicators')
    .flatten()
    .filter(d => {
      return +d.indicator === yAxis
    })
    .pluck('value')
    .value()
  )

  const chartData = _(data.objects)
    .map(d => {
      const index = _.indexBy(d.indicators, 'indicator')

      return {
        id: d.location,
        name: locationsIndex[d.location].name,
        x: index[xAxis] && index[xAxis].hasOwnProperty('value') ? index[yAxis] : null,
        y: index[yAxis] && index[yAxis].hasOwnProperty('value') ? index[yAxis] : null
      }
    })
    .filter(d => {
      return _.isFinite(d.x) && _.isFinite(d.y)
    })
    .value()
  const showTooltip = () => {}
  const hideTooltip = () => {}
  let chartOptions = {
    aspect: aspects[layout].scatterChart,
    domain: _.constant(domain),
    onMouseOut: hideTooltip,
    onMouseOver: showTooltip,
    range: _.constant(range),
    xLabel: chartDef.xLabel,
    yLabel: chartDef.yLabel
  }
  chartOptions = chartOptionsHelpers.generateMarginForAxisLabel(chartOptions)
  return { options: chartOptions, data: chartData }
}

export default processScatterChart
