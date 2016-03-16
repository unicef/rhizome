import _ from 'lodash'
import d3 from 'd3'
import React from 'react'
import Layer from 'react-layer'

import Tooltip from 'components/molecules/Tooltip.jsx'

import browser from 'components/molecules/charts_d3/utils/browser'
import palettes from 'components/molecules/charts_d3/utils/palettes'

import legend from 'components/molecules/charts_d3/renderer/legend'

var DEFAULTS = {
  aspect: 1,
  domain: _.noop,
  margin: {
    top: 0,
    right: 0,
    bottom: 20,
    left: 0
  },
  data_format: 'pct',
  onClick: _.noop,
  value: _.property('properties.value'),
  color: palettes.orange,
  xFormat: d => d3.format(Math.abs(d) < 1 ? '.4f' : 'n')(d),
  name: _.property('properties.name'),
  maxBubbleValue: 5000,
  maxBubbleRadius: 25,
  bubbleLegendRatio: [0.1, 0.5, 1],
  indicatorName: 'Has data'
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
        tspan = text.append('tspan').attr('x', x).attr('y', y).attr('dy', (lineNumber * lineHeight) + 'rem').text(word)
        lineNumber += 1
      }
    }
  })
}

function _calculateBounds (features) {
  var lat = _.property(1)
  var lng = _.property(0)

  if (features.length < 1) {
    return [[0, 0], [0, 0]]
  }

  var coordinates = _(features).map(function (f) {
    if (f.geometry.type !== 'MultiPolygon') {
      return _.flatten(f.geometry.coordinates)
    }
  })
    .flatten()
    .value()

  var left = d3.min(coordinates, lng)
  var right = d3.max(coordinates, lng)
  var bottom = d3.min(coordinates, lat)
  var top = d3.max(coordinates, lat)

  return [[left, top], [right, bottom]]
}

function _calculateCenter (bounds) {
  var lat = bounds[1][1] + ((bounds[0][1] - bounds[1][1]) / 2)
  var lng = bounds[0][0] + ((bounds[1][0] - bounds[0][0]) / 2)

  return [lng, lat]
}

function _valueForLocation (data, options, locationObject) {
  let locationIndex = (_.select(data, function (d) {
    return d.location_id === locationObject.location_id
  }))[0]

  return options.value(locationIndex)
}

function _chooseRadius (v, radius) {
  if (v > radius.domain()[1]) {
    return radius.range()[1]
  } else {
    return radius(v)
  }
}

function ChoroplethMap () {
}

