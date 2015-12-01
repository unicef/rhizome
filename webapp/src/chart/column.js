import _ from 'lodash'
import d3 from 'd3'
import moment from 'moment'

import browser from 'util/browser'
import label from 'chart/renderer/label'
import color from 'util/color'
import palettes from 'util/palettes'

var defaults = {
  margin: {
    top: 30,
    right: 0,
    bottom: 12,
    left: 0
  },
  name: _.partial(_.get, _, 'name', ''),
  padding: 0.1,
  values: _.property('values'),
  color: palettes.blue,
  x: _.property('x'),
  xFormat: String,
  y: _.property('y'),
  y0: _.partial(_.get, _, 'y0', 0),
  yFormat: String,
  yScale: d3.scale.linear,
  widthRatio: 0.15
}

function processData (originalData, options) {
  var percentage = function (dataset) {
    var total = _(dataset).pluck('value').sum()
    _.forEach(dataset, d => { d.value /= total })
    return dataset
  }

  var stack = d3.layout.stack()
    .offset('zero')
    .values(d => { return d.values })
    .x(d => { return d.campaign.start_date })
    .y(d => { return d.value })

  var data = _(originalData)
    .each(d => { d.quarter = moment(d.campaign.start_date).format('[Q]Q YYYY') })
    .groupBy(d => { return d.indicator.id + '-' + d.quarter })
    .map(d => {
      return _.assign({}, d[0], {
        'value': _(d).pluck('value').sum()
      })
    })
    .groupBy('quarter')
    .map(percentage)
    .flatten()
    .reject(d => { return d.indicator.id === options.rejectId })
    .groupBy('indicator.short_name')
    .map((values, name) => {
      return {
        name: name,
        values: values
      }
    })
    .sortBy('name')
    .value()

  return stack(data)
}

function defaultColumnChart (data, options, svg, h, w, topLegendHeight) {
  var margin = options.margin
  var dataMarginLeft = 25

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
    range = d3.extent(_(data).map(options.values).flatten().value(), d => {
      return options.y0(d) + options.y(d)
    })

    // Make sure we always have at least a 0 baseline
    range[0] = Math.min(0, range[0])
  }

  var yScale = options.yScale()
    .domain(range)
    .range([h, 0])

  var y = d => {
    return yScale(options.y0(d) + options.y(d))
  }

  var height = d => {
    var y0 = options.y0(d)
    var y = options.y(d)

    return yScale(y0) - yScale(y0 + y)
  }

  var g = svg.select('.data').attr('transform', 'translate(0,' + topLegendHeight + ')')
  var series = g.selectAll('.bar').data(data)

  svg.select('.bg')
    .attr({
      'height': h + margin.top + topLegendHeight,
      'width': w,
      'x': margin.left
    })

  series.enter().append('g')
    .attr('class', 'bar')

  let fill = color.map(data.map(options.name), options.color)

  series.style({
    'fill': _.flow(options.name, fill),
    'stroke': '#fff'
  })

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
    .attr('transform', 'translate(0,' + (h + topLegendHeight) + ')')
    .call(d3.svg.axis()
      .orient('bottom')
      .tickSize(0)
      .tickPadding(4)
      .tickValues(_.filter(dataXScale.domain(), function (d, i, domain) {
        // Include every fourth tick value unless that tick is within three
        // ticks of the last value. Always include the last tick. We have to
        // do this manually because D3 ignores the ticks() value for
        // ordinal scales
        return (i % 4 === 0 && i + 3 < domain.length) || (i + 1) === domain.length
      }))
      .tickFormat(options.xFormat)
      .scale(dataXScale))

  svg.select('.x.axis').selectAll('text').attr('y', 9)
  svg.select('.x.axis').selectAll('.domain').data([0])
    .attr('d', 'M' + 0 + ',' + 0 + 'V0H' + w + 'V' + 0)

  svg.select('.y.axis')
    .attr('transform', 'translate(0,' + topLegendHeight + ')')
    .call(d3.svg.axis()
      .orient('right')
      .tickFormat(options.yFormat)
      .tickSize(w)
      .ticks(2)
      .scale(yScale))

  svg.selectAll('.y.axis text')
    .attr({
      'dx': -w,
      'dy': 10
    })

  d3.select(svg.selectAll('.y.axis text')[0][0]).attr('visibility', 'hidden')

  var fmt = _.flow(options.y, options.yFormat)

  var seriesLabel = label()
    .addClass('series')
    .width(w)
    .height(h)
    .align(false)

  var legendText = _(data)
    .map(d => {
      return options.name(d)
    })
    .reverse()
    .value()

  var legend = svg.select('.legend').selectAll('*')
    .data(legendText)

  legend.enter().append('g')
    .attr('class', 'series')
    .attr('transform', function (d, i) { return 'translate(0,' + i * 15 + ')' })

  legend.append('rect')
    .attr({
      'x': w - 12,
      'y': -25,
      'width': 12,
      'height': 12
    })
    .style({
      'fill': fill
    })

  legend.append('text')
    .attr({
      'x': w - 12,
      'y': -25,
      'dx': -5,
      'dy': 9
    })
    .style({
      'text-anchor': 'end',
      'fill': '#999999'
    })
    .text(d => { return d })

  legend.exit().remove()

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

  hover.on('over', d => {
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
      .map(d => {
        return {
          text: d.name + ' ' + fmt(d),
          x: x(d),
          y: y(d),
          defined: _.isFinite(d.value)
        }
      })
      .tap(list => {
        if (_(list).some(item => (item.y >= h || item.y < 50))) {
          list.forEach(item => { item.y = 50 })
        }
      })
      .each(item => {
        item.y = 50
      })
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
        'dx': xScale.rangeBand() / 2,
        'dy': '0.45em'
      })
      .text(options.xFormat)
  })
}

