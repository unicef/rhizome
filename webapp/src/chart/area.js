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
  y0: _.property('y0'),
  yFormat: d3.format(',d')
}

function AreaChart () {}

_.extend(AreaChart.prototype, {
  defaults: DEFAULTS,

  update: function (originalData, options) {
    var series = function (values, name) {
      return {
        name: name,
        values: _.sortBy(values, _.result('campaign.start_date.getTime'))
      }
    }

    var stack = d3.layout.stack()
      .order('default')
      .offset('zero')
      .values(_.property('values'))
      .x(_.property('campaign.start_date'))
      .y(_.property('value'))

    try {
      var data = _(originalData)
        .groupBy('indicator.short_name')
        .map(series)
        .thru(stack)
        .value()
    } catch (err) {
      console.error(err)
      console.log(`Data error in ${originalData}`)
      data = []
    }

    data = _(data).filter(serie => {
      serie.values = _(serie.values).reject(item => {
        return item.value === null
      }).value()
      return serie.values.length > 0
    }).value()

    options = _.assign(this._options, options)

    var margin = options.margin
    var dataMarginLeft = 25

    var svg = this._svg
    var width = this._width - margin.left - margin.right
    var height = this._height - margin.top - margin.bottom

    var fillColor = options.fill
    var strokeColor = options.stroke

    if (!_.isFunction(fillColor)) {
      var fillColorScale = d3.scale.ordinal()
        .domain(_.map(data, options.seriesName))
        .range(['#D8D9E1', '#E5E9EC', '#A2AAB3', '#C4D9DC'])
      fillColor = _.flow(options.seriesName, fillColorScale)
    }

    if (!_.isFunction(strokeColor)) {
      var strokeColorScale = d3.scale.ordinal()
        .domain(_.map(data, options.seriesName))
        .range(['#B0B3C3', '#B9C3CB', '#87939F', '#707070'])
      strokeColor = _.flow(options.seriesName, strokeColorScale)
    }

    var domain = _.isFunction(options.domain)
      ? options.domain(data)
      : d3.extent(_(data)
      .map(options.values)
      .flatten()
      .map(options.x)
      .value())

    var xScale = d3.time.scale()
      .domain(domain)
      .range([dataMarginLeft, width])

    var range = _.isFunction(options.range)
      ? options.range(data)
      : d3.extent(_(data).map(options.values).flatten().value(), d => { return options.y0(d) + options.y(d) })

    range[0] = 0

    var yScale = options.scale()
      .domain(range)
      .range([height, 0])

    var x = d => { return xScale(options.x(d)) }
    var y = d => { return yScale(options.y(d)) }
    var y0 = d => { return yScale(options.y(d)) }
    if (options.y0) {
      y = d => { return yScale(options.y0(d) + options.y(d)) }
      y0 = d => { return yScale(options.y0(d)) }
    }

    var points = _(data)
      .map(d => { return _.map(options.values(d), _.partial(_.set, _, 'seriesName', options.seriesName(d))) })
      .flatten()
      .value()

    svg.attr('class', 'area')
      .call(hoverLine()
        .width(width)
        .height(height)
        .xFormat(options.xFormat)
        .yFormat(options.yFormat)
        .x(options.x)
        .y(d => { return d.y0 ? (options.y(d) + options.y0(d)) : options.y(d) })
        .xScale(xScale)
        .yScale(yScale)
        .value(options.y)
        .seriesName(options.withoutSeriesName ? null : _.property('seriesName'))
        .sort(true)
        .total(options.total)
        .datapoints(points)
    )

    var g = svg.select('.data')
      .selectAll('.series')
      .data(data, options.seriesName)

    g.enter()
      .append('g')
      .attr('class', 'series')

    g.style({
      'fill': fillColor,
      'stroke': strokeColor,
      'stroke-width': 2,
      'opacity': 0.6
    })

    g.exit().remove()

    var path = g.selectAll('path')
      .data(function (d) {
        return [options.values(d)]
      })

    path.enter().append('path')

    var area = d3.svg.area()
      .x(x)
      .y0(y0)
      .y1(y)

    path.transition()
      .duration(500)
      .attr('d', area)

    var labels = _(data)
      .map(function (d) {
        var last = _.max(options.values(d), options.x)
        var v = options.y(last)

        var text = options.withoutSeriesName ? options.yFormat(v) : (options.seriesName(d) + ' ' + options.yFormat(v))

        return {
          text: text,
          x: x(last),
          y: y(last),
          defined: _.isFinite(v),
          value: v
        }
      })
      .filter('defined')
      .sortBy('y')
      .value()

    if (options.total) {
      var v = _.sum(labels, d => { return d.value })
      labels.unshift({
        x: width,
        y: 0,
        text: 'TOTAL ' + options.yFormat(v),
        defined: _.isFinite(v),
        value: v
      })
    }

    svg.select('.annotation')
      .selectAll('.series.label')
      .data(labels)
      .call(label()
        .addClass('series')
        .width(width)
        .height(height)
        .align(false))

    svg.select('.x.axis')
      .call(d3.svg.axis()
        .tickFormat(options.xFormat)
        .outerTickSize(0)
        .ticks(4)
        .scale(xScale)
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

export default AreaChart
