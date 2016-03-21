import _ from 'lodash'
import d3 from 'd3'
import React, { PropTypes, Component } from 'react'

import formatUtil from 'components/molecules/charts_d3/utils/format'
import TableHelpers from 'components/molecules/charts/TableHelpers'

const TABLE_DEFAULTS = {
  cellHeight: 16,
  column: _.property('indicator.short_name'),
  sourceColumn: _.property('short_name'),
  fontSize: 12,
  format: formatUtil.general,
  headerText: _.property('short_name'),
  headers: [],
  onClick: null,
  onColumnHeadOver: null,
  onColumnHeadOut: null,
  onMouseMove: null,
  onMouseOut: null,
  onRowClick: null,
  seriesName: _.property('name'),
  sortValue: TableHelpers.sortValue,
  values: _.property('values'),
  value: _.property('value'),
  sortDirection: 1
}

class TableChart extends Component {

	constructor(props) {
		console.log('------------------------------ constructor ------------------------------')
		super(props)
    const options = _.defaults({}, props.options, TABLE_DEFAULTS)
  	const h = Math.max(props.data.length * options.cellHeight, 0)
  	const z = 160 //  extra margin space needed to add the "z" (parent) axis
  	const w = 3 * Math.max(options.headers.length * options.cellHeight, 0)
  	const xDomainProvided = typeof (options.xDomain) !== 'undefined' && options.xDomain.length > 0
  	const xDomain = xDomainProvided ? options.xDomain : options.selected_indicators.map(ind => ind.short_name)
  	const xScale = d3.scale.ordinal().domain(xDomain).rangeBands([0, w], 0.1)
  	const sourceFlow = _.flow(options.sourceColumn, xScale)
  	const x = _.flow(options.column, xScale)
  	const margin = options.margin
  	const scale = d3.scale.ordinal().domain(['bad', 'ok', 'good']).range(options.color)
  	const domain = TableHelpers.getDomain(props.data, options)
  	const yScale = d3.scale.ordinal().domain(domain).rangeBands([0, h], 0.1)
  	const y = _.flow(options.seriesName, yScale)
  	const transform = (d, i) => `translate(${z}, ${y(d) + 10})`

  	this.table = {
	    options: options,
	  	h: h,
	  	z: z,
	  	w: w,
	  	xDomainProvided: xDomainProvided,
	  	xDomain: xDomain,
	  	xScale: xScale,
	  	sourceFlow: sourceFlow,
	  	x: x,
	  	margin: margin,
	  	scale: scale,
	  	domain: domain,
	  	yScale: yScale,
	  	y: y,
	  	transform: transform,
  	}
	}

	componentDidMount () {
		console.log('------------------------------ TableChart.jsx - componentDidMount ------------------------------')
		this.renderTable(this.props.data, this.table.options)
	}

	componentDidUpdate () {
		console.log('------------------------------ TableChart.jsx - componentDidUpdate ------------------------------')
		this.renderTable(this.props.data, this.table.options)
	}

