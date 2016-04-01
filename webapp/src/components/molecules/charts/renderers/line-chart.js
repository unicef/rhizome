import _ from 'lodash'
import d3 from 'd3'
import hoverLine from 'components/molecules/charts/renderers/common/hover-line'
import axisLabel from 'components/molecules/charts/renderers/common/axis-label'
import label from 'components/molecules/charts/renderers/common/label'

class LineChartRenderer {
  constructor (data, options, container) {
    console.info('------- LineChartRenderer.constructor')
    this.setChartParams(data, options, container)
    this.prepContainer()
  }

  setChartParams (data, options, container) {
    console.info('------- LineChartRenderer.setChartParams')
    this.container = container
    this.options = options
    this.data = data
    this.margin = options.margin
    this.data.forEach(d => d.values = d.values.filter(item => item.value !== null))
    this.height = options.height - this.margin.top - this.margin.bottom
    this.width = options.width - this.margin.left - this.margin.right * 2
    this.h = this.height - options.margin.top - options.margin.bottom
    this.domain = _.isFunction(options.domain)
      ? options.domain(data)
      : d3.extent(_(data).map(options.values).flatten().map(options.x).value())
    this.range = _.isFunction(options.range)
      ? options.range(data)
      : d3.extent(_(data).map(options.values).flatten().map(options.y).value())
    this.range[0] = Math.min(this.range[0], 0)
    this.dataXScale = d3.time.scale().domain(this.domain).range([30, this.width])
    this.yScale = options.scale().domain(this.range).range([0.9 * this.height, 0])
    this.x = _.flow(options.x, this.dataXScale)
    this.y = _.flow(options.y, this.yScale)
    this.svg = d3.select(this.container)
  }

  update (data, options, container) {
    console.info('------- LineChartRenderer.update')
    this.setChartParams(data, options, container)
    this.render()
  }

  render () {
    // console.info('------- LineChartRenderer.render')
    this.renderLine()
    this.renderLabels()
    this.renderXAxis()
    this.renderYAxis()
    this.renderAnnotations()
    this.renderHoverline()
  }

  // =========================================================================== //
  //                                   RENDER                                    //
  // =========================================================================== //

  prepContainer () {
    // console.info('------- LineChartRenderer.prepContainer')
    this.svg.attr({
      'class': 'line',
      'viewBox': '0 0 ' + this.width + ' ' + this.height,
      'width': this.width,
      'height': this.height
    })

    this.svg.append('rect')
      .attr({
        'class': 'bg',
        'x': this.margin.left,
        'y': 0,
        'width': this.width - this.margin.left - this.margin.right,
        'height': this.h
      })

    const g = this.svg.append('g')
      .attr('transform', 'translate(' + this.margin.left + ', ' + this.margin.top + ')')

    g.append('g').attr('class', 'y axis')
    g.append('g').attr({
      'class': 'x axis',
      'transform': 'translate(0, ' + this.h + ')'
    })
    g.append('g').attr('class', 'data')
    g.append('g').attr('class', 'annotation')
  }

  // LINE
  // ---------------------------------------------------------------------------
  renderLine () {
    // console.info('LineChartRenderer.renderLine')
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
    // console.info('LineChartRenderer.renderXAxis')
    this.svg.select('.x.axis')
      .call(d3.svg.axis()
        .tickFormat(this.options.xFormat)
        .outerTickSize(0)
        .ticks(3)
        .scale(this.dataXScale)
        .orient('bottom'))
        .attr('transform', `translate(0, ${this.height - this.margin.top + 12})`)
        .selectAll('.domain').data([0])
          .attr('d', `M0,0V0H${this.width - 30}V0`)
          .attr('transform', 'translate(30, 0)')
  }

  // Y AXIS
  // ---------------------------------------------------------------------------
  renderYAxis () {
    // console.info('LineChartRenderer.renderYAxis')
    const gy = this.svg.select('.y.axis')
      .call(d3.svg.axis()
        .tickFormat(this.options.yFormat)
        .tickSize(this.width - 25)
        .tickPadding(30)
        .ticks(5)
        .scale(this.yScale)
        .orient('right'))
    gy.selectAll('line').attr('transform', 'translate(25, 0)')
    gy.selectAll('text').attr({'x': -6, 'y': -5, 'dy': 10})
    gy.selectAll('g').classed('minor', d => d !== this.range[0])
    d3.select(gy.selectAll('line')[0][0]).attr('visibility', 'hidden') // Hide lowest tick line
    d3.select(gy.selectAll('text')[0][0]).attr('visibility', 'hidden') // Hide lowest tick (usually 0)
  }

  // HOVERLINE
  // ---------------------------------------------------------------------------
  renderHoverline () {
    // console.info('LineChartRenderer.renderHoverline')
    this.svg.attr('class', 'line')
      .call(hoverLine()
        .width(this.width)
        .height(this.height)
        .xFormat(this.options.xFormat)
        .yFormat(this.options.yFormat)
        .x(this.options.x)
        .y(this.options.y)
        .xScale(this.dataXScale)
        .yScale(this.yScale)
        .value(this.options.y)
        .seriesName(_.property('seriesName'))
        .sort(true)
        .colorRange(this.options.colors)
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
    // console.info('LineChartRenderer.renderLabels')
    if (this.data.length === 1) {
      this.labels = _(this.data)
        .map(d => {
          return d.values.map(datapoint => {
            const v = this.options.y(datapoint)
            return {
              // text: this.options.seriesName(d) + ' ' + this.options.yFormat(v),
              x: this.x(datapoint),
              y: this.y(datapoint),
              defined: _.isFinite(v)
            }
          })
        })
        // .filter('defined')
        .sortBy('y')
        .value()
      this.labels = this.labels[0]
    }
  }

  // ANNOTATIONS
  // ---------------------------------------------------------------------------
  renderAnnotations () {
    const legendColorScale = d3.scale.ordinal()
      .domain(_(this.labels).map(d => d.text).uniq().sortBy().value())
      .range(this.options.colors)
    const legendColor = _.flow(d => d.text, legendColorScale)
    if (this.options.annotated) {
      this.svg.select('.annotation').selectAll('.series.label')
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