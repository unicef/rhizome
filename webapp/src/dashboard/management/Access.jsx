'use strict'

import _ from 'lodash'
import d3 from 'd3'
import React from 'react'
import moment from 'moment'

import Chart from 'component/Chart.jsx'
import DonutChart from 'component/DonutChart.jsx'
import PieChartList from 'component/PieChartList.jsx'

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

    var inaccessible = _(data.numberOfInaccessibleChildren)
      .sortBy(_.method('campaign.start_date.getTime'))
      .groupBy('indicator.short_name')
      .map(function (values) {
        return {name: '', values: values}
      })
      .value()

    var reasons = _(data.inaccessibilityBreakdown)
      .filter(d => {
        return d.campaign.id === campaign.id &&
          _.isFinite(d.value) &&
          d.value >= 0.01
      })
      .sortBy(_.property('value'))
      .reverse()
      .map(d => [d])
      .value()

    var pieChartName = function (d) {
      return d3.format('%')(d[0].value) + ' ' +
        _.trimLeft(d[0].indicator.short_name, '% ')
    }

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

    var totalNumber = 0;

    if (campaign && data.numberOfInaccessibleChildren.length > 0) {
      var year = m.format('YYYY')

      totalNumber = _.get(_.find(data.numberOfInaccessibleChildren,
        function (d) { return d.campaign.start_date.getTime() === m.valueOf() }),
        'value')
    }

    var chartOptions = {
      aspect: 2.26,
      domain: _.constant([lower.toDate(), upper.toDate()]),
      values: _.property('values'),
      x: _.property('campaign.start_date'),
      xFormat: d => moment(d).format('MMM YYYY'),
      y: _.property('value'),
      yFormat: d3.format(',.0f')
    }

    return (
      <div className='row'>
        <div className='medium-4 columns'>
          <h4><span style={{'font-weight': 'bold'}}>{totalNumber}</span><span> Children were inaccessible</span></h4>
          <Chart type='AreaChart' data={inaccessible}
                 loading={loading}
                 options={chartOptions}/>
        </div>

        <div className='accessibility medium-2 columns'>
          <h4>Inaccessibiity<br />Breakdown</h4>
          <PieChartList keyPrefix='inaccessibility-breakdown'
                        loading={loading}
                        data={reasons}
                        name={pieChartName}
                        options={{
                          domain: _.constant([0, 1]),
                          size: 24
                        }} />
        </div>

        <div className='medium-2 columns'>
          <h4>Districts with<br />
            Access Plan</h4>
          <DonutChart data={plans} label={planLabel}
                      loading={loading}
                      options={{
                        innerRadius: 0.3,
                        outerRadius: 0.5,
                        domain: _.constant([0, 1])
                      }} />
        </div>

      </div>
    )
  }
})

export default Access