function wrap (text, width, x) {
  text.each(function () {
    let text = d3.select(this)
    let words = text.text().split(/\s+/).reverse()
    let word
    let line = []
    let lineNumber = 1
    let lineHeight = 1.1
    let y = text.attr('y')
    let tspan = text.text(null).append('tspan').attr('x', x).attr('y', y)
    while (words.length > 0) {
      word = words.pop()
      line.push(word)
      tspan.text(line.join(' '))
      if (tspan.node().getComputedTextLength() > (width - x)) {
        line.pop()
        tspan.text(line.join(' '))
        line = [word]
        tspan = text.append('tspan').attr('x', x).attr('y', y).attr('dy', (lineNumber * lineHeight) + 'em').text(word)
        lineNumber += 1
      }
    }
  })
}

function roundedRect (xCoordinate, yCoordinate, width, height, radius, topLeft, topRight, bottomLeft, bottomRight) {
  var path
  path = 'M' + (xCoordinate + radius) + ',' + yCoordinate
  path += 'h' + (width - 2 * radius)

  path += topRight
    ? 'a' + radius + ',' + radius + ' 0 0 1 ' + radius + ',' + radius
    : 'h' + radius + 'v' + radius
  path += 'v' + (height - 2 * radius)

  path += bottomRight
    ? 'a' + radius + ',' + radius + ' 0 0 1 ' + -radius + ',' + radius
    : 'v' + radius + 'h' + -radius
  path += 'h' + (2 * radius - width)

  path += bottomLeft
    ? 'a' + radius + ',' + radius + ' 0 0 1 ' + -radius + ',' + -radius
    : 'h' + -radius + 'v' + -radius
  path += 'v' + (2 * radius - height)

  path += topLeft
    ? 'a' + radius + ',' + radius + ' 0 0 1 ' + radius + ',' + -radius
    : 'v' + -radius + 'h' + radius
  path += 'z'
  return path
}

function ColumnChart () {}

