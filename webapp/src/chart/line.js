import _ from 'lodash'
import d3 from 'd3'

import format from 'util/format'
import hoverLine from 'chart/behavior/hover-line'
import label from 'chart/renderer/label'

var DEFAULTS = {
  margin: {
    top: 12,
    right: 0,
    bottom: 12,
    left: 0
  },
  scale: d3.scale.linear,
  seriesName: _.property('name'),
  values: _.property('values'),
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

    var margin = options.margin

    var svg = this._svg
    var width = this._width - margin.left - margin.right
    var height = this._height - margin.top - margin.bottom

    var dataColor = options.color
    var colorRange = ['#377EA3', '#D95348', '#82888e', '#98a0a8', '#b6c0cc']

    if (!_.isFunction(dataColor)) {
      var dataColorScale = d3.scale.ordinal()
        .domain(_(series)
          .map(options.seriesName)
          .uniq()
          .sortBy()
          .value())
        .range(colorRange)

      dataColor = _.flow(options.seriesName, dataColorScale)
    }

    var domain = _.isFunction(options.domain)
      ? options.domain(series)
      : d3.extent(_(series)
      .map(options.values)
      .flatten()
      .map(options.x)
      .value())

    var dataXScale = d3.time.scale()
      .domain(domain)
      .range([30, width])

    var range = _.isFunction(options.range)
      ? options.range(series)
      : d3.extent(_(series)
      .map(options.values)
      .flatten()
      .map(options.y)
      .value())

    range[0] = Math.min(range[0], 0)

    var yScale = options.scale()
      .domain(range)
      .range([0.95 * height, 0])

    var x = _.flow(options.x, dataXScale)
    var y = _.flow(options.y, yScale)

    var g = svg.select('.data')
      .selectAll('.series')
      .data(series, options.seriesName)

    g.enter()
      .append('g')
      .attr('class', 'series')

    g.style({
      'fill': dataColor,
      'stroke': dataColor
    })

    g.exit().remove()

    var path = g.selectAll('path')
      .data(function (d) {
        return [options.values(d)]
      })

    path.enter().append('path')

    path.transition()
      .duration(500)
      .attr('d', d3.svg.line().x(x).y(y))

    g.selectAll('line').data(options.values)

    var labels = _(series)
      .map(function (d) {
        var last = _.max(options.values(d), options.x)
        var v = options.y(last)

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

    var legendColorScale = d3.scale.ordinal()
      .domain(_(labels)
        .map(function (d) {
          return d.text
        })
        .uniq()
        .sortBy()
        .value())
      .range(colorRange)

    var legendColor = _.flow(function (d) {
      return d.text
    }, legendColorScale)

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
        .colorRange(colorRange)
        .datapoints(_(series).map(function (s) {
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

    svg.select('.x.axis').selectAll('.domain').data([0])
      .attr('d', 'M' + 0 + ',' + 0 + 'V0H' + width + 'V' + 0)

    var gy = svg.select('.y.axis')
      .call(d3.svg.axis()
        .tickFormat(options.yFormat)
        .tickSize(width)
        .ticks(3)
        .scale(yScale)
        .orient('right'))

    gy.selectAll('text')
      .attr({
        'x': 4,
        'dy': 10
      })

    d3.select(gy.selectAll('text')[0][0]).attr('visibility', 'hidden')

    gy.selectAll('g').classed('minor', function (d) {
      return d !== range[0]
    })
  }
})

export default LineChart
