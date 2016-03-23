import _ from 'lodash'
import d3 from 'd3'
import React, { PropTypes, Component } from 'react'

import formatUtil from 'components/molecules/charts/utils/format'
import TableChartRenderer from 'components/molecules/charts/renderers/table-chart'

const DEFAULTS = {
  cellHeight: 24,
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
  values: _.property('values'),
  value: _.property('value'),
  sortDirection: 1
}

class TableChart extends Component {
	constructor(props) {
		super(props)
    this.options = _.defaults({}, props.options, DEFAULTS)
  }

  componentDidMount () {
    this.container = React.findDOMNode(this)
    this.table = new TableChartRenderer(this.props.data, this.options, this.container)
    this.table.render()
  }

  componentDidUpdate () {
    this.options = _.defaults({}, this.props.options, this.options)
    this.table.update(this.props.data, this.options, this.container)
  }

	render () {
		return (
			<svg className='heatmap sortable'>
		    <g className='margin'>
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

export default TableChart

