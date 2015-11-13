'use strict'

import _ from 'lodash'
import d3 from 'd3'
import React from 'react'

import Chart from 'component/Chart.jsx'
import Monitoring from 'dashboard/nco/Monitoring.jsx'

// function donutLabel (data, labelText) { // FIXME this is repeated in odk/overview
//   var value = _.get(data, '[0].value')

//   if (!_.isFinite(value)) {
//     return
//   }

//   var fmt = d3.format('%')
//   var label

//   if (labelText) {
//     label = (<span><br /><label>{labelText}</label></span>)
//   }

//   return (<span>{fmt(value)}{label}</span>)
// }

var Overview = React.createClass({
  propTypes: {
    data: React.PropTypes.object.isRequired,
    loading: React.PropTypes.bool
  },

  getDefaultProps: function () {
    return {
      loading: false
    }
  },

  render: function () {
    var loading = this.props.loading
    var data = this.props.data
    var monitoring = _.pick(data, 'inside', 'outside', 'caregiverAwareness',
      'insideMonitoring', 'outsideMonitoring')

    var options = {
      values: _.identity,
      x: _.property('value'),
      xFormat: d3.format('%'),
      y: _.property('indicator.short_name')
    }

    var headerStyle = {
      marginLeft: '80px'
    }

    return (
      <div>
        <div className='row'>
          <div className='medium-6 columns'>
            <Monitoring data={monitoring} loading={loading} />
          </div>

          <div className='medium-3 columns'>
            <h4 style={headerStyle}><a href='#influencers'>Influencers</a></h4>
            <Chart
              type='BarChart'
              options={options}
              loading={loading}
              data={[data.influencers]} />
          </div>

          <div className='medium-3 columns'>
            <h4 style={headerStyle}><a href='#sources-of-information'>Information Sources</a></h4>
            <Chart
              type='BarChart'
              options={options}
              loading={loading}
              data={[data.informationSource]} />
          </div>
        </div>

        <div className='row'>
          <div className='medium-3 columns'>
            <h4 style={headerStyle}><a href='#missed-children'>Reason for Missed</a></h4>
            <Chart
              type='BarChart'
              options={options}
              loading={loading}
              data={[data.reasonForMissed]} />
          </div>

          <div className='medium-3 columns'>
            <h4 style={headerStyle}><a href='#absences'>Reason for Absesnce</a></h4>
            <Chart
              type='BarChart'
              options={options}
              loading={loading}
              data={[data.reasonForAbsence]} />
          </div>

          <div className='medium-3 columns'>
            <h4 style={headerStyle}><a href='#non-compliance' title='Reason for Non-Compliance'>Reason for N.C.</a></h4>
            <Chart
              type='BarChart'
              options={options}
              loading={loading}
              data={[data.reasonForNonCompliance]} />
          </div>

          <div className='medium-3 columns'>
            <h4 style={headerStyle}><a href='#resolutions'title='Non-Compliance Resolved by'>N.C. Resolved by</a></h4>
            <Chart
              type='BarChart'
              options={options}
              loading={loading}
              data={[data.ncResolvedBy]} />
          </div>
        </div>
      </div>
    )
  }
})

module.exports = Overview
