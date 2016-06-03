import React from 'react'
import IndicatorDetailContainer from 'containers/IndicatorDetailContainer'

const IndicatorPage = ({ params }) => {
	return (
  	<div>
  		<h1>Indicator Page</h1>
  		<IndicatorDetailContainer indicator_id={params.indicator_id}/>
  	</div>
	)
}

export default IndicatorPage
