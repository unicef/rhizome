'use strict'

var _ = require('lodash')
var d3 = require('d3')

var browser = require('util/browser')
var label = require('chart/renderer/label')
var color = require('util/color')
var legend = require('chart/renderer/legend')

var defaults = {
  margin: {
    top: 12,
    right: 0,
    bottom: 12,
    left: 0
  },
  name: _.partial(_.get, _, 'name', ''),
  padding: 0.1,
  values: _.property('values'),
  x: _.property('x'),
  xFormat: String,
  y: _.property('y'),
  y0: _.partial(_.get, _, 'y0', 0),
  yFormat: String,
  yScale: d3.scale.linear
}

function ColumnChart () {
}

_.extend(ColumnChart.prototype, {
  classNames: 'chart stacked-column',
  defaults: defaults,

  initialize: function (el, data, options) {
    options = this._options = _.defaults({}, options, this.defaults)

    var aspect = _.get(options, 'aspect', 1)
    this._width = _.get(options, 'width', el.clientWidth)
    this._height = _.get(options, 'height', this._width / aspect)

    var svg = this._svg = d3.select(el).append('svg')
      .attr({
        'viewBox': '0 0 ' + this._width + ' ' + this._height,
        'class': this.classNames
      })

    if (browser.isIE()) {
      svg.attr({
        'width': this._width,
        'height': this._height
      })
    }

    var h = this._height - options.margin.top - options.margin.bottom

    svg.append('rect').attr({
      'class': 'bg',
      'height': h + options.margin.top,
      'width': this._width - options.margin.left - options.margin.right,
      'x': options.margin.left
    })

    var g = svg.append('g')
      .attr('transform', 'translate(' + options.margin.left + ', ' +
      options.margin.top + ')')

    g.append('g').attr('class', 'data')

    g.append('g').attr('class', 'y axis')
    g.append('g').attr({
      'class': 'x axis',
      'transform': 'translate(0, ' + h + ')'
    })
    g.append('g').attr('class', 'legend')
    g.append('g').attr('class', 'annotation')

    this.update(data, options)
  },

  update: function (data, options) {
    var options = _.assign(this._options, options)
    var margin = options.margin

    var h = this._height - margin.top - margin.bottom
    var w = this._width - margin.left - margin.right
    var dataMarginLeft = 20

    var domain

    if (_.isFunction(options.domain)) {
      domain = options.domain(data)
    } else {
      domain = _(data).map(options.values).flatten().map(options.x).value()
    }

    var xScale = d3.scale.ordinal()
      .domain(domain)
      .rangeBands([0, w], options.padding)

    var dataXScale = d3.scale.ordinal()
      .domain(domain)
      .rangeBands([dataMarginLeft, w], options.padding)

    var x = _.flow(options.x, dataXScale)

    var range
    if (_.isFunction(options.range)) {
      range = options.range(data)
    } else {
      range = d3.extent(_(data).map(options.values).flatten().value(), function (d) {
        return options.y0(d) + options.y(d)
      })

      // Make sure we always have at least a 0 baseline
      range[0] = Math.min(0, range[0])
    }

    var yScale = options.yScale()
      .domain(range)
      .range([h, 0])

    var y = function (d) {
      return yScale(options.y0(d) + options.y(d))
    }

    var height = function (d) {
      var y0 = options.y0(d)
      var y = options.y(d)

      return yScale(y0) - yScale(y0 + y)
    }

    var svg = this._svg
    var g = svg.select('.data')
    var series = g.selectAll('.bar').data(data)

    svg.select('.bg')
      .attr({
        'height': h + margin.top,
        'width': w,
        'x': margin.left
      })

    series.enter().append('g')
      .attr('class', 'bar')

    var fill = options.hasOwnProperty('color')
      ? options.color
      : _.flow(options.name, color.scale(_.map(data, options.name)))

    series.style('fill', fill)
    series.exit().remove()

    var hover = d3.dispatch('over', 'out')

    var column = series.selectAll('rect').data(options.values)

    column.enter()
      .append('rect')
      .style('fill', 'inherit')

    column.attr({
      'height': height,
      'width': xScale.rangeBand(),
      'x': x,
      'y': y
    })
      .on('mouseover', hover.over)
      .on('mouseout', hover.out)

    column.exit().remove()

    svg.select('.x.axis')
      .call(d3.svg.axis()
        .orient('bottom')
        .tickSize(0)
        .tickPadding(4)
        .tickValues(_.filter(xScale.domain(), function (d, i, domain) {
          // Include every fourth tick value unless that tick is within three
          // ticks of the last value. Always include the last tick. We have to
          // do this manually because D3 ignores the ticks() value for
          // ordinal scales
          return (i % 4 === 0 && i + 3 < domain.length) || (i + 1) === domain.length
        }))
        .tickFormat(options.xFormat)
        .scale(dataXScale))

    svg.select('.y.axis')
      .call(d3.svg.axis()
        .orient('right')
        .tickFormat(options.yFormat)
        .tickSize(w)
        .ticks(3)
        .scale(yScale))

    svg.selectAll('.y.axis text')
      .attr({
        'dx': -w,
        'dy': -4
      })

       var fmt = _.flow(options.y, options.yFormat)
    var labels = _(data)
      .map(function (s) {
        return _.assign({},
          _.max(options.values(s), options.x),
          { name: options.name(s) }
        )
      })
      .map(function (d) {
        return {
          text: d.name + ' ' + fmt(d),
          x: x(d),
          y: y(d),
          defined: _.isFinite(d.value)
        }
      })
      .reverse()
      .value()

    var seriesLabel = label()
      .addClass('series')
      .width(w)
      .height(h)
      .align(false)

    var legendText = _(data)
      .map(function (d) {
        return options.name(d)
      })
      .value()

    var fillColor = d3.scale.ordinal().range(['#B6D0D4', '#D95449'])
    var legend = svg.select('.legend').selectAll('*')
      .data(legendText)
      .enter().append('g')
      .attr('class', 'series')
      .attr('transform', function (d, i) { return 'translate(0,' + i * 15 + ')' })

    legend.append('rect')
      .attr('x', w - 15)
      .attr('y', -25)
      .attr('width', 10)
      .attr('height', 10)
      .style('fill', fillColor)

    legend.append('text')
      .attr('x', w - 20)
      .attr('y', -25)
      .attr('dy', '0.85em')
      .style({
        'text-anchor': 'end',
        'fill': '#999999'
        })
      .text(function (d) { return d })

    var timeout = null

    hover.on('out', function () {
      timeout = window.setTimeout(function () {
        timeout = null

        g.selectAll('rect')
          .transition()
          .duration(300)
          .style('opacity', 1)

        svg.selectAll('.x.axis text').style('opacity', 1)

        svg.select('.annotation').selectAll('*').remove()
      }, 200)
    })

    hover.on('over', function (d) {
      if (_.isNumber(timeout)) {
        window.clearTimeout(timeout)
        timeout = null
      }

      g.selectAll('rect')
        .transition()
        .duration(500)
        .style('opacity', function (e) {
          return options.x(d) === options.x(e) ? 1 : 0.5
        })

      svg.selectAll('.x.axis text').style('opacity', 0)
      var annotations = _(data)
        .map(function (s) {
          return _.assign({},
            _.find(options.values(s), function (e) {
              return options.x(d) === options.x(e)
            }),
            { name: options.name(s) }
          )
        })
        .map(function (d) {
          return {
            text: d.name + ' ' + fmt(d),
            x: x(d),
            y: y(d),
            defined: _.isFinite(d.value)
          }
        })
        .tap(list => {
          if (_(list).some(item => (item.y >= h || item.y < 0))) {
            list.forEach(item => {
              item.y = 0
            })
          }
        })
        .each(item => { item.y = 0 })
        .reverse()
        .value()

      svg.select('.annotation').selectAll('.series.label')
        .data(annotations)
        .call(seriesLabel.align(true))

      var axisLabel = svg.select('.annotation')
        .selectAll('.axis.label')
        .data([options.x(d)])

      axisLabel.enter()
        .append('text')
        .attr('class', 'axis label')
        .style('text-anchor', 'middle')

      axisLabel
        .attr({
          'transform': 'translate(' + x(d) + ', ' + (h + margin.bottom) + ')',
          'dx': xScale.rangeBand() / 2
        })
        .text(options.xFormat)
    })
  }

})

module.exports = ColumnChart
