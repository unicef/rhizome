import React, { Component } from 'react'
import TableChart from 'components/molecules/charts/TableChart'
import LineChart from 'components/molecules/charts/LineChart'
import ChoroplethMap from 'components/molecules/charts/ChoroplethMap'

class ChartContainer extends Component {

	componentDidMount() {
		this.container = React.findDOMNode(this)
	}

	renderChart(type, chart_props) {
	  if (type === 'TableChart') {
	  	return <TableChart {...chart_props} />
	  } else if (type === 'LineChart') {
	  	return <LineChart {...chart_props} />
	  } else if (type === 'ChoroplethMap') {
	  	return <ChoroplethMap {...chart_props} />
	  }
	}

	render () {
		let chart
		const props = this.props
		if (this.container) {
			const options = props.options
			const margin = options.margin
	   	const aspect = options['aspect'] || 1
		 	this._width =  options['width'] || this.container.clientWidth
	 		this._height = options['height'], this._width / aspect
	   	const viewBox = '0 0 ' + this._width + ' ' + this._height
	 	 	const h = this._height - margin.top - margin.bottom
	 	 	const w = this._width - margin.left - margin.right

		  const chart_props = {
		  	data: props.data,
		  	options: props.options,
		  	domain: options.domain,
		  	data_format: options.data_format,
		  	colors: options.color,
		  	margin: margin,
		  	height: 300,
		  	width: 300
		  }
		  chart = this.renderChart(props.type, chart_props)
		}

		return (
			<div className='chart-container'>
				{ chart }
			</div>
		)
	}
}

export default ChartContainer

