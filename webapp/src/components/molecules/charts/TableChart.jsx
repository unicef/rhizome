import _ from 'lodash'
import d3 from 'd3'
import React, { PropTypes, Component } from 'react'

import palettes from 'components/molecules/charts/utils/palettes'
import formatUtil from 'components/molecules/charts/utils/format'
import TableChartRenderer from 'components/molecules/charts/renderers/table-chart'

class TableChart extends Component {
	constructor(props) {
		super(props)
    this.params = this.props
  }

  componentDidMount () {
    this.container = React.findDOMNode(this)
    const chart = this.getParams()
    this.table = new TableChartRenderer(chart.data, chart, this.container)
    this.table.render()
  }

  componentDidUpdate () {
    console.log('----------- Tablechart.componentDidUpdate')
    this.params = this.props
    const chart = this.getParams()
    this.table.update(chart.data, chart, this.container)
  }

  getParams () {
    const aspect = this.params.aspect || 1
    this.params.width = this.props.width || this.container.clientWidth
    this.params.height = this.props.height || this.params.width / aspect
    this.params.data = this.filterData()
    return this.params
  }

  filterData () {
    const campaign_id = this.props.selected_campaigns[0].id || this.state.campaigns.list[0].id
    return this.props.data.filter(datapoint => datapoint.campaign_id === campaign_id)
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

TableChart.defaultProps = {
  data: null,
  // Look and Feel
  cellHeight: 30,
  cellFontSize: 14,
  fontSize: 12,
  margin: {},
  colors: palettes['traffic_light'],
  // Chart
  default_sort_order: null,
  headers: null,
  parent_location_map: null,
  selected_indicators: null,
  // Defaults
  sourceColumn: d => d.short_name,
  column: d => d.indicator.short_name,
  seriesName: d => d.name,
  sortDirection: 1,
  value: d => d.value,
  values: d => d.values,
}


export default TableChart

