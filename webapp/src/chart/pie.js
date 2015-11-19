'use strict'

import _ from 'lodash'
import d3 from 'd3'

import colors from 'util/color'

import React from 'react'
import Layer from 'react-layer'
import Tooltip from 'component/Tooltip.jsx'

function _domain (data, options) {
  return [0, _(data).map(options.value).sum()]
}

var DEFAULTS = {
  domain: _domain,
  innerRadius: 0,
  outerRadius: 1,
  margin: {
    top: 0,
    right: 0,
    bottom: 0,
    left: 0
  },
  value: _.property('value'),
  name: _.property('indicator.short_name'),
  format: function (d) {
    return d3.format((Math.abs(d) < 1) ? '.4f' : 'n')(d)
  }
}

function PieChart () {
}

_.extend(PieChart.prototype, {
  defaults: DEFAULTS,

  initialize: function (el, data, options) {
    var opts = this._options = _.defaults({}, options, DEFAULTS)

    this._height = this._width = _.get(opts, 'size', el.clientWidth)

    var svg = this._svg = d3.select(el).append('svg').attr('class', 'pie')

    var g = svg.append('g').attr('class', 'margin')

    g
      .append('g').attr('class', 'data')
      .append('path').attr('class', 'bg')

    this.update(data)
  },

  update: function (values, options) {
    options = _.assign(this._options, options)
    var margin = options.margin

    values = _(values)
      .filter(d => {
        var v = options.value(d)
        return _.isFinite(v) && v > 0
      })
      .sortBy(options.value)
      .reverse()
      .value()

    var data = [{value: 0}, {value: 0}]
    if (values[0] && values[0].value) {
      data[0].value = Math.round(values[0].value * 100) / 100
      data[1].value = 1 - data[0].value
    }

    var w = this._width - margin.left - margin.right
    var h = this._height - margin.top - margin.bottom
    var s = Math.min(w, h)

    var svg = this._svg

    svg.attr({
      'viewBox': '0 0 ' + this._width + ' ' + this._height
    })
      .select('.margin')
      .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')')


    if (this._options.pieType) {
      var g = svg.select('.data')
      .attr('transform', 'translate(' + 50 + ', ' + 50 + ')')
    } else {
      var g = svg.select('.data')
      .attr('transform', 'translate(' + (w / 2) + ', ' + (h / 2) + ')')
    }


    var arc = d3.svg.arc()
      .innerRadius(s / 2 * options.innerRadius)
      .outerRadius(s / 2 * options.outerRadius)

    svg.select('.bg')
      .datum({
        startAngle: 0,
        endAngle: 2 * Math.PI
      })
      .attr('d', arc)

    var scale = d3.scale.linear()
      .domain(options.domain(data, options))
      .range([0, 2 * Math.PI])

    var pie = d3.layout.stack()
      .values(function (d) {
        return [d]
      })
      .x(options.name)
      .y(options.value)
      .out(function (d, y0, y) {
        d.startAngle = scale(y0)
        d.endAngle = scale(y0 + y)
      })

    var colorScale = colors.scale(_.map(data, options.value), options.palette)
    var fill = _.flow(options.value, colorScale)

    var slice = g.selectAll('.slice').data(pie(_.cloneDeep(data)))

    slice.enter()
      .append('path')
      .attr('class', 'slice')

    slice.attr({
      'd': arc,
      'fill': fill
    }).on('mousemove', d => {
      var evt = d3.event

      var render = function () {
        return (
          <Tooltip left={evt.pageX} top={evt.pageY}>
            <div>
              <p>{d3.format('%')(options.value(d))}</p>
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

    slice.exit().remove()
  }
})

export default PieChart
