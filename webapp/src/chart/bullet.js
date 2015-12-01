import _ from 'lodash'
import d3 from 'd3'

import qualitativeAxis from './qualitative-axis'

var defaults = {
  domain: _.constant([0, 1]),
  fontSize: 11,
  lineHeight: 1.3,
  padding: 0,
  scale: d3.scale.linear,
  thresholds: [],
  targets: [],
  format: String,

  margin: {
    top: 0,
    right: 0,
    bottom: 0,
    left: 0
  }
}

function BulletChart () {
}

_.extend(BulletChart.prototype, {
  defaults: defaults,

  initialize: function (el, data, options) {
    options = this._options = _.defaults({}, options, defaults)

    var n = Math.max(data.length, 1)
    var height = options.fontSize * n * options.lineHeight +
      options.fontSize * options.padding * (n - 1) +
      options.margin.top +
      options.margin.bottom

    this._width = el.clientWidth

    var svg = this._svg = d3.select(el).append('svg')
      .attr({
        'viewBox': '0 0 ' + this._width + ' ' + height,
        'width': this._width,
        'height': height
      })

    // Append the x-axis container and a blank background
    svg.append('g').attr('class', 'x axis')

    // Append a data layer
    svg.append('g')
      .attr({
        'class': 'data',
        'transform': 'translate(' + options.margin.left + ', ' + options.margin.top + ')'
      })

    this.update(data)
  },

  update: function (data, options) {
    options = _.assign(this._options, options)

    var margin = options.margin
    var svg = this._svg

    var n = Math.max(data.length, 1)
    var h = options.fontSize * n * options.lineHeight + options.fontSize * options.padding * (n - 1)
    var w = this._width - margin.left - margin.right

    var yScale = d3.scale.ordinal()
      .domain(_(data).flatten().map(options.y).uniq().value())
      .rangeRoundBands([h, 0])

    var y = _.flow(options.y, yScale)

    var xScale = options.scale()
      .domain(options.domain(data))
      .range([0, w])

    var x = _.flow(options.marker, xScale)
    var width = _.flow(options.value, xScale)

    var isEmpty = !_(data).map(options.value).all(_.isFinite)

    // Draw qualitative ranges
    if (!(isEmpty || _.isEmpty(options.thresholds) || _.isEmpty(options.targets))) {
      var tick = svg.select('.x.axis').selectAll('.tick').data(data)

      tick.enter()
        .append('g')
        .attr('class', 'tick')
        .style('fill', options.axisFill)
      tick.exit().remove()

      var rect = tick.selectAll('rect').data(function (d) {
        return isEmpty ? [] : [d]
      })
      rect.enter().append('rect')
        .style('fill', 'inherit')

      rect
        .attr({
          'height': h + margin.top + margin.bottom,
          'width': w,
          'ry': 5
        })
    } else {
      svg.select('.x.axis')
        .call(qualitativeAxis()
          .height(h + margin.top + margin.bottom)
          .width(w)
          .scale(xScale)
          .threshold(d3.scale.threshold()
            .domain([])
            .range([''])
        )
          .colors(['#F2F2F2', '#F2F2F2'])
      )
    }

    svg.attr({
      'viewBox': '0 0 ' + w + ' ' + (h + margin.top + margin.bottom),
      'width': w,
      'height': h + margin.top + margin.bottom
    })

    svg.select('.data')
      .call(qualitativeAxis()
      .height(h + margin.top + margin.bottom)
      .width(w)
      .scale(xScale)
      .threshold(d3.scale.threshold().domain(options.thresholds).range(options.targets))
    )

    var g = svg.select('.data')
      .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')')

    // Draw value
    var bar = g.selectAll('.bar').data(data)

    bar.enter().append('g')
    bar
      .attr({
        'class': 'bar',
        'y': y
      })
      .style('fill', options.dataFill)
    bar.exit().remove()

    var value = bar.selectAll('.value').data(function (d) {
      return isEmpty ? [] : [d]
    })

    var valueAttr = {
      'class': 'value',
      'height': yScale.rangeBand(),
      'ry': 5
    }

    value.enter()
      .append('rect')
      .attr(valueAttr)
      .style({
        'fill': 'inherit',
        'stroke': '#fff'
      })

    value.attr(valueAttr)
      .transition()
      .duration(500)
      .attr('width', width)
    value.exit().remove()

     // Draw comparitive measure
    var measure = bar.selectAll('.comparative-measure')
      .data(function (d) {
        var v = options.value(d)
        var m = options.marker(d)
        return _.isFinite(v) && _.isFinite(m) ? [d] : []
      })

    var measureHeight = yScale.rangeBand() * 0.5

    var initAttr = {
      'class': 'comparative-measure',
      'width': 3,
      'height': yScale.rangeBand() + measureHeight,
      'y': -measureHeight / 2
    }

    measure.enter().append('rect').attr(initAttr)
      .style('fill', 'inherit')
    measure.attr(initAttr).attr('x', x)
    measure.exit().remove()

    var label = bar.selectAll('.label')
      .data(function (d) {
        var v = options.value(d)
        return _.isFinite(v) ? [v] : []
      })

    label.enter()
      .append('text')
      .attr({
        'class': 'label'
      })

    label
      .attr({
        'x': w,
        'y': -0.1 * w,
        'text-anchor': 'end',
        'dy': -(options.lineHeight / 4) + 'em',
        'transform': 'translate(0, ' + (h / 2) + ')',
        'fill': 'inherit'
      })
      .style('font-size', options.fontSize)
      .text(options.format)
    label.exit().remove()

    var compareValue = bar.selectAll('.comparative-text')
      .data(function (d) {
        var v = options.value(d)
        return width(d) > options.fontSize * 2 ? [options.valueText(v)] : [options.valueText(v).slice(0, 1)]
      })

    compareValue.enter().append('text')
      .attr('class', 'comparative-text')

    compareValue
      .attr({
        'x': 4,
        'y': 0,
        'text-anchor': 'start',
        'dy': (options.lineHeight / 4) + 'em',
        'transform': 'translate(0, ' + (h / 2) + ')',
        'fill': '#FFFFFF'
      })
      .style('font-size', options.fontSize - 2)
      .text(d => { return d })
    compareValue.exit().remove()
  },

  resize: function (el) {}
})

export default BulletChart
