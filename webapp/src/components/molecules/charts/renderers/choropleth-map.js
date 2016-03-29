import React from 'react'
import _ from 'lodash'
import d3 from 'd3'
import Layer from 'react-layer'
import Tooltip from 'components/molecules/Tooltip'
import legend from 'components/molecules/charts/renderers/common/legend'

class ChoroplethMapRenderer {
  constructor (data, options, container) {
    console.log('------- MapRenderer.constructor')
    this.setMapParams(data, options, container)
  }

  setMapParams (data, options, container) {
    console.log('------- MapRenderer.setMapParams')
    this.container = container
    this.options = options
    this.data = data
    this.features = _.reject(data, 'properties.isBorder')
    this.w = options.width - options.margin.left - options.margin.right
    this.h = options.height - options.margin.top - options.margin.bottom
    this.path = this.calculatePath(this.features, this.w, this.h)
    this.colorScale = this.getColorScale(options.domain, options.colors)
    this.svg = d3.select(container)
  }

  update (data, options, container) {
    console.log('------- MapRenderer.update')
    this.setMapParams(data, options, container)
    this.render()
  }

  //===========================================================================//
  //                                   RENDER                                  //
  //===========================================================================//

  render () {
    console.log('------- MapRenderer.render')
    const svg = d3.select(this.container)
    svg.attr({
      'viewBox': '0 0 ' + this.options.width + ' ' + this.options.height,
      'width': this.options.width,
      'height': this.options.height,
      'preserveAspectRatio': 'xMinYMin'
    })
    this.renderMapPaths()
    this.renderColorLegend()
  }

  // RENDER MAP PATHS
  // ---------------------------------------------------------------------------
  renderMapPaths() {
    const map = this.svg.select('.colors')
    const g = map.select('.data')
    const location = g.selectAll('.location').data(this.features, (d, i) => d['properties.location_id'] || i)
    location.enter().append('path')
    location.attr({
      'd': this.path,
      'class': d => {
        let classNames = ['location']
        if (_.isFinite(d.properties.value)) {
          classNames.push('clickable')
        }
        if (d.location_type_id === 1) {
          classNames.push('country-path')
        } else if (d.location_type_id === 2) {
          classNames.push('province-path')
        } else if (d.location_type_id === 3) {
          classNames.push('district-path')
        }
        return classNames.join(' ')
      }
    })
    .style('fill', d => {
      var v = d.properties.value
      return _.isFinite(v) ? this.getColor(v, this.options.domain, this.options.colors, this.options.data_format) : '#fff'
    })
    .on('click', this._onClick)
    .on('mousemove', this._onMouseMove)
    .on('mouseout', this._onMouseOut)

    // const svg_width = map.node().getBBox().width
    const map_width = map.node().getBoundingClientRect().width
    const offset = (this.container.clientWidth - map_width) / 2
    map.attr('transform', `translate(${offset + (offset * 0.3)}, ${-offset/4})`)
    location.exit().remove()
  }

  // MAP COLOR LEGEND
  // ---------------------------------------------------------------------------
  renderColorLegend () {
    console.log('------- MapLegendRenderer.renderColorLegend')
    const features = _.reject(this.data, 'properties.isBorder')
    let domain = this.options.domain(features)
    if (!_.isArray(domain)) {
      domain = d3.extent(features, this.options.value)
      domain[0] = Math.min(domain[0], 0)
    }

    const colors = this.options.colors.concat().reverse()
    const colorScale = d3.scale.quantize().domain(domain).range(colors)
    const legendTicks = this.buildTicksFromBounds(this.options)
    const g  = this.svg.select('.colors')
    g.select('.legend').call(legend().scale(d3.scale.ordinal()
      .domain(legendTicks)
      .range(colorScale.range())))
    .attr('transform', () => 'translate(50, 75)')
  }

  // MAP STRIPES LEGEND
  // ---------------------------------------------------------------------------
  // renderStripesLegend () {
  //   console.log('------- MapLegendRenderer.renderStripesLegend')
  //   if (this.options.stripeValue) {
  //     const stripeLegendColor = d3.scale.ordinal().range(['#FFFFFF', 'url(#stripe)'])
  //     const stripeLegendText = this.options.stripeLegendText
  //     const stripeLegend = this.svg.select('.stripes').select('.legend')
  //       .attr('transform', () => 'translate(' + 2 + ', ' + 0 + ')')
  //       .selectAll('.series').data(stripeLegendText)
  //       .enter().append('g')
  //       .attr('class', 'series')
  //       .attr('transform', (d, i) => `translate(0, ${i * 15})`)

