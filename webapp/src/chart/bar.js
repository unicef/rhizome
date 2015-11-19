'use strict'

import _ from 'lodash'
import d3 from 'd3'
import React from 'react'
import Layer from 'react-layer'

import ColumnChart from './column'
import Tooltip from 'component/Tooltip.jsx'

import browser from 'util/browser'
import color from 'util/color'
import legend from 'chart/renderer/legend'

var defaults = {
  barHeight: 14,
  name: _.partial(_.get, _, 'name', ''),
  offset: 'zero',
  padding: 0.1,
  values: _.property('values'),
  x: _.property('value'),
  xFormat: String,
  xScale: d3.scale.linear,
  y: _.property('location.name'),
  yFormat: String,

  margin: {
    top: 0,
    right: 0,
    bottom: 18,
    left: 80
  }
}

function BarChart () {}

_.extend(BarChart.prototype, ColumnChart.prototype, {
  classNames: 'chart stacked-bar',
  defaults: defaults,

  update: function (data, options) {
    options = _.assign(this._options, options)
    var margin = options.margin

    var l = _(data).map(options.values).map('length').max()
    var h = Math.max(options.barHeight,
      l * options.barHeight + (l - 1) * options.barHeight * options.padding)
    var w = this._width - margin.left - margin.right

    var sortIdx = 0
    var sortBy = this.sortBy

    if (sortBy) {
      sortIdx = _.findIndex(data, function (d) {
        return d.name === sortBy
      })
    }

    let topLegendHeight = 0
    let legendPaddingTop = 0
    if(data && data.length && data.length > 1){
      legendPaddingTop = 18
      topLegendHeight = legendPaddingTop + data.length * 13.8
    }

    // d3.layout.stack stacks the y-value, but we want to stack the x value,
    // so we swap x and y in the layout definition.
    var stack = d3.layout.stack()
      .values(options.values)
      .offset(options.offset)
      .order(function (values) {
        var order = d3.range(values.length)

        if (sortIdx > 0) {
          order.splice(sortIdx, 1)
          order.unshift(sortIdx)
        }

        return order
      })
      .x(options.y)
      .y(options.x)
      .out(function (d, y0, y) {
        d.x0 = y0
        d.x = y
      })

    var stacked = stack(_.cloneDeep(data))

    var range
    if (_.isFunction(options.range)) {
      range = options.range(stacked)
    } else {
      range = d3.extent(_(stacked).map(options.values).flatten().value(), function (d) {
        return d.x0 + d.x
      })

      // Make sure we always have at least a 0 baseline
      range[0] = Math.min(0, range[0])
    }

    var xScale = options.xScale()
      .domain(range)
      .range([0, w])

    var x = function (d) {
      return xScale(d.x0)
    }

    var width = function (d) {
      var x0 = d.x0
      var x = d.x

      return xScale(x0 + x) - xScale(x0)
    }

    var order = _(options.values(stacked[sortIdx]))
      .sortBy(_.property('x'))
      .map(options.y)
      .value()

    var domain = _(stacked)
      .map(options.values)
      .flatten()
      .map(options.y)
      .sortBy(function (n) {
        return order.indexOf(n)
      })
      .value()

    var yScale = d3.scale.ordinal()
      .domain(domain)
      .rangeBands([h, 0], options.padding)

    var y = _.flow(options.y, yScale)

    var colorScale = color.scale(_.map(stacked, options.name))
    var fill = _.flow(options.name, colorScale)

    var svg = this._svg

    var canvasH = h + margin.top + margin.bottom + topLegendHeight
    var canvasW = w + margin.left + margin.right

    svg.attr('viewBox', '0 0 ' + canvasW + ' ' + canvasH)

    if (browser.isIE()) {
      svg.attr({
        'width': canvasW,
        'height': canvasH
      })
    }

    svg.select('.bg')
      .attr({
        'height': h + topLegendHeight,
        'width': w,
        'x': margin.left,
        'y': margin.top
      })

    var g = svg.select('.data').datum(data)
    var series = g.selectAll('.bar').data(stacked)

    series.enter().append('g')
      .attr('class', 'bar')

    series.style('fill', fill)

    series.exit()
      .transition()
      .duration(500)
      .style('opacity', 0)
      .remove()

    var hover = d3.dispatch('over', 'out')

    var bar = series.selectAll('rect').data(options.values)

    bar.enter()
      .append('rect')
      .style('fill', 'inherit')

    bar
      .on('mousemove', hover.over)
      .on('mouseout', hover.out)
      .transition().duration(500)
      .attr({
        'height': yScale.rangeBand(),
        'width': width,
        'x': x
      })
      .transition().duration(500)
      .attr('y', y)

    bar.exit().remove()

    var t0 = svg.transition().duration(500)

    t0.select('.x.axis')
      .attr('transform', 'translate(0, ' + h + ')')
      .call(d3.svg.axis()
        .orient('bottom')
        .ticks(4)
        .outerTickSize(0)
        .tickSize(-h)
        .tickPadding(4)
        .tickFormat(options.xFormat)
        .scale(xScale))

    t0.transition().duration(500)
      .select('.y.axis')
        .call(d3.svg.axis()
          .orient('left')
          .tickFormat(options.yFormat)
          .ticks(3)
          .scale(yScale))

    if (data.length > 1) {
      // Show the legend if we have at least two series
      svg.select('.legend')
        .attr('transform', 'translate(0,' + (h + legendPaddingTop) + ')')
        .call(legend()
          .interactive(true)
          .scale(colorScale)
          .filled(function (d, i) {
            return sortBy ? sortBy === d : i === 0
          })
          .clickHandler(this.setSort.bind(this)))

      g.selectAll('.label').remove()
    } else {
      // Clear the legend if we have fewer than two series
      svg.select('.legend')
        .selectAll('g')
        .remove()

      var label = series.selectAll('.label').data(options.values)
      label.enter()
        .append('text')
        .attr({
          'class': 'label',
          'dx': '2',
          'dy': '.3em'
        })

      label.attr('transform', d => 'translate(0, ' + (y(d) + yScale.rangeBand() / 2) + ')')
        .text(d => options.xFormat(options.x(d)))

      label.exit().remove()
    }

    hover.on('out', function (d, i) {
      if (this.layer) {
        this.layer.destroy()
        this.layer = null
      }
    })

    hover.on('over', function (d, i) {
      if (data.length < 2) {
        return
      }

      var evt = d3.event
      var series = d3.select(this.parentNode).datum()

      var render = function () {
        return (
          <Tooltip left={evt.pageX} top={evt.pageY}>
          <div>
            <h3>{options.name(series)}</h3>
            {options.y(d)}:&ensp;{options.x(d)}
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
  },

  setSort: function (d) {
    this.sortBy = d
    this.update(this._svg.select('.data').datum())
  }
})

export default BarChart
