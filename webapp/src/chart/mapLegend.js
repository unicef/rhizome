import _ from 'lodash'
import d3 from 'd3'

import browser from 'util/browser'
import palettes from 'util/palettes'

import legend from 'chart/renderer/legend'

var DEFAULTS = {
  aspect: 1,
  domain: _.noop,
  margin: {
    top: 0,
    right: 0,
    bottom: 0,
    left: 0
  },
  color: palettes.orange,
  onClick: _.noop,
  yFormat: d => d3.format(Math.abs(d) < 1 ? '.4f' : 'n')(d),
  name: _.property('properties.name'),
  maxBubbleValue: 5000,
  maxBubbleRadius: 25,
  bubbleLegendRatio: [0.1, 0.5, 1]
}

function MapLegend () {
}

_.extend(MapLegend.prototype, {
  defaults: DEFAULTS,

  initialize: function (el, data, options) {
    options = this._options = _.defaults({}, options, DEFAULTS)

    var margin = options.margin

    var aspect = _.get(options, 'aspect', 1)
    this._width = _.get(options, 'width', el.clientWidth)
    this._height = _.get(options, 'height', this._width * aspect)

    var svg = this._svg = d3.select(el).append('svg')
      .attr('class', 'reds')
      .attr('viewBox', '0 0 ' + this._width + ' ' + this._height)

    if (browser.isIE()) {
      svg.attr({
        'width': this._width,
        'height': this._height
      })
    }

    var g = svg.append('g')
      .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')')

    g.append('g').attr('class', 'legend')
    svg.append('g').attr('class', 'bubbles')
    svg.select('.bubbles').append('g').attr('class', 'legend')

    svg.append('g').attr('class', 'stripes')
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
      .style('stroke', '#cccccc')
      .attr({
        'stroke-linecap': 'square',
        'stroke-linejoin': 'miter',
        'stroke-width': 1
      })

    this.update(data)
  },

  update: function (data, options) {
    options = _.assign(this._options, options)

    var svg = this._svg

    if (options.value) {
      var features = _.reject(data, 'properties.isBorder')

      var domain = options.domain(features)

      if (!_.isArray(domain)) {
        domain = d3.extent(features, options.value)
        domain[0] = Math.min(domain[0], 0)
      }

      var colorScale = d3.scale.quantize()
        .domain(domain.concat().reverse())
        .range(options.color.concat().reverse())

      var ticks = _.map(colorScale.range(), c => _.map(colorScale.invertExtent(c), options.yFormat).join('—'))
      svg.select('.legend')
      .call(legend().scale(d3.scale.ordinal().domain(ticks).range(colorScale.range())))
      .attr('transform', function () { return 'translate(' + 2 + ', ' + 0 + ')' })
    }

    if (options.stripeValue) {
      var stripeLegendColor = d3.scale.ordinal().range(['#FFFFFF', 'url(#stripe)'])
      var stripeLegendText = options.stripeLegendText
      var stripeLegend = svg.select('.stripes').select('.legend')
        .attr('transform', function () {
          return 'translate(' + 2 + ', ' + 0 + ')'
        })
        .selectAll('.series').data(stripeLegendText)
        .enter().append('g')
        .attr('class', 'series')
        .attr('transform', function (d, i) {
          return 'translate(' + 0 + ', ' + i * 15 + ')'
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
        .text(function (d) { return d })
    }

    if (options.bubbleValue) {
      var radius = d3.scale.sqrt()
        .domain([0, options.maxBubbleValue])
        .range([0, options.maxBubbleRadius])

      var bubbleLegendText = _.map(options.bubbleLegendRatio, d => {
        return Math.ceil(d * options.maxBubbleValue, -1)
      })

      var bubbleLegend = svg.select('.bubbles').select('.legend')
        .attr('transform', function () {
          return 'translate(' + 2 + ', ' + 0 + ')'
        })
        .selectAll('.series').data(bubbleLegendText)
        .enter().append('g')
        .attr('class', 'series')

      let cx = 2.5 * options.maxBubbleRadius
      let cy = d => { return 2.5 * options.maxBubbleRadius - radius(d) }
      var lineY = d => { return (cy(d) - radius(d)) }

      bubbleLegend.append('circle')
        .attr('r', d => { return radius(d) })
        .attr({
          'cx': cx,
          'cy': cy
        })
        .style({
          'opacity': 0.5,
          'fill': 'transparent',
          'stroke': '#AAAAAA'
        })

      bubbleLegend.append('line')
        .attr({
          x1: 0,
          y1: lineY,
          x2: cx,
          y2: lineY
        })
        .style('stroke', '#AAAAAA')

      bubbleLegend.append('text')
        .attr('dx', 0)
        .attr('dy', lineY)
        .text(d => { return d })
        .style('fill', '#AAAAAA')
    }
  }
})

export default MapLegend
