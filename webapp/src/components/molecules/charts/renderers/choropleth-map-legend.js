import _ from 'lodash'
import d3 from 'd3'
import legend from 'components/molecules/charts/renderers/common/legend'
import browser from 'components/molecules/charts/utils/browser'


class ChoroplethMapLegendRenderer {
  constructor (data, options, container) {
    console.info('------- MapLegendRenderer.constructor')
    this.setChartParams(data, options, container)
    this.prepContainer()
  }

  setChartParams (data, options, container) {
    console.info('------- MapLegendRenderer.setChartParams')
    this.container = container
    this.options = options
    this.data = data
    this.margin = options.margin
    this.height = options.height - this.margin.top - this.margin.bottom
    this.width = options.width - this.margin.left - this.margin.right * 2
    this.svg = d3.select(this.container)
  }

  update (data, options, container) {
    console.info('------- MapLegendRenderer.update')
    this.setChartParams(data, options, container)
    this.render()
  }

  render () {
    console.info('------- MapLegendRenderer.render')
    this.renderColorLegend()
    this.renderStripesLegend()
    this.renderBubbleLegend()
  }

  // =========================================================================== //
  //                                   RENDER                                    //
  // =========================================================================== //

  prepContainer () {
    console.info('------- MapLegendRenderer.prepContainer')
    var svg = this.svg
      .attr({
        'class': 'reds',
        'viewBox': '-300 80 ' + this.width + ' ' + this.height
      })

    if (browser.isIE() || browser.isWkhtmlToPdf()) {
      svg.attr({
        'width': this.width,
        'height': this.height
      })
    }

    var g = svg.append('g').attr('transform', 'translate(' + this.margin.left + ', ' + this.margin.top + ')')

    g.append('g').attr('class', 'legend')
    svg.append('g').attr('class', 'bubbles')
    svg.select('.bubbles').append('g').attr('class', 'legend')
    svg.append('g').attr('class', 'stripes')
    svg.select('.stripes').append('g').attr('class', 'legend')

    const lineWidth = 10
    const lineHeight = 10
    const lineInterval = 5

    const defs = svg.append('defs')

    const pattern = defs.append('pattern')
      .attr({
        'id': 'stripe',
        'patternUnits': 'userSpaceOnUse',
        'width': lineWidth,
        'height': lineHeight
      })

    pattern.append('line').attr({'x1': 0, 'y1': 0, 'x2': -lineInterval, 'y2': lineHeight})
    pattern.append('line').attr({'x1': lineInterval, 'y1': 0, 'x2': 0, 'y2': lineHeight})
    pattern.append('line').attr({'x1': 2 * lineInterval, 'y1': 0, 'x2': lineInterval, 'y2': lineHeight})
    pattern.selectAll('line')
      .style('stroke', '#cccccc')
      .attr({'stroke-linecap': 'square', 'stroke-linejoin': 'miter', 'stroke-width': 1})
  }

  // MAP COLOR LEGEND
  // ---------------------------------------------------------------------------
  renderColorLegend () {
    console.log('------- MapLegendRenderer.renderColorLegend')
    if (this.options.value) {
      const features = _.reject(this.data, 'properties.isBorder')
      let domain = this.options.domain(features)

      if (!_.isArray(domain)) {
        domain = d3.extent(features, this.options.value)
        domain[0] = Math.min(domain[0], 0)
      }

      const colors = this.options.color.concat().reverse()
      const colorScale = d3.scale.quantize().domain(domain).range(colors)

      const legendTicks = this.buildTicksFromBounds(this.options)
      this.svg.select('.legend')
      .call(legend().scale(d3.scale.ordinal()
        .domain(legendTicks)
        .range(colorScale.range())))
      .attr('transform', () => 'translate(2, 0)')
    }
  }

