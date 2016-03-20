import React, { PropTypes, Component } from 'react'

class TableChart extends Component {
	render () {
		const props = this.props
		const margin = props.margin
   	const viewBox = '0 0 ' + props.width + ' ' + props.height

		return (
			<svg className='heatmap sortable' viewBox={viewBox} width={props.width} height={props.height}>
		    <g className='margin' transform={`translate(-75, ${margin.top})`}>
		    	<g clasName='z axis'></g>
		    	<g clasName='y axis'></g>
		    	<g clasName='x axis'></g>
		    	<g clasName='data'></g>
		    	<g clasName='source-footer'></g>
		    	<g clasName='legend'></g>
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

