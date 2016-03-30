import _ from 'lodash'
import React, { PropTypes } from 'react'


const ChartTypeSelector = React.createClass({
  render () {
    return (
      <div style={{ fontSize: '1px' }}>
        <i className='fa fa-table' />
        <i className='fa fa-th' />
        <i className='fa fa-map' />
        <i className='fa fa-line-chart' />
        <i className='fa fa-bar-chart' />
      </div>
    )
  }
})

export default ChartTypeSelector