  // MAP STRIPES LEGEND
  // ---------------------------------------------------------------------------
  renderStripesLegend () {
    console.log('------- MapLegendRenderer.renderStripesLegend')
    if (this.options.stripeValue) {
      const stripeLegendColor = d3.scale.ordinal().range(['#FFFFFF', 'url(#stripe)'])
      const stripeLegendText = this.options.stripeLegendText
      const stripeLegend = this.svg.select('.stripes').select('.legend')
        .attr('transform', () => 'translate(' + 2 + ', ' + 0 + ')')
        .selectAll('.series').data(stripeLegendText)
        .enter().append('g')
        .attr('class', 'series')
        .attr('transform', (d, i) => `translate(0, ${i * 15})`)

      stripeLegend.append('rect')
        .attr('width', 11)
        .attr('height', 11)
        .style({
          'fill': stripeLegendColor,
          'stroke': '#cccccc',
          'stroke-width': 1
        })

      stripeLegend.append('text')
        .attr({'x': 16, 'y': 3.5, 'dy': 6})
        .style({'text-anchor': 'start', 'font-size': 12})
        .text(d => d)
    }
  }

  // MAP BUBBLES LEGEND
  // ---------------------------------------------------------------------------
  renderBubbleLegend () {
    console.log('------- MapLegendRenderer.renderBubbleLegend')
    if (this.options.bubbleValue) {
      const radius = d3.scale.sqrt().domain([0, this.options.maxBubbleValue]).range([0, this.options.maxBubbleRadius])
      const bubbleLegendText = _.map(this.options.bubbleLegendRatio, d => Math.ceil(d * this.options.maxBubbleValue, -1))
      const bubbleLegend = this.svg.select('.bubbles').select('.legend')
        .attr('transform', () => 'translate(2, 0)')
        .selectAll('.series').data(bubbleLegendText)
        .enter().append('g')
        .attr('class', 'series')

      let cx = 2.5 * this.options.maxBubbleRadius
      let cy = d => 2.5 * this.options.maxBubbleRadius - radius(d)
      const lineY = d => cy(d) - radius(d)

      bubbleLegend.append('circle')
        .attr('r', d => radius(d))
        .attr({ 'cx': cx, 'cy': cy })
        .style({'opacity': 0.5, 'fill': 'transparent', 'stroke': '#AAAAAA'})

      bubbleLegend.append('line')
        .attr({ x1: 0, y1: lineY, x2: cx, y2: lineY })
        .style('stroke', '#AAAAAA')

      bubbleLegend.append('text')
        .attr('dx', 0)
        .attr('dy', lineY)
        .text(d => d)
        .style('fill', '#AAAAAA')
    }
  }

  buildTicksFromBounds (options) {
    // green/yellow/red pattern for 0, 1, 2
    // legendText[0] = good bound, [1] = middle, [2] = bad bound
    let legendTicks = []
    if (this.options.data_format === 'bool') {
      legendTicks[1] = 'No'
      legendTicks[0] = 'Yes'
    } else if (this.options.data_format === 'pct') {
      this.options.ticks.badBound *= 100
      this.options.ticks.goodBound *= 100
      legendTicks[1] = `${this.options.ticks.badBound}%-${this.options.ticks.goodBound}%`
      if (this.options.ticks.reversed) {
        legendTicks[0] = `0%-${this.options.ticks.badBound}%`
        legendTicks[2] = `${this.options.ticks.goodBound}%-100%`
      } else {
        legendTicks[2] = `0%-${this.options.ticks.badBound}%`
        legendTicks[0] = `${this.options.ticks.goodBound}%-100%`
      }
    } else if (this.options.data_format === 'int') {
      // double check actual data with this logic
      legendTicks[1] = `${this.options.ticks.badBouznd}-${this.options.ticks.goodBound}`
      if (this.options.ticks.reversed) {
        legendTicks[0] = `0-${this.options.ticks.badBound}`
        legendTicks[2] = `${this.options.ticks.goodBound}+`
      } else {
        legendTicks[2] = `0-${this.options.ticks.badBound}`
        legendTicks[0] = `${this.options.ticks.goodBound}+`
      }
    }
    return legendTicks
  }
}

export default ChoroplethMapLegendRenderer