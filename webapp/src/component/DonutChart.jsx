'use strict'

import _ from 'lodash'
import React from 'react'

import Chart from 'component/Chart.jsx'

var DonutChart = React.createClass({
  propTypes: {
    data: React.PropTypes.array.isRequired,
    options: React.PropTypes.object,
    label: React.PropTypes.func,
    labelStyle: React.PropTypes.object
  },

  getDefaultProps: function () {
    return {
      label: _.noop,
      labelStyle: {},
      loading: false
    }
  },

  render: function () {
    var props = _.omit(this.props, 'label', 'labelStyle')
    var labelText = this.props.label(this.props.data)
    var label
    var labelStyle = ''

    // if (this.props.options.pieType) {
    //  labelStyle = 'label__value'
    // }

    if (!_.isEmpty(labelText) && labelText !== '0%') {
      label = (<p className={'donut-label ' + labelStyle} style={this.props.labelStyle}>{labelText}</p>)
    }

    return (
      <div className='labeled-donut'>
        <Chart type='PieChart' {...props} />
        {label}
      </div>
    )
  }
})

export default DonutChart