_.extend(ChoroplethMap.prototype, {
  defaults: DEFAULTS,

  initialize: function (el, data, options) {
    options = this._options = _.defaults({}, options, DEFAULTS)

    var margin = options.margin

    var aspect = _.get(options, 'aspect', 1)
    this._width = _.get(options, 'width', el.clientWidth)
    this._height = _.get(options, 'height', this._width * aspect)

    var svg = this._svg = d3.select(el).append('svg')
      .attr({
        'class': 'reds',
        'viewBox': '0 0 ' + this._width + ' ' + this._height
      })

    if (browser.isIE() || browser.isWkhtmlToPdf()) {
      svg.attr({
        'width': this._width,
        'height': this._height
      })
    }

    var g = svg.append('g')
      .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')')

    g.append('g').attr('class', 'data')
    g.append('g').attr('class', 'legend')
    svg.append('g').attr('class', 'bubbles')
    svg.select('.bubbles').append('g').attr('class', 'data')
    svg.select('.bubbles').append('g').attr('class', 'legend')

    svg.append('g').attr('class', 'stripes')
    svg.select('.stripes').append('g').attr('class', 'data')
    svg.select('.stripes').append('g').attr('class', 'legend')

    var lineWidth = 10
    var lineHeight = 10
    var lineInterval = 5

    var defs = svg.append('defs')

    var pattern = defs.append('pattern')
      .attr({
        'id': 'stripe',
        'patternUnits': 'userSpaceOnUse',
        'width': lineWidth,
        'height': lineHeight
      })

    pattern.append('line')
      .attr({
        'x1': 0,
        'y1': 0,
        'x2': -lineInterval,
        'y2': lineHeight
      })

    pattern.append('line')
      .attr({
        'x1': lineInterval,
        'y1': 0,
        'x2': 0,
        'y2': lineHeight
      })

    pattern.append('line')
      .attr({
        'x1': 2 * lineInterval,
        'y1': 0,
        'x2': lineInterval,
        'y2': lineHeight
      })

    pattern.selectAll('line')
      .attr({
        'stroke-linecap': 'square',
        'stroke-linejoin': 'miter',
        'stroke-width': 1
      })

    this.update(data)
  },
  getColor(indicatorValue, location){
    const bad_bound = this._options.domain()[0]
    const good_bound = this._options.domain()[1]
    const reverseBounds = bad_bound > good_bound
    const colors = this._options.color
    let mapFillColor = ''
    if (this._options.data_format === 'bool'){
      if (indicatorValue === 0){
        mapFillColor = colors[0]
      } else {
        mapFillColor = colors[1]
      }
    } else {
      if (indicatorValue > good_bound && indicatorValue < bad_bound){
        mapFillColor = colors[1]
      } else if (indicatorValue <= good_bound) {
        mapFillColor = reverseBounds ? colors[2] : colors[0]
      } else if (indicatorValue >= bad_bound){
        mapFillColor = reverseBounds ? colors[0] : colors[2]
      }
    }
    return mapFillColor
  },
  update: function (data, options) {
    options = _.assign(this._options, options)
    var margin = options.margin
    var w = this._width - margin.left - margin.right
    var h = this._height - margin.top - margin.bottom

    var svg = this._svg
    var g = svg.select('.data')

    var features = _.reject(data, 'properties.isBorder')

    var bounds = _calculateBounds(features)
    var center = _calculateCenter(bounds)

    var projection = d3.geo.conicEqualArea()
      .parallels([bounds[1][1], bounds[0][1]])
      .rotate([-center[0], 0])   // Rotate the globe so that the country is centered horizontally
      .center([0, center[1]])    // Set the center of the projection so that the polygon is moved vertically into the center of the viewport
      .translate([w / 2, h / 2]) // Translate to the center of the viewport
      .scale(1)

    var b = [projection(bounds[0]), projection(bounds[1])]
    var s = 1 / Math.max((b[1][0] - b[0][0]) / w, (b[1][1] - b[0][1]) / h)

    projection.scale(s)

    var path = d3.geo.path().projection(projection)
    //removed features from parameters into domain()
    var domain = options.domain()
    // calculate the bounds upon which to color the map based on the
    // scale of the cooresponding data.

    if (!_.isArray(domain)) {
      domain = d3.extent(features, options.value)
      domain[0] = Math.min(domain[0], 0)
    }
    var colorScale = d3.scale.threshold()
      .domain(domain.concat().reverse())
      .range(options.color.concat().reverse())
//<<<<<<< HEAD:webapp/src/02-molecules/charts/choropleth.js
    // table.js --> THIS SETS THE COLOR... MOVE FROM HERE ONCE THE USER CAN SET A PALLETTE
    // var targets = _(options.headers)
    //   .indexBy('id')
    //   .mapValues(ind => {
    //     var extents = [ ind.low_bound, ind.high_bound ]
    //     var names = ['bad', 'ok', 'good']

    //     if (ind.low_bound > ind.high_bound) {
    //       names = ['good', 'ok', 'bad']
    //     }

    //     return d3.scale.threshold()
    //       .domain(extents)
    //       .range(names)
    //   })
    //   .value()
// =======
// >>>>>>> d41e7ed9ff5b20d3e11f4a31198b070068ddba67:webapp/src/components/molecules/charts_d3/choropleth_map/ChoroplethMap.js
    var location = g.selectAll('.location')
      .data(features, function (d, i) {
        return _.get(d, 'properties.location_id', i)
      })

    location.enter().append('path')

    location.attr({
      'd': path,
      'class': function (d) {
        var v = options.value(d)
        var classNames = ['location']

        if (_.isFinite(v)) {
          classNames.push('clickable')
        }
        return classNames.join(' ')
      }
    })
      .style('fill', d => {
        var v = options.value(d)
        return _.isFinite(v) ? this.getColor(v,d) : '#fff'
      })
      .on('click', _.partial(this._onClick, _, options, data))
      .on('mousemove', _.partial(this._onMouseMove, _, options, data))
      .on('mouseout', this._onMouseOut)

    location.exit().remove()

    var ticks = _.map(
      colorScale.range(),
        c => _.map(colorScale, options.xFormat).join('—')
    )
    if (!options.homepage && options.chartInDashboard) {
      if (_.every(colorScale.domain(), _.isNaN)) {
        svg.select('.legend').selectAll('*').remove()
      } else {
        svg.select('.legend')
          .call(legend(options).scale(
            d3.scale.ordinal().domain(ticks).range(colorScale.range())
          )
        ).attr('transform', 'translate(2, 0)')

        let dataYPosition = options.chartInDashboard ? (ticks && ticks.length ? Math.ceil(ticks.length / 2) : 0) : 0
        g.attr('transform', 'translate(0, ' + dataYPosition * 12 + ')')
      }
    }

    var legendGap = 0.03 * w
    var fontLength = 100
    var stripeLegendStartPosition

    if (options.stripeValue) {
      var stripes = svg.select('.stripes').select('.data')
      var stripeData = stripes.selectAll('.location')
        .data(features, function (d, i) {
          return _.get(d, 'properties.location_id', i)
        })

      stripeData.enter().append('path')

      stripeData.attr({
        'd': path,
        'class': d => {
          var v = options.value(d)
          var classNames = ['location']

          if (_.isFinite(v)) {
            classNames.push('clickable')
          }

          return classNames.join(' ')
        }
      })
        .style('fill', d => {
          var v = options.stripeValue(d)
          var lineColor = _.isFinite(options.value(d)) ? '#ffffff' : '#cccccc'
          svg.selectAll('line').style('stroke', lineColor)
          return (_.isFinite(v) && v > 0) ? 'url(#stripe)' : '#fff'
        })
        .style('opacity', d => {
          var v = options.stripeValue(d)
          return _.isFinite(v) && v > 0 ? 1 : 0
        })
        .on('click', d => { this._onClick(d, options) })
        .on('mousemove', _.partial(this._onMouseMove, _, options, data))
        .on('mouseout', this._onMouseOut)

      stripeData.exit().remove()

      let dataYPosition = options.chartInDashboard ? (ticks && ticks.length ? Math.ceil(ticks.length / 2) : 0) : 0
      stripes.attr('transform', 'translate(0' + ', ' + dataYPosition * 12 + ')')

      if (options.chartInDashboard) {
        var stripeLegendLength = 140
        stripeLegendStartPosition = fontLength + legendGap
        var stripeLegendGap = 14
        var stripeLegendColor = d3.scale.ordinal().range(['#FFFFFF', 'url(#stripe)'])
        var stripeLegendText = ['No data', options.indicatorName]
        var stripeLegend = svg.select('.stripes').select('.legend')
          .attr('transform', 'translate(' + stripeLegendStartPosition + ', ' + 0 + ')')
          .selectAll('.series').data(stripeLegendText)
          .enter().append('g')
          .attr('class', 'series')
          .attr('transform', function (d, i) {
            return 'translate(' + 0 + ', ' + i * stripeLegendGap + ')'
          })

        stripeLegend.append('rect')
          .attr('width', 11)
          .attr('height', 11)
          .style({
            'fill': stripeLegendColor,
            'stroke': '#cccccc',
            'stroke-width': 1
          })

        stripeLegend.append('text')
          .attr({
            'x': 16,
            'y': 3.5,
            'dy': 6
          })
          .style({
            'text-anchor': 'start',
            'font-size': 10
          })
          .text(d => { return d })
          .call(wrap, stripeLegendLength, 16)
      }
    }

    if (options.bubbleValue) {
      if (options.maxBubbleValue === 0) {
        options.maxBubbleValue = 5000
      }

      var radius = d3.scale.sqrt()
        .domain([0, options.maxBubbleValue])
        .range([0, options.maxBubbleRadius])

      var bubbles = svg.selectAll('.bubbles').select('.data')
      var bubbleData = bubbles.selectAll('circle')
        .data(features, function (d, i) {
          return _.get(d, 'properties.location_id', i)
        })

      bubbleData.enter().append('circle')
      bubbleData.attr('transform', function (d) {
        return 'translate(' + path.centroid(d) + ')'
      })
        .attr('r', function (d) {
          var v = options.bubbleValue(d)
          return v ? _chooseRadius(v, radius) : 0
        })
        .style({
          'opacity': 0.5,
          'fill': '#D5EBF7',
          'stroke': '#FFFFFF'
        })

      bubbleData.exit().remove()

      let dataYPosition = options.chartInDashboard ? (ticks && ticks.length ? Math.ceil(ticks.length / 2) : 0) : 0
      bubbles.attr('transform', 'translate(0' + ', ' + dataYPosition * 12 + ')')

      if (options.chartInDashboard) {
        var bubbleLegendText = _.map(options.bubbleLegendRatio, d => {
          return Math.ceil(d * options.maxBubbleValue, -1)
        })

        var bubbleLegendLineLength = w > 400 ? 60 : 0.15 * w

        var bubbleLegendStartPosition = options.stripeValue
          ? stripeLegendStartPosition + stripeLegendLength + legendGap + bubbleLegendLineLength
          : fontLength + legendGap + bubbleLegendLineLength

        var bubbleLegend = svg.select('.bubbles').select('.legend')
          .attr('transform', 'translate(' + bubbleLegendStartPosition + ', ' + (options.maxBubbleRadius + 10) + ')')
          .selectAll('.series').data(bubbleLegendText)
          .enter().append('g')
          .attr('class', 'series')

        bubbleLegend.append('circle')
          .attr('r', d => {
            return radius(d)
          })
          .attr('cy', d => {
            return (options.maxBubbleRadius - radius(d))
          })
          .style({
            'opacity': 0.5,
            'fill': 'transparent',
            'stroke': '#AAAAAA'
          })

        bubbleLegend.append('line')
          .attr({
            x1: -bubbleLegendLineLength,
            y1: d => {
              return (options.maxBubbleRadius - 2 * radius(d))
            },
            x2: 0,
            y2: d => {
              return (options.maxBubbleRadius - 2 * radius(d))
            }
          })
          .style('stroke', '#AAAAAA')

        bubbleLegend.append('text')
          .attr('dx', -bubbleLegendLineLength)
          .attr('dy', d => {
            return (options.maxBubbleRadius - 2 * radius(d))
          })
          .text(d => {
            return d
          })
          .style('fill', '#AAAAAA')
      }
    }
  },

  _onMouseMove: function (d, options, data) {
    const evt = d3.event
    let locationValue = options.xFormat(_valueForLocation(data, options, d) || 0)
    if (options.data_format === 'bool') {
      locationValue = locationValue !== '0' ? 'Yes' : 'No'
    }
    const displayValue = options.name(d) + ': ' + locationValue
    const render = () => <Tooltip left={evt.pageX + 2} top={ evt.pageY + 2}>{displayValue}</Tooltip>
    this.layer ? this.layer._render = render : this.layer = new Layer(document.body, render)
    this.layer.render()
  },

  _onMouseOut: function () {
    if (this.layer) {
      this.layer.destroy()
      this.layer = null
    }
  },

  _onClick: function (d, options, data) {
    if (this.layer) {
      this.layer.destroy()
      this.layer = null
    }
    options.onClick(_.get(d, 'properties.location_id'))
  }
})

export default ChoroplethMap
