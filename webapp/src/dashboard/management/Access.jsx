import _ from 'lodash'
import d3 from 'd3'
import React from 'react'
import moment from 'moment'

import Chart from 'component/Chart.jsx'

var Access = React.createClass({
  propTypes: {
    campaign: React.PropTypes.object.isRequired,
    indicators: React.PropTypes.object.isRequired,
    data: React.PropTypes.object,
    loading: React.PropTypes.bool
  },

  render: function () {
    var data = this.props.data
    var campaign = this.props.campaign
    var loading = this.props.loading

    var reasons = _(data.inaccessibilityBreakdown)
      .filter(d => {
        return d.campaign.id === campaign.id && _.isFinite(d.value) && d.value >= 0.01
      })

    var plans = _.filter(data.districtsWithAccessPlans,
        d => d.campaign.id === campaign.id && _.isFinite(d.value))

    var planLabel = function (d) {
      var fmt = d3.format('%')
      var v = _.get(d, '[0].value', '')

      return fmt(v)
    }

    var m = moment(this.props.campaign.start_date, 'YYYY-MM-DD')
    var lower = m.clone().startOf('month').subtract(1, 'year')
    var upper = m.clone().endOf('month')

    let totalNumber

    if (campaign && data.numberOfInaccessibleChildren.length > 0) {
      totalNumber = _.get(_.find(data.numberOfInaccessibleChildren,
        function (d) { return d.campaign.start_date.getTime() === m.valueOf() }),
        'value')
    }

    var labelText
    if (totalNumber) {
      labelText = (<h4><span style={{ fontWeight: 'bold' }}>{totalNumber}</span> Children were inaccessible</h4>)
    } else {
      labelText = (<h4>No data for current campaign</h4>)
    }

    var chartOptions = {
      aspect: 2.26,
      domain: _.constant([lower.toDate(), upper.toDate()]),
      values: _.property('values'),
      x: _.property('campaign.start_date'),
      xFormat: d => moment(d).format('MMM YYYY'),
      y: _.property('value'),
      yFormat: d3.format(',.0f'),
      withoutSeriesName: true
    }

    return (
      <div className='row'>
        <div className='medium-4 columns'>
          {labelText}
          <Chart type='AreaChart' data={data.numberOfInaccessibleChildren}
                 loading={loading}
                 options={chartOptions}/>
        </div>

        <div className='medium-2 columns'>
          <h4>Inaccessibiity<br />Breakdown</h4>
          <Chart type='ColumnChart'
                        loading={loading}
                        data={reasons}
                        options={{
                          aspect: 1,
                          domain: _.constant([0, 1]),
                          values: _.property('values'),
                          y0: _.property('y0'),
                          yFormat: d3.format('%'),
                          processData: true
                        }} />
        </div>

        <div className='medium-2 columns'>
          <h4>Districts with<br />
            Access Plan</h4>
          <Chart type='PieChart' data={plans}
                      loading={loading}
                      options={{
                        innerRadius: 0.3,
                        outerRadius: 0.5,
                        domain: _.constant([0, 1]),
                        percentage: planLabel(plans),
                        name: (d, i) => { return i },
                        color: ['#377EA4', '#B6D0D4']
                      }} />
        </div>

      </div>
    )
  }
})

export default Access
