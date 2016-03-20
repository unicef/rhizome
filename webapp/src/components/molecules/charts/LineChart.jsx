import React, { PropTypes, Component } from 'react'

class LineChart extends Component {
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
		    	<g clasName='y axis'></g>
		    	<g clasName='x axis' transform={`translate(0, ${bg_height})`}></g>
		    	<g clasName='data'></g>
		    	<g clasName='annotation'></g>
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

