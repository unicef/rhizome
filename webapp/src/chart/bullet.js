import _ from 'lodash'
import d3 from 'd3'
import React from 'react'
import Layer from 'react-layer'
import Tooltip from 'component/Tooltip.jsx'
import browser from 'util/browser'

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

    var aspect = _.get(options, 'aspect', 1)
    this._width = el.clientWidth
    this._height = _.get(options, 'height', this._width / aspect)

    var svg = this._svg = d3.select(el).append('svg')
      .attr({
        'viewBox': '0 0 ' + this._width + ' ' + this._height
      })

    if (browser.isIE() || browser.isWkhtmlToPdf()) {
      svg.attr({
        'width': this._width,
        'height': this._height
      })
    }

    // Append the x-axis container and a blank background
    svg.append('g').attr('class', 'x axis')

    // Append a data layer
    svg.append('g')
      .attr({
        'class': 'data',
        'transform': 'translate(' + options.margin.left + ', ' + options.margin.top + ')'
      })

    svg.append('g').attr('class', 'legend')

    this.update(data)
  },

  update: function (data, options) {
    options = _.assign(this._options, options)

    var margin = options.margin
    var svg = this._svg

    var h = this._height
    var w = this._width - margin.left - margin.right
    var dataHeight = h / 3

    var yScale = d3.scale.ordinal()
      .domain(_(data).flatten().map(options.y).uniq().value())
      .rangeRoundBands([dataHeight, 0])

    var y = _.flow(options.y, yScale)

    var xScale = options.scale()
      .domain(options.domain(data))
      .range([0, w])

    var x = _.flow(options.marker, xScale)
    var width = _.flow(options.value, xScale)
    var measureHeight = _.isFinite(yScale.rangeBand()) ? yScale.rangeBand() * 0.5 : 0
    var rectStartPosition = this._height - dataHeight - measureHeight + margin.top

    var isEmpty = !_(data).map(options.value).all(_.isFinite)

    svg.select('.x.axis').attr('transform', 'translate(0, ' + rectStartPosition + ')')

    // Draw qualitative ranges
    if (!(isEmpty || _.isEmpty(options.thresholds) || _.isEmpty(options.targets))) {
      var tick = svg.select('.x.axis').selectAll('.tick').data(data)

      tick.enter()
        .append('g')
        .attr({
          'class': 'tick'
        })
        .style('fill', options.axisFill)
      tick.exit().remove()

      var rect = tick.selectAll('rect').data(function (d) {
        return isEmpty ? [] : [d]
      })
      rect.enter().append('rect')
        .style('fill', 'inherit')

      rect
        .attr({
          'height': dataHeight,
          'width': w,
          'ry': 5
        })
    } else {
      svg.select('.x.axis')
        .call(qualitativeAxis()
          .height(dataHeight)
          .width(w)
          .scale(xScale)
          .threshold(d3.scale.threshold()
            .domain([])
            .range([''])
        )
          .colors(['#F2F2F2', '#F2F2F2'])
      )
    }

    svg.select('.data')
      .call(qualitativeAxis()
      .height(dataHeight)
      .width(w)
      .scale(xScale)
      .threshold(d3.scale.threshold().domain(options.thresholds).range(options.targets))
    )

    var g = svg.select('.data')
      .attr('transform', 'translate(' + margin.left + ', ' + rectStartPosition + ')')

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

    var legend = svg.select('.legend').attr('transform', 'translate(0, ' + options.fontSize + ')')
    let noDataColor = '#B9C3CB'

    var title = legend.selectAll('.title').data(data)
    title.enter().append('text')
      .attr({
        'class': 'title',
        'text-anchor': 'start'
      })
      .style({
        'font-size': options.fontSize,
        'fill': d => { return _.isFinite(options.value(d)) ? options.dataFill(d) : noDataColor }
      })
      .text(d => { return options.indicatorName(d) })
      .on('mousemove', d => {
        var evt = d3.event
        var render = function () {
          return (
            <Tooltip left={evt.pageX} top={evt.pageY}>
              <div>
                <h3>{options.indicatorName(d)}</h3>
                <p>{options.indicatorDescription(d)}</p>
              </div>
            </Tooltip>
          )
        }

        if (this.layer) {
          this.layer._render = render
        } else {
          this.layer = new Layer(document.body, render)
        }

        this.layer.render()
      })
      .on('mouseout', d => {
        if (this.layer) {
          this.layer.destroy()
          this.layer = null
        }
      })

    title.exit().remove()

    var label = legend.selectAll('.label').data(data)

    label.enter().append('text')
      .attr({
        'class': 'label',
        'x': w,
        'text-anchor': 'end',
        'fill': options.dataFill
      })
      .style('font-size', options.fontSize)
      .text(d => {
        var v = options.value(d)
        return _.isFinite(v) ? [options.format(v)] : []
      })

    label.exit().remove()

    var compareValue = bar.selectAll('.comparative-text')
      .data(function (d) {
        var v = options.value(d)
        var text = options.valueText(v)
        return !_.isUndefined(text)
          ? width(d) > options.fontSize * 2 ? [text] : [text.slice(0, 1)]
          : ''
      })

    compareValue.enter().append('text')
      .attr('class', 'comparative-text')

    compareValue
      .attr({
        'x': 4,
        'y': 0,
        'text-anchor': 'start',
        'transform': 'translate(0, ' + ((yScale.rangeBand() + measureHeight) / 2) + ')',
        'fill': '#FFFFFF'
      })
      .style('font-size', options.fontSize - 2)
      .text(d => { return d })
    compareValue.exit().remove()
  },

  resize: function (el) {}
})

export default BulletChart
