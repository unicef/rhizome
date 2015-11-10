'use strict'

var _ = require('lodash')
var d3 = require('d3')
var React = require('react')
var moment = require('moment')

var Chart = require('component/Chart.jsx')
var DonutChart = require('component/DonutChart.jsx')
var PieChartList = require('component/PieChartList.jsx')

var Access = React.createClass({
  propTypes: {
    campaign: React.PropTypes.object.isRequired,
    indicators: React.PropTypes.object.isRequired,
    data: React.PropTypes.object
  },

  render: function () {
    var data = this.props.data
    var campaign = this.props.campaign
    var loading = this.props.loading

    var inaccessible = _(data.numberOfInaccessibleChildren)
      .sortBy(_.method('campaign.start_date.getTime'))
      .groupBy('indicator.short_name')
      .map(function (values, name) {
        return {name: name, values: values}
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

    var chartOptions = {
      aspect: 2.26,
      domain: _.constant([lower.toDate(), upper.toDate()]),
      values: _.property('values'),
      x: _.property('campaign.start_date'),
      y: _.property('value'),
      yFormat: d3.format(',.0f')
    }

    return (
      <div className='row'>
        <div className='medium-4 columns'>
          <h4>Number of Inaccessible Children</h4>
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

module.exports = Access
