import React from 'react'
import MultiChartContainer from 'containers/MultiChartContainer'

const ChartPage = ({params}) => {
	return (
  	<div>
  		<h1>Chart Page</h1>
  		<MultiChartContainer chart_id={params.chart_id} />
  	</div>
	)
}

export default ChartPage