_.extend(ColumnChart.prototype, {
  classNames: 'chart stacked-column',
  defaults: defaults,

  initialize: function (el, data, options) {
    options = this._options = _.defaults({}, options, this.defaults)

    var aspect = _.get(options, 'aspect', 1)
    this._width = _.get(options, 'width', el.clientWidth)
    this._height = _.get(options, 'height', this._width / aspect)

    this._topLegendHeight = 0
    if (options && options.chartInDashboard && data && data.length && data.length > 0) {
      this._topLegendHeight = data.length * 10
    }

    var svg = this._svg = d3.select(el).append('svg')
      .attr({
        'viewBox': '0 0 ' + this._width + ' ' + (this._height + this._topLegendHeight),
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

  update: function (originalData, options) {
    var data = options.processData ? processData(originalData, options) : originalData
    options = _.assign(this._options, options)

    var h = this._height - options.margin.top - options.margin.bottom
    var w = this._width - options.margin.left - options.margin.right
    var topLegendHeight = this._topLegendHeight
    var svg = this._svg

    var range
    if (_.isFunction(options.range)) {
      range = options.range(data)
    } else {
      range = d3.extent(_(data).map(options.values).flatten().value(), d => {
        return options.y0(d) + options.y(d)
      })

      range[0] = Math.min(0, range[0])
    }

    var yScale = options.yScale()
      .domain(range)
      .range([h, 0])

    var y = d => {
      return yScale(options.y0(d) + options.y(d))
    }

    var height = d => {
      var y0 = options.y0(d)
      var y = options.y(d)

      return yScale(y0) - yScale(y0 + y)
    }

    if (!options.inaccessibility) {
      defaultColumnChart(data, options, svg, h, w, topLegendHeight)
    } else {
      var g = svg.select('.data').attr('transform', 'translate(0,' + 0 + ')')
      var series = g.selectAll('.bar').data(data)

      var rectWidth = options.widthRatio * w
      var x = options.margin.left

      svg.select('.bg')
        .attr({
          'height': h + options.margin.top,
          'width': w,
          'x': x
        })

      series.enter().append('g')
        .attr('class', 'bar')

      let fill = color.map(data.map(options.name), options.color)

      series.style({
        'fill': _.flow(options.name, fill),
        'stroke': '#fff'
      })

      series.exit().remove()

      var column = series.selectAll('rect').data(options.values)

      column.enter()
        .append('path')
        .attr('d', d => {
          var topRounded = y(d) === 0
          var bottomRounded = (y(d) + height(d)) === h
          return roundedRect(x, y(d), rectWidth, height(d), 5, topRounded, topRounded, bottomRounded, bottomRounded)
        })
        .style('fill', 'inherit')

      column.exit().remove()

      var fmt = _.flow(options.y, options.yFormat)
      let annotationData = _(data)
        .map(function (s) {
          return _.assign({}, ...options.values(s),
            { name: options.name(s) }
          )
        })
        .map(d => {
          return {
            name: d.name,
            text: d.name.slice(2) + ' ' + fmt(d),
            x: rectWidth,
            y: y(d) + (height(d) * 0.2),
            defined: _.isFinite(d.value)
          }
        })
        .value()

      var annotation = svg.select('.annotation').selectAll('*')
        .data(annotationData)

      annotation.enter().append('g')
        .attr('class', 'series')
        .style({
          'fill': _.flow(options.name, fill),
          'stroke': _.flow(options.name, fill)
        })

      var xLine = rectWidth * 1.5
      var xText = rectWidth * 1.7

      annotation.append('text')
        .attr({
          'x': xText,
          'y': d => { return d.y }
        })
        .text(d => { return d.text })
        .call(wrap, w, xText)
        .style({
          'fill': 'inherit',
          'stroke': 'transparent',
          'font-size': 10
        })

      annotation.append('line')
        .attr({
          'x1': rectWidth,
          'x2': xLine,
          'y1': d => { return d.y },
          'y2': d => { return d.y }
        })
        .style('stroke', 'inherit')

      annotation.exit().remove()
    }
  }

})

export default ColumnChart