  //     stripeLegend.append('rect')
  //       .attr('width', 11)
  //       .attr('height', 11)
  //       .style({
  //         'fill': stripeLegendColor,
  //         'stroke': '#cccccc',
  //         'stroke-width': 1
  //       })

  //     stripeLegend.append('text')
  //       .attr({'x': 16, 'y': 3.5, 'dy': 6})
  //       .style({'text-anchor': 'start', 'font-size': 12})
  //       .text(d => d)
  //   }
  // }

  // MAP BUBBLES LEGEND
  // ---------------------------------------------------------------------------
  // renderBubbleLegend () {
  //   console.log('------- MapLegendRenderer.renderBubbleLegend')
  //   if (this.options.bubbleValue) {
  //     const radius = d3.scale.sqrt().domain([0, this.options.maxBubbleValue]).range([0, this.options.maxBubbleRadius])
  //     const bubbleLegendText = _.map(this.options.bubbleLegendRatio, d => Math.ceil(d * this.options.maxBubbleValue, -1))
  //     const bubbleLegend = this.svg.select('.bubbles').select('.legend')
  //       .attr('transform', () => 'translate(2, 0)')
  //       .selectAll('.series').data(bubbleLegendText)
  //       .enter().append('g')
  //       .attr('class', 'series')

  //     let cx = 2.5 * this.options.maxBubbleRadius
  //     let cy = d => 2.5 * this.options.maxBubbleRadius - radius(d)
  //     const lineY = d => cy(d) - radius(d)

  //     bubbleLegend.append('circle')
  //       .attr('r', d => radius(d))
  //       .attr({ 'cx': cx, 'cy': cy })
  //       .style({'opacity': 0.5, 'fill': 'transparent', 'stroke': '#AAAAAA'})

  //     bubbleLegend.append('line')
  //       .attr({ x1: 0, y1: lineY, x2: cx, y2: lineY })
  //       .style('stroke', '#AAAAAA')

  //     bubbleLegend.append('text')
  //       .attr('dx', 0)
  //       .attr('dy', lineY)
  //       .text(d => d)
  //       .style('fill', '#AAAAAA')
  //   }
  // }

  //===========================================================================//
  //                               EVENT HANDLERS                              //
  //===========================================================================//
  _onMouseMove = (location) => {

    const xFormat = value => {
      const format = this.options.data_format === 'pct' ? ',.1%' : Math.abs(value) < 1 ? '.4f' : 'n'
      return d3.format(format)(value)
    }
    let locationValue = xFormat(this.valueForLocation(this.data, location) || 0)
    if (this.options.data_format === 'bool') {
      locationValue = Math.abs(locationValue) !== 0 ? 'Yes' : 'No'
    }
    const displayValue = location.properties.name + ': ' + locationValue
    const evt = d3.event
    const render = () => <Tooltip left={evt.pageX + 2} top={ evt.pageY + 2}>{displayValue}</Tooltip>
    this.layer ? this.layer._render = render : this.layer = new Layer(document.body, render)
    this.layer.render()
  }

  _onMouseOut = () => {
    if (this.layer) {
      this.layer.destroy()
      this.layer = null
    }
  }

  _onClick = (location) => {
    if (this.layer) {
      this.layer.destroy()
      this.layer = null
    }
    this.options.onClick(location.properties.location_id)
  }

  //===========================================================================//
  //                                    UTILITIES                              //
  //===========================================================================//
  getDomain (domain) {
    if (!_.isArray(domain)) {
      domain = d3.extent(this.features, this.options.value) // Deal with this options.value - not sure how
      domain[0] = Math.min(domain[0], 0)
    }
    return domain
  }

  calculateBounds (features) {
    if (features.length < 1) {
      return [[0, 0], [0, 0]]
    }

    const coordinates = _(features).map(feature => {
      if (feature.geometry.type !== 'MultiPolygon') {
        return _.flatten(feature.geometry.coordinates)
      }
    })
    .flatten()
    .value()

    const lat = _.property(1)
    const lng = _.property(0)
    const left = d3.min(coordinates, lng)
    const right = d3.max(coordinates, lng)
    const bottom = d3.min(coordinates, lat)
    const top = d3.max(coordinates, lat)

    return [[left, top], [right, bottom]]
  }

