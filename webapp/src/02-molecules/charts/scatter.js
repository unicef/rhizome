import _ from 'lodash'
import d3 from 'd3'

import React from 'react'
import Layer from 'react-layer'
import Tooltip from 'component/Tooltip.jsx'
import axisLabel from '02-molecules/charts/renderer/axis-label'

var defaults = {
  hoverRadius: 5,
  radius: 3,
  x: _.property('x'),
  xFormat: d3.format('n'),
  xScale: d3.scale.linear,
  y: _.property('y'),
  yFormat: d3.format('n'),
  yScale: d3.scale.linear,

  margin: {
    top: 0,
    right: 0,
    bottom: 24,
    left: 24
  }
}

function ScatterPlot () {}

_.extend(ScatterPlot.prototype, {
  defaults: defaults,

  update: function (data, options) {
    var self = this

    options = _.assign(this._options, options)
    var margin = options.margin

    var svg = this._svg
    var w = this._width - margin.left - margin.right
    var h = this._height - margin.top - margin.bottom

    var domain = _.isFunction(options.domain)
      ? options.domain(data)
      : d3.extent(_.map(data, options.x))

    var xScale = options.xScale()
      .domain(domain)
      .range([0, w])
      .nice()

    var x = function (d) { return xScale(options.x(d)) }

    var range = _.isFunction(options.range)
      ? options.range(data)
      : d3.extent(_.map(data, options.y))

    var yScale = options.yScale()
      .domain(range)
      .range([h, 0])
      .nice()

    var y = function (d) { return yScale(options.y(d)) }

    var point = svg.select('.data').selectAll('.point').data(data, function (d, i) {
      return d.hasOwnProperty('id') ? d.id : i
    })

    var attrs = {
      'cx': x,
      'cy': y,
      'r': options.radius
    }

    point.enter()
      .append('circle')
      .attr('class', 'point')
      .attr(attrs)

    point
      .style('cursor', _.isFunction(options.onClick) ? 'pointer' : 'default')
      .on('click', function (d, i) {
        _.get(options, 'onClick', _.noop)(d, i, this)
      })
      .on('mouseover', function (d, i) {
        d3.select(this)
          .transition()
          .duration(500)
          .ease('elastic')
          .attr('r', options.hoverRadius)

        self._onMouseMove(d, i)
      })
      .on('mouseout', function (d, i) {
        d3.select(this)
          .transition()
          .duration(500)
          .ease('elastic')
          .attr('r', options.radius)

        self._onMouseOut(d, i, this)
      })

    point.transition()
      .duration(300)
      .style('fill', '#525b5e')
      .attr(attrs)

    point.exit()
      .transition()
      .duration(300)
      .attr('r', 0)
      .remove()

    var xAxis = d3.svg.axis()
      .scale(xScale)
      .tickFormat(options.xFormat)
      .tickSize(-h)
      .tickPadding(5)
      .ticks(5)
      .orient('bottom')

    svg.select('.x.axis')
      .transition()
      .duration(300)
      .call(xAxis)

    var yAxis = d3.svg.axis()
      .scale(yScale)
      .tickFormat(options.yFormat)
      .tickSize(-w)
      .ticks(5)
      .orient('left')

    svg.select('.y.axis')
      .transition()
      .duration(300)
      .call(yAxis)

    if (options.xLabel || options.yLabel) {
      svg.call(axisLabel()
      .data(options.xLabel, options.yLabel)
      .width(w)
      .height(h)
      .margin(options.margin))
    }
  },

  _onMouseMove: function (d) {
    var evt = d3.event
    var name = _.get(d, 'name', _.get(d, 'location.name'))

    if (_.isUndefined(name)) {
      return
    }

    var render = function () {
      return React.createElement(
      Tooltip,
      { left: evt.pageX + 2, top: evt.pageY + 2 },
      name
      )
    }

    if (this.layer) {
      this.layer._render = render
    } else {
      this.layer = new Layer(document.body, render)
    }

    this.layer.render()
  },

  _onMouseOut: function () {
    if (this.layer) {
      this.layer.destroy()
      this.layer = null
    }
  }
})

export default ScatterPlot