  renderTable = (data, options) => {
  	console.log('------------------------------ TableChart.jsx - renderTable ------------------------------')
  	console.log('options', options)
  	console.log('------------------------------------------------------------------------------------------')
		this.container = React.findDOMNode(this)
    const container = this.container
    const margin = this.props.margin

    // COLORS - Move from here once the user can set a pallette
    // ---------------------------------------------------------------------------
    const targets = _(options.headers)
      .indexBy('id')
      .mapValues(ind => {
        const boundsReversed = ind.bad_bound > ind.good_bound
        const names = boundsReversed ? ['good', 'ok', 'bad'] : ['bad', 'ok', 'good']
        const extents = boundsReversed ? [ ind.good_bound, ind.bad_bound ] : [ ind.bad_bound, ind.good_bound ]
        return d3.scale.threshold().domain(extents).range(names)
      })
      .value()
    console.log('this', this)
    console.log('this.table', this.table)
    // CONTAINER
    // ---------------------------------------------------------------------------
    // hacky way to scale the view box.. this should be done by taking into account the user's screen size
    const calculatedHeightScale = 1 + (options.headers.length - 8) / 10
    const viewBoxHeightScale = calculatedHeightScale < 1 ? calculatedHeightScale : 1
    const viewBoxWidth = this.table.w + margin.left + margin.right - 150
    const viewBox = '0 0 ' + viewBoxWidth + ' ' + ((this.table.h * viewBoxHeightScale) + margin.top + margin.bottom)
    const svg = d3.select(this.container)
      .attr({
        'viewBox': viewBox,
        'width': (this.table.w + margin.left + margin.right),
        'height': (this.table.h + margin.top + margin.bottom)
      })
      .datum(this.props.data)
    svg.select('.margin').attr('transform', 'translate(-75, ' + margin.top + ')')

    const g = svg.select('.data')
    console.log('svg', svg)
    console.log('g', g)
    g.on('mouseout', () => TableHelpers.onRowOut.apply(this))

    // ROWS
    // ---------------------------------------------------------------------------
    const rows = g.selectAll('.row').data(this.props.data)
    rows.enter().append('g').attr({'class': 'row', 'transform': this.transform})
    rows.exit().transition().duration(300).style('opacity', 0).remove()
    rows.on('click', (d, i) => TableHelpers.onRowClick([d, i]))
    rows.on('mouseover', (d, i) => TableHelpers.onRowOver([d, i])).transition().duration(750).attr('transform', this.transform)

    // CELLS
    // ---------------------------------------------------------------------------

    const fill = d => this.table.scale(targets[d.indicator.id](d.value))
    const cells = rows.selectAll('.cell').data(options.values)
    cells.exit().transition().duration(300).style('opacity', 0).remove()
    cells.attr('id', d => [d.location.name, d.indicator.short_name].join('-'))
    cells.style('cursor', _.isFunction(options.onClick) ? 'pointer' : 'initial')
    cells.on('mousemove', options.onMouseMove)
    cells.on('mouseout', options.onMouseOut)
    cells.on('click', options.onClick)
    cells.transition().duration(500).style('fill', fill)
      .attr({
        'height': this.table.yScale.rangeBand(),
        'width': this.table.xScale.rangeBand(),
        'x': this.table.x
      })

    const cg = cells.enter().append('g')
    cg.append('rect')
      .attr({
        'class': 'cell',
        'height': this.table.yScale.rangeBand(),
        'x': this.table.x,
        'width': this.table.xScale.rangeBand()
      })
      .style({ 'opacity': 0, 'fill': fill })
      .transition().duration(500)
      .style('opacity', 1)
    console.log('RECT RAN')
    cg.append('text')
      .attr({
        'height': this.table.yScale.rangeBand(),
        'x': d => this.table.x(d) + this.table.xScale.rangeBand() / 2,
        'y': (options.cellHeight / 2) - (options.cellFontSize / 4.3),
        'width': this.table.xScale.rangeBand(),
        'dominant-baseline': 'central',
        'text-anchor': 'middle',
        'font-weight': 'bold'
      })
      .style({'font-size': options.cellFontSize})
      .text(d => d.displayValue)
      .transition().duration(500)
    console.log('TEXT RAN')

    // X AXIS
    // ---------------------------------------------------------------------------
    svg.select('.x.axis')
      .transition().duration(500)
      .attr({'transform': 'translate(' + this.table.z + ',-40)'})
      .call(d3.svg.axis().scale(this.table.xScale).orient('top').outerTickSize(0))
    svg.selectAll('.x.axis text').on('click', (d, i) => TableHelpers.setSort(d, i))
    svg.selectAll('.x.axis text')
      .attr({'transform': 'rotate(-45)'})
      .call(TableHelpers.wrap, this.table.xScale.rangeBand())

    // Y AXIS
    // ---------------------------------------------------------------------------
    svg.select('.y.axis')
      .transition().duration(500)
      .attr({'transform': 'translate(' + this.table.z + ',10)'})
      .call(d3.svg.axis().scale(this.table.yScale).orient('left').outerTickSize(0))
    svg.selectAll('.y.axis text')
      .style('font-size', options.fontSize + 2)
      .on('click', (d, i) => options.onRowClick(d, i, this))

    // Z AXIS
    // ---------------------------------------------------------------------------
    // the z axis shows the parent location//
    svg.select('.z.axis')
      .transition().duration(500)
      .attr({'transform': 'translate(20,10)'})
      .call(d3.svg.axis()
        .scale(this.table.yScale)
        .tickFormat(d => options.parentLocationMap[d].parent_location__name)
        .orient('left')
        .outerTickSize(0))
    svg.selectAll('.z.axis text')
      .style('font-size', options.fontSize)
      .on('click', (d, i) => options.onRowClick(options.parentLocationMap[d].parent_location__name, i, this))

    // FOOTER
    // ---------------------------------------------------------------------------
    var singleRowIndicators = options.headers // chartData[0].values
    var sourceFooter = svg.select('.source-footer').attr({'transform': 'translate(0,' + 10 + ')'})
    var sourceCell = sourceFooter.selectAll('.source-cell').data(singleRowIndicators)
    var sourceG = sourceCell.enter().append('g')

    sourceG.append('rect')
      .attr({
        'class': 'cell',
        'height': this.table.yScale.rangeBand() * 1.5,
        'transform': `translate(${this.table.z}, ${this.table.h})`,
        'x': this.table.sourceFlow,
        'width': this.table.xScale.rangeBand()
      })
      .style({ 'opacity': 0, 'fill': '#F1F1F1' })
      .transition().duration(500)
      .style('opacity', 1)

    sourceG.append('text')
      .attr({
        'height': this.table.yScale.rangeBand(),
        'transform': `translate(${this.table.z}, ${this.table.h})`,
        'x': d => sourceFlow(d) + options.cellHeight * 1.33,
        'y': options.cellHeight / 2,
        'width': this.table.xScale.rangeBand(),
        'dominant-baseline': 'central',
        'text-anchor': 'middle',
        'font-weight': 'bold'
      })
      .text(d => d.source_name)
      .transition().duration(500)
      .call(TableHelpers.wrap, this.table.xScale.rangeBand())

    // LEGEND
    // ---------------------------------------------------------------------------
    if (options.legend) {
      svg.select('.legend')
        .call(options.legend)
        .attr('transform', () => {
          const bbox = this.getBoundingClientRect()
          const dx = this.table.w + margin.right - bbox.width
          return `translate(${dx}, 0)`
        })
    } else {
      svg.select('.legend').selectAll('*').remove()
    }
  }

