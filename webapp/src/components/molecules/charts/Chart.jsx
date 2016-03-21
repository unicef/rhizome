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
		console.log('------------------------------ Chart.jsx - render ------------------------------')
		let chart
		const props = this.props
		if (this.container) {
			const options = props.options
			const margin = options.margin
	   	const aspect = options['aspect'] || 1
		 	this.width =  options['width'] || this.container.clientWidth
	 		this.height = options['height'] || this.width / aspect
	   	const viewBox = '0 0 ' + this.width + ' ' + this._height
	 	 	const h = this.height - margin.top - margin.bottom
	 	 	const w = this.width - margin.left - margin.right
		  const chart_props = {
		  	data: props.data,
		  	options: props.options,
		  	domain: options.domain,
		  	data_format: options.data_format,
		  	colors: options.color,
		  	margin: margin,
		  	height: this.height,
		  	width: this.width
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