  calculateCenter (bounds) {
    const lat = bounds[1][1] + ((bounds[0][1] - bounds[1][1]) / 2)
    const lng = bounds[0][0] + ((bounds[1][0] - bounds[0][0]) / 2)

    return [lng, lat]
  }

  calculatePath (features, width, height) {
    const bounds = this.calculateBounds(features)
    const center = this.calculateCenter(bounds)
    const projection = d3.geo.conicEqualArea()
      .parallels([bounds[1][1], bounds[0][1]])
      .rotate([-center[0], 0])   // Rotate the globe so that the country is centered horizontally
      .center([0, center[1]])    // Set the center of the projection so that the polygon is moved vertically into the center of the viewport
      .translate([width / 2, height / 2]) // Translate to the center of the viewport
      .scale(1)
    const b = [projection(bounds[0]), projection(bounds[1])]
    const s = 1 / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height)
    projection.scale(s)
    return d3.geo.path().projection(projection)
  }

  roundToTwo (num) {
    return +(Math.round(num + 'e+3') + 'e-3')
  }

  getColorScale(domain, colors) {
    if (!_.isArray(domain)) {
      domain = d3.extent(this.features, this.options.value) // Deal with this options.value - not sure how
      domain[0] = Math.min(domain[0], 0)
    }
    return d3.scale.threshold().domain(domain.concat()).range(colors.concat())
  }

  getColor (indicatorValue, domain, colors, data_format) {
    const bad_bound = domain()[0]
    const good_bound = domain()[1]
    const reverseBounds = bad_bound > good_bound
    let mapFillColor = ''
    indicatorValue = this.roundToTwo(indicatorValue)
    if (data_format === 'bool') {
      if (indicatorValue === 0) {
        mapFillColor = colors[0]
      } else {
        mapFillColor = colors[1]
      }
    } else {
      if (reverseBounds) {
        if (indicatorValue > good_bound && indicatorValue < bad_bound) {
          mapFillColor = colors[1]
        } else if (indicatorValue <= good_bound) {
          mapFillColor = colors[2]
        } else if (indicatorValue >= bad_bound) {
          mapFillColor = colors[0]
        }
      } else {
        if (indicatorValue < good_bound && indicatorValue > bad_bound) {
          mapFillColor = colors[1]
        } else if (indicatorValue >= good_bound) {
          mapFillColor = colors[2]
        } else if (indicatorValue <= bad_bound) {
          mapFillColor = colors[0]
        }
      }
    }
    return mapFillColor
  }

  valueForLocation (data, locationObject) {
    let locationIndex = (_.select(data, d => d.location_id === locationObject.location_id))[0]
    return locationIndex.properties.value
  }

  chooseRadius (v, radius) {
    if (v > radius.domain()[1]) {
      return radius.range()[1]
    } else {
      return radius(v)
    }
  }

  buildTicksFromBounds (options) {
    // green/yellow/red pattern for 0, 1, 2
    // legendText[0] = good bound, [1] = middle, [2] = bad bound
    const ticks = this.options.ticks
    let legendTicks = []
    if (this.options.data_format === 'bool') {
      legendTicks[1] = 'No'
      legendTicks[0] = 'Yes'
    } else if (this.options.data_format === 'pct') {
      this.options.ticks.bad *= 100
      this.options.ticks.good *= 100
      legendTicks[1] = `${ticks.bad}%-${ticks.good}%`
      if (ticks.reversed) {
        legendTicks[0] = `0%-${ticks.bad}%`
        legendTicks[2] = `${ticks.good}%-100%`
      } else {
        legendTicks[2] = `0%-${ticks.bad}%`
        legendTicks[0] = `${ticks.good}%-100%`
      }
    } else if (this.options.data_format === 'int') {
      // double check actual data with this logic
      legendTicks[1] = `${ticks.bad}-${ticks.good}`
      if (ticks.reversed) {
        legendTicks[0] = `0-${ticks.bad}`
        legendTicks[2] = `${ticks.good}+`
      } else {
        legendTicks[2] = `0-${ticks.bad}`
        legendTicks[0] = `${ticks.good}+`
      }
    }
    return legendTicks
  }


}

export default ChoroplethMapRenderer