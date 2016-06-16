import React from 'react'

const PercentCell = ({cellParams}) => {
	const params = cellParams.params
	const datapoint = cellParams.datapoint
  return <span>{datapoint.value}</span>
}


export default PercentCell