import React from 'react'
import _ from 'lodash'
import d3 from 'd3'
import Tooltip from 'components/molecules/Tooltip'
import hoverLine from 'components/molecules/charts_d3/line_chart/hover-line'
import Layer from 'react-layer'

class LineChartRenderer {
  constructor (data, options, container) {
    this.setChartParams(data, options, container)
  }

  setChartParams (data, options, container) {
    this.container = container
    this.options = options
    this.data = data
    this.data.forEach(d => d.values = d.values.filter(item => item.value !== null))
    this.height = options.height - options.margin.top - options.margin.bottom
    this.width = options.width - options.margin.left - options.margin.right * 2
    this.domain = _.isFunction(options.domain)
      ? options.domain(data)
      : d3.extent(_(data)
      .map(options.values)
      .flatten()
      .map(options.x)
      .value())
   this.range = _.isFunction(options.range)
      ? options.range(data)
      : d3.extent(_(data)
      .map(options.values)
      .flatten()
      .map(options.y)
      .value())
    this.range[0] = Math.min(this.range[0], 0)
    this.dataXScale = d3.time.scale().domain(this.domain).range([30, this.width])
    this.yScale = options.scale().domain(this.range).range([0.9 * this.height, 0])
    this.yFormat = d3.format(',d')
    this.x = _.flow(options.x, this.dataXScale)
    this.y = _.flow(options.y, this.yScale)
    this.svg = d3.select(this.container)
  }

  update () {
    this.setChartParams(this.data, this.options, this.container)
    this.render()
  }

  render () {
    this.renderLine()
    this.renderLabels()
    this.renderXAxis()
    this.renderYAxis()
    this.renderAnnotations()
    this.renderHoverline()
  }

  //===========================================================================//
  //                                   RENDER                                  //
  //===========================================================================//

  // LINE
  // ---------------------------------------------------------------------------
  renderLine () {
    const dataColorScale = d3.scale.ordinal()
      .domain(_(this.data)
        .map(this.options.seriesName)
        .uniq()
        .sortBy()
        .value())
      .range(this.options.colors)
    const dataColor = _.flow(this.options.seriesName, dataColorScale)
    const g = this.svg.select('.data').selectAll('.series').data(this.data, this.options.seriesName)
    g.enter().append('g').attr('class', 'series')
    g.style({ 'fill': dataColor, 'stroke': dataColor })
    g.exit().remove()

    const path = g.selectAll('path').data(d => [this.options.values(d)])
    path.enter().append('path')
    path.transition().duration(500).attr('d', d3.svg.line().x(this.x).y(this.y))

    g.selectAll('line').data(this.options.values)
  }

  // X AXIS
  // ---------------------------------------------------------------------------
  renderXAxis () {
    this.svg.select('.x.axis')
      .call(d3.svg.axis()
        .tickFormat(this.options.xFormat)
        .outerTickSize(0)
        .ticks(3)
        .scale(this.dataXScale)
        .orient('bottom'))
        .attr('transform', `translate(0, ${this.height - this.options.margin.top})`)
        .selectAll('.domain').data([0]).attr('d', `M0,0V0H${this.width}V0`)
  }

  // Y AXIS
  // ---------------------------------------------------------------------------
  renderYAxis () {
    const gy = this.svg.select('.y.axis')
      .call(d3.svg.axis()
        .tickFormat(this.yFormat)
        .tickSize(this.width - 25)
        .tickPadding(30)
        .ticks(4)
        .scale(this.yScale)
        .orient('right'))
    gy.selectAll('line').attr('transform', 'translate(25, 0)')
    gy.selectAll('text').attr({'x': -6, 'y': -5, 'dy': 10})
    gy.selectAll('g').classed('minor', d => d !== this.range[0])
    // d3.select(gy.selectAll('line')[0][0]).attr('visibility', 'hidden') // Hide lowest tick line
    // d3.select(gy.selectAll('text')[0][0]).attr('visibility', 'hidden') // Hide lowest tick (usually 0)
  }

  // HOVERLINE
  // ---------------------------------------------------------------------------
  renderHoverline () {
    this.svg.attr('class', 'line')
      .call(hoverLine()
        .width(this.width)
        .height(this.height)
        .xFormat(this.options.xFormat)
        .yFormat(this.yFormat)
        .x(this.options.x)
        .y(this.options.y)
        .xScale(this.dataXScale)
        .yScale(this.yScale)
        .value(this.options.y)
        .seriesName(_.property('seriesName'))
        .sort(true)
        .colorRange(this.options.color)
        .datapoints(_(this.data).map(d => {
          return _.map(this.options.values(d), _.partial(_.set, _, 'seriesName', this.options.seriesName(d)))
        })
        .flatten()
        .value()
      )
    )
  }

  // LABELS
  // ---------------------------------------------------------------------------
  renderLabels () {
    this.labels = _(this.data)
      .map(d => {
        const last = _.max(this.options.values(d), this.options.x)
        const v = this.options.y(last)
        return {
          text: this.options.seriesName(d) + ' ' + this.yFormat(v),
          x: this.x(last),
          y: this.y(last),
          defined: _.isFinite(v)
        }
      })
      .filter('defined')
      .sortBy('y')
      .value()
    if (this.options.xLabel || this.options.yLabel) {
      svg.call(axisLabel()
      .data(this.options.xLabel, this.options.yLabel)
      .width(width)
      .height(height)
      .margin(this.options.margin))
    }
  }


  // ANNOTATIONS
  // ---------------------------------------------------------------------------
  renderAnnotations () {
    const legendColorScale = d3.scale.ordinal()
      .domain(_(this.labels).map(d => d.text).uniq().sortBy().value())
      .range(this.options.color)
    const legendColor = _.flow(d => d.text, legendColorScale)
    if (this.options.annotated) {
      svg.select('.annotation').selectAll('.series.label')
        .data(this.labels)
        .call(label()
          .addClass('series')
          .width(this.width)
          .height(this.height)
          .align(false)
          .scale(legendColor)
          .dots(this.options.hasDots))
    }
  }
}

export default LineChartRenderer