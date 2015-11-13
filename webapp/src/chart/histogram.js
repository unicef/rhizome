'use strict'

import _ from 'lodash'
import d3 from 'd3'

var DEFAULTS = {
  className: _.constant(''),
  format: d3.format('n'),
  value: _.property('value'),
  yAxisTitle: '',
  margin: {
    top: 12,
    right: 6,
    bottom: 12,
    left: 12
  }
}

function Histogram () {}

_.extend(Histogram.prototype, {
  defaults: DEFAULTS,

  update: function (data, options) {
    options = _.assign(this._options, options)

    var margin = options.margin
    var w = this._width - margin.left - margin.right
    var h = this._height - margin.top - margin.bottom

    var svg = this._svg.datum(data)
    var g = svg.select('.data')

    var histogram = d3.layout.histogram().value(options.value)

    var buckets = histogram(_.filter(data, d => _.isFinite(options.value(d))))

    var domain = [
      d3.min(buckets, _.property('x')),
      d3.max(buckets, d => d.x + d.dx)
    ]
    var xScale = d3.scale.linear().domain(domain).range([0, w])
    var x = d => xScale(d.x)
    var width = d => xScale(d.x + d.dx) - xScale(d.x)

    var yScale = d3.scale.linear()
      .domain([0, d3.max(buckets, _.property('y'))])
      .range([h, 0])

    var y = d => yScale(d.y)

    var bin = g.selectAll('.bin').data(buckets)

    var transform = d => 'translate(' + x(d) + ', ' + y(d) + ')'

    bin.enter()
      .append('g')
      .attr({
        'class': 'bin',
        'transform': d => 'translate(' + x(d) + ', ' + h + ')'
      })

    bin.transition().duration(500).attr('transform', transform)

    bin.exit().remove()

    var bar = bin.selectAll('.bar').data(d => [d])

    bar.enter().append('rect')
      .attr({
        'class': 'bar',
        'width': width,
        'height': 0
      })

    bar.transition()
      .duration(500)
      .attr({
        'width': width,
        'height': d => h - yScale(d.y),
        'class': d => 'bar ' + options.className(d)
      })

    var label = bin.selectAll('.label').data(d => [d])
    var labelTransform = d => 'translate(' + (width(d) / 2) + ', 0)'

    label.enter()
      .append('text')
      .attr({
        'class': 'label',
        'text-anchor': 'middle',
        'dy': '-.2em',
        'transform': labelTransform
      })

    // We know these are counts, so we don't need a formatter
    label
      .attr('transform', labelTransform)
      .text(d => d3.format('n')(d.y))

    var tickValues = _(buckets)
      .pluck('x')
      .push(xScale.domain()[1])
      .value()

    // Formatter is for the x-axis because we don't know what the data is
    var axis = d3.svg.axis()
      .scale(xScale)
      .tickValues(tickValues)
      .tickPadding(0)
      .outerTickSize(0)
      .orient('bottom')

    svg.select('.x.axis')
      .attr('transform', 'translate(0, ' + h + ')')
      .call(axis)

    var yAxis = svg.select('.y.axis')
      .selectAll('text')
      .data([options.yAxisTitle])

    yAxis.enter().append('text')

    yAxis.attr({
      'transform': 'translate(0, ' + (h / 2) + ') rotate(-90)',
      'text-anchor': 'middle',
      'dy': '-6'
    })
    .text(String)
  }
})

module.exports = Histogram
