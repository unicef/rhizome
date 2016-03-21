import _ from 'lodash'
import d3 from 'd3'
import React, { PropTypes, Component } from 'react'

import hoverLine from 'components/molecules/charts_d3/line_chart/hover-line'

import label from 'components/molecules/charts_d3/renderer/label'
import axisLabel from 'components/molecules/charts_d3/renderer/axis-label'

import palettes from 'components/molecules/charts_d3/utils/palettes'
import format from 'components/molecules/charts_d3/utils/format'


const DEFAULTS = {
  margin: {
    top: 12,
    right: 0,
    bottom: 20,
    left: 0
  },
  annotated: false,
  scale: d3.scale.linear,
  seriesName: _.property('name'),
  values: _.property('values'),
  color: palettes.blue,
  x: _.property('campaign.start_date'),
  xFormat: format.timeAxis,
  y: _.property('value'),
  yFormat: d3.format(',d')
}

class LineChart extends Component {

	constructor(props) {
		console.log('------------------------------ constructor ------------------------------')
		super(props)
    this.options = _.defaults({}, props.options, DEFAULTS)
    this.yFormat = d3.format(',d')
	}

	componentDidMount () {
		console.log('------------------------------ TableChart.jsx - componentDidMount ------------------------------')
		this.renderTable(this.props.data, this.options)
	}

	componentDidUpdate () {
		console.log('------------------------------ TableChart.jsx - componentDidUpdate ------------------------------')
		this.renderTable(this.props.data, this.options)
	}