	render () {
		console.log('------------------------------ TableChart.jsx render ------------------------------')
		const props = this.props
		const margin = props.margin
   	const viewBox = '0 0 ' + props.width + ' ' + props.height

		return (
			<svg className='heatmap sortable' viewBox={viewBox} width={props.width} height={props.height}>
		    <g className='margin' transform={`translate(-75, ${margin.top})`}>
		    	<g className='z axis'></g>
		    	<g className='y axis'></g>
		    	<g className='x axis'></g>
		    	<g className='data'></g>
		    	<g className='source-footer'></g>
		    	<g className='legend'></g>
		    </g>
			</svg>
		)
	}
}

TableChart.propTypes = {
	width: PropTypes.number,
	height: PropTypes.number,
  margin: PropTypes.shape({
    top: PropTypes.number,
    right: PropTypes.number,
    bottom: PropTypes.number,
    left: PropTypes.number
  })
}

TableChart.DEFAULTS = {
  cellHeight: 16,
  column: _.property('indicator.short_name'),
  sourceColumn: _.property('short_name'),
  fontSize: 12,
  format: formatUtil.general,
  headerText: _.property('short_name'),
  headers: [],
  onClick: null,
  onColumnHeadOver: null,
  onColumnHeadOut: null,
  onMouseMove: null,
  onMouseOut: null,
  onRowClick: null,
  seriesName: _.property('name'),
  sortValue: TableHelpers.sortValue,
  values: _.property('values'),
  value: _.property('value'),
  sortDirection: 1
}



export default TableChart

