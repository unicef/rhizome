import _ from 'lodash'
import d3 from 'd3'

import hoverLine from '02-molecules/charts_d3/line_chart/hover-line'

import label from '02-molecules/charts_d3/renderer/label'
import axisLabel from '02-molecules/charts_d3/renderer/axis-label'

import palettes from '02-molecules/charts_d3/utils/palettes'
import format from '02-molecules/charts_d3/utils/format'

var DEFAULTS = {
  margin: {
    top: 12,
    right: 0,
    bottom: 20,
    left: 0
  },
  scale: d3.scale.linear,
  seriesName: _.property('name'),
  values: _.property('values'),
  color: palettes.blue,
  x: _.property('campaign.start_date'),
  xFormat: format.timeAxis,
  y: _.property('value'),
  yFormat: d3.format(',d')
}

function LineChart () {}

_.extend(LineChart.prototype, {
  defaults: DEFAULTS,

  update: function (series, options) {
    series = _(series).each(serie => {
      serie.values = _(serie.values).reject(item => {
        return item.value === null
      }).value()
    }).value()

    options = _.assign(this._options, options)

    const margin = options.margin
    const height = (options.height <= 2 ? this._height : options.height) - margin.top - margin.bottom
    const width = this._width - margin.left - margin.right
    const svg = this._svg

    // CHART COLORS
    // ---------------------------------------------------------------------------
    const dataColorScale = d3.scale.ordinal()
      .domain(_(series)
        .map(options.seriesName)
        .uniq()
        .sortBy()
        .value())
      .range(options.color)

    const dataColor = _.flow(options.seriesName, dataColorScale)

    const domain = _.isFunction(options.domain)
      ? options.domain(series)
      : d3.extent(_(series)
      .map(options.values)
      .flatten()
      .map(options.x)
      .value())

    let range = _.isFunction(options.range)
      ? options.range(series)
      : d3.extent(_(series)
      .map(options.values)
      .flatten()
      .map(options.y)
      .value())

    range[0] = Math.min(range[0], 0)

    const dataXScale = d3.time.scale().domain(domain).range([30, width])
    const yScale = options.scale().domain(range).range([0.9 * height, 0])

    const x = _.flow(options.x, dataXScale)
    const y = _.flow(options.y, yScale)

    const g = svg.select('.data').selectAll('.series').data(series, options.seriesName)
    g.enter().append('g').attr('class', 'series')
    g.style({ 'fill': dataColor, 'stroke': dataColor })
    g.exit().remove()

    const path = g.selectAll('path').data(d => [options.values(d)])
    path.enter().append('path')
    path.transition().duration(500).attr('d', d3.svg.line().x(x).y(y))

    g.selectAll('line').data(options.values)

    const labels = _(series)
      .map(d => {
        const last = _.max(options.values(d), options.x)
        const v = options.y(last)
        return {
          text: options.seriesName(d) + ' ' + options.yFormat(v),
          x: x(last),
          y: y(last),
          defined: _.isFinite(v)
        }
      })
      .filter('defined')
      .sortBy('y')
      .value()

    const legendColorScale = d3.scale.ordinal()
      .domain(_(labels).map(d => {
        console.log('d', d)
        return d.text
      }).uniq().sortBy().value())
      .range(options.color)

    const legendColor = _.flow(d => d.text, legendColorScale)

    svg.select('.annotation').selectAll('.series.label')
      .data(labels)
      .call(label()
        .addClass('series')
        .width(width)
        .height(height)
        .align(false)
        .scale(legendColor)
        .dots(options.hasDots))

    svg.attr('class', 'line')
      .call(hoverLine()
        .width(width)
        .height(height)
        .xFormat(options.xFormat)
        .yFormat(options.yFormat)
        .x(options.x)
        .y(options.y)
        .xScale(dataXScale)
        .yScale(yScale)
        .value(options.y)
        .seriesName(_.property('seriesName'))
        .sort(true)
        .colorRange(options.color)
        .datapoints(_(series).map(s => {
          return _.map(options.values(s), _.partial(_.set, _, 'seriesName', options.seriesName(s)))
        })
        .flatten()
        .value()
      )
    )

    svg.select('.x.axis')
      .call(d3.svg.axis()
        .tickFormat(options.xFormat)
        .outerTickSize(0)
        .ticks(3)
        .scale(dataXScale)
        .orient('bottom'))
    svg.select('.x.axis').selectAll('.domain').data([0]).attr('d', `M0,0V0H${width}V0`)

    const gy = svg.select('.y.axis')
      .call(d3.svg.axis()
        .tickFormat(options.yFormat)
        .tickSize(width)
        .ticks(3)
        .scale(yScale)
        .orient('right'))
    gy.selectAll('text').attr({'x': 4, 'dy': 10})
    gy.selectAll('g').classed('minor', d => d !== range[0])
    d3.select(gy.selectAll('text')[0][0]).attr('visibility', 'hidden')

    if (options.xLabel || options.yLabel) {
      svg.call(axisLabel()
      .data(options.xLabel, options.yLabel)
      .width(width)
      .height(height)
      .margin(options.margin))
    }
  }
})

export default LineChart