  renderTable (series, options) {
  	console.log('series', series)
  	console.log('options', options)
		this.container = React.findDOMNode(this)
    const container = this.container
    const margin = this.props.margin
    const svg = d3.select(this.container)

    series = _(series).each(serie => {
      serie.values = _(serie.values).reject(item => item.value === null).value()
    }).value()


    const height = (options.height <= 2 ? this.props.height : options.height) - margin.top - margin.bottom
    const width = this.props.width - margin.left - margin.right * 2

    // COLORS
    // ---------------------------------------------------------------------------
    const dataColorScale = d3.scale.ordinal()
      .domain(_(series)
        .map(options.seriesName)
        .uniq()
        .sortBy()
        .value())
      .range(options.color)

    const dataColor = _.flow(options.seriesName, dataColorScale)

    const legendColorScale = d3.scale.ordinal()
      .domain(_(labels).map(d => d.text).uniq().sortBy().value())
      .range(options.color)

    const legendColor = _.flow(d => d.text, legendColorScale)
    console.log('COLORS RAN')

    // DOMAIN & RANGE
    // ---------------------------------------------------------------------------
    const domain = _.isFunction(options.domain)
      ? options.domain(series)
      : d3.extent(_(series)
      .map(options.values)
      .flatten()
      .map(options.x)
      .value())

    let range = _.isFunction(options.range)
      ? options.range(series)
      : d3.extent(_(series)
      .map(options.values)
      .flatten()
      .map(options.y)
      .value())

    range[0] = Math.min(range[0], 0)
    console.log('DOMAIN AND RANGE RAN')

    // BODY
    // ---------------------------------------------------------------------------
    console.log('width', width)
    const dataXScale = d3.time.scale().domain(domain).range([30, width])
    const yScale = options.scale().domain(range).range([0.9 * height, 0])
    const x = _.flow(options.x, dataXScale)
    const y = _.flow(options.y, yScale)
    const g = svg.select('.data').selectAll('.series').data(series, options.seriesName)
    g.enter().append('g').attr('class', 'series')
    g.style({ 'fill': dataColor, 'stroke': dataColor })
    g.exit().remove()

    const path = g.selectAll('path').data(d => [options.values(d)])
    path.enter().append('path')
    path.transition().duration(500).attr('d', d3.svg.line().x(x).y(y))

    g.selectAll('line').data(options.values)
    console.log('BODY RAN')

    // LABELS
    // ---------------------------------------------------------------------------
    const labels = _(series)
      .map(d => {
        const last = _.max(options.values(d), options.x)
        const v = options.y(last)
        return {
          text: options.seriesName(d) + ' ' + this.yFormat(v),
          x: x(last),
          y: y(last),
          defined: _.isFinite(v)
        }
      })
      .filter('defined')
      .sortBy('y')
      .value()
    console.log(1)
    if (options.xLabel || options.yLabel) {
      svg.call(axisLabel()
      .data(options.xLabel, options.yLabel)
      .width(width)
      .height(height)
      .margin(options.margin))
    }
    console.log('LABELS')

    // X AXIS
    // ---------------------------------------------------------------------------
    svg.select('.x.axis')
      .call(d3.svg.axis()
        .tickFormat(options.xFormat)
        .outerTickSize(0)
        .ticks(3)
        .scale(dataXScale)
        .orient('bottom'))
    svg.select('.x.axis')
      .attr('transform', `translate(0, ${height - (options.margin.bottom + options.margin.top)})`)
      .selectAll('.domain').data([0]).attr('d', `M0,0V0H${width}V0`)
    console.log('X AXIS')

    // Y AXIS
    // ---------------------------------------------------------------------------
    const gy = svg.select('.y.axis')
      .call(d3.svg.axis()
        .tickFormat(this.yFormat)
        .tickSize(width - 25)
        .tickPadding(30)
        .ticks(4)
        .scale(yScale)
        .orient('right'))
    gy.selectAll('line').attr('transform', 'translate(25, 0)')
    gy.selectAll('text').attr({'x': -6, 'y': -5, 'dy': 10})
    gy.selectAll('g').classed('minor', d => d !== range[0])
    d3.select(gy.selectAll('line')[0][0]).attr('visibility', 'hidden') // Hide lowest tick line
    d3.select(gy.selectAll('text')[0][0]).attr('visibility', 'hidden') // Hide lowest tick (usually 0)

    // HOVERLINE
    // ---------------------------------------------------------------------------
    svg.attr('class', 'line')
      .call(hoverLine()
        .width(width)
        .height(height)
        .xFormat(options.xFormat)
        .yFormat(this.yFormat)
        .x(options.x)
        .y(options.y)
        .xScale(dataXScale)
        .yScale(yScale)
        .value(options.y)
        .seriesName(_.property('seriesName'))
        .sort(true)
        .colorRange(options.color)
        .datapoints(_(series).map(s => {
          return _.map(options.values(s), _.partial(_.set, _, 'seriesName', options.seriesName(s)))
        })
        .flatten()
        .value()
      )
    )
    console.log('HOVERLINE')

    // ANNOTATIONS
    // ---------------------------------------------------------------------------
    if (options.annotated) {
      svg.select('.annotation').selectAll('.series.label')
        .data(labels)
        .call(label()
          .addClass('series')
          .width(width)
          .height(height)
          .align(false)
          .scale(legendColor)
          .dots(options.hasDots))
    }
    console.log('ANNOTATIONS')
  }
	render () {
		const props = this.props
		const margin = props.margin
  	const viewBox = '0 0 ' + props.width + ' ' + props.height
 	 	const bg_height = props.height - margin.top - margin.bottom
 	 	const bg_width = props.width - margin.left - margin.right

		return (
			<svg className='line' viewBox={viewBox} width={props.width} height={props.height}>
	    	<rect className='bg' width={bg_width} height={bg_height} x={margin.left} y={0}></rect>
		    <g transform={`translate(${margin.left}, ${margin.top})`}>
		    	<g className='y axis'></g>
		    	<g className='x axis' transform={`translate(0, ${bg_height})`}></g>
		    	<g className='data'></g>
		    	<g className='annotation'></g>
		    </g>
			</svg>
		)
	}
}

LineChart.propTypes = {
	width: PropTypes.number,
	height: PropTypes.number,
  margin: PropTypes.shape({
    top: PropTypes.number,
    right: PropTypes.number,
    bottom: PropTypes.number,
    left: PropTypes.number
  })
}


export default LineChart

