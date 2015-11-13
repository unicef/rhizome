'use strict'

var _ = require('lodash')
var d3 = require('d3')
var moment = require('moment')
var React = require('react')

var Chart = require('component/Chart.jsx')
var PieChartList = require('component/PieChartList.jsx')

var DashboardActions = require('actions/DashboardActions')

var series = function (values, name) {
  return {
    name: name,
    values: _.sortBy(values, _.result('campaign.start_date.getTime'))
  }
}

var indicatorForCampaign = function (campaign, indicator) {
  return d => d.campaign.id === campaign && d.indicator.id === indicator
}

var Performance = React.createClass({
  propTypes: {
    campaign: React.PropTypes.object.isRequired,
    data: React.PropTypes.object,
    loading: React.PropTypes.bool,
    location: React.PropTypes.string
  },

  getDefaultProps: function () {
    return {
      data: [],
      loading: false
    }
  },

  generateMissedChildrenChartData: function (originalData) {
    var stack = d3.layout.stack()
      .order('default')
      .offset('zero')
      .values(_.property('values'))
      .x(_.property('campaign.start_date'))
      .y(_.property('value'))

    var missed
    try {
      missed = _(originalData)
        .groupBy('indicator.short_name')
        .map(series)
        .thru(stack)
        .value()
    } catch (err) {
      console.error(err)
      console.log(`Data error in ${originalData}`)
      missed = []
    }

    return missed
  },

  render: function () {
    var data = this.props.data
    var campaign = this.props.campaign
    var upper = moment(campaign.start_date, 'YYYY-MM-DD')
    var lower = upper.clone().startOf('month').subtract(1, 'year')
    var loading = this.props.loading
    var location = this.props.location
    var colors = ['#377EA4', '#B6D0D4']

    var missed = this.generateMissedChildrenChartData(data.missedChildren)

    var sortedConversions = _.sortBy(data.conversions, 'campaign.start_date')
    var conversions = _(sortedConversions)
      .groupBy('indicator.short_name')
      .map(series)
      .value()

    var vaccinated = _.get(_.find(data.transitPoints, indicatorForCampaign(campaign.id, 177)), 'value')

    if (!_.isUndefined(vaccinated) && !_.isNull(vaccinated)) {
      var num = d3.format('n')

      vaccinated = (
        <p><strong>{num(vaccinated)}</strong> children vaccinated at transit points.</p>
      )
    } else {
      vaccinated = (<p>No vaccination data.</p>)
    }

    var planned = _.get(_.find(data.transitPoints, indicatorForCampaign(campaign.id, 204)), 'value')
    var inPlace = _.get(_.find(data.transitPoints, indicatorForCampaign(campaign.id, 175)), 'value')
    var withSM = _.get(_.find(data.transitPoints, indicatorForCampaign(campaign.id, 176)), 'value')

    var transitPoints = []
    if ((!_.any([inPlace, planned], _.isUndefined)) && (!_.any([inPlace, planned], _.isNull))) {
      transitPoints.push([{
        title: inPlace + ' / ' + planned + ' in place',
        value: inPlace / planned
      }])
    }

    if ((!_.any([withSM, inPlace], _.isUndefined)) && (!_.any([withSM, inPlace], _.isNull))) {
      transitPoints.push([{
        title: withSM + ' / ' + inPlace + ' have a social mobilizer',
        value: withSM / inPlace
      }])
    }

    var pct = d3.format('%')

    var missedChildrenMap = data.missedChildrenByProvince

    var maxVaccinatedChildren = 5000

    var maxRadius = 20

    var radius = d3.scale.sqrt()
      .domain([0, maxVaccinatedChildren])
      .range([0, maxRadius])

    function _chooseRadius (v) {
      if (v > maxVaccinatedChildren) {
        return maxRadius
      } else {
        return radius(v)
      }
    }

    return (
      <div>
        <div className='medium-6 columns'>
          <h3>Performance of Front Line Workers</h3>
        </div>

        <div className='medium-2 columns'>
          <section>
            <h4>Missed Children</h4>
            <Chart type='AreaChart' data={missed}
                   loading={loading}
                   options={{
                     aspect: 2.26,
                     domain: _.constant([lower.valueOf(), upper.valueOf()]),
                     x: d => moment(d.campaign.start_date).startOf('month').valueOf(),
                     xFormat: d => moment(d).format('MMM YYYY'),
                     yFormat: d3.format(',.1%')
                   }}/>
          </section>

          <section>
            <h4>Conversions</h4>
            <Chart type='LineChart'
              data={conversions}
              loading={loading}
              options={{
                aspect: 2.26,
                domain: _.constant([lower.toDate(), upper.toDate()]),
                range: _.constant([0, 1]),
                x: d => moment(d.campaign.start_date).startOf('month').valueOf(),
                xFormat: d => moment(d).format('MMM YYYY'),
                yFormat: pct
              }}/>
          </section>
        </div>

        <section className='medium-3 columns'>
          <h4>{location}, country overview</h4>
          <Chart type='ChoroplethMap'
            data={missedChildrenMap}
            loading={loading}
            options={{
              aspect: 0.555,
              domain: _.constant([0, 0.1]),
              value: _.property('properties[475]'),
              bubblesValue: _.property('properties[177]'),
              stripesValue: _.property('properties[203]'),
              yFormat: pct,
              radius: _.partial(_chooseRadius, _),
              onClick: d => { DashboardActions.navigate({ location: d }) }
            }}/>
        </section>

        <section className='transit-points medium-1 column'>
          <h4 className='font-bold'>Missed Children</h4>
          <h4>Transit Points</h4>

          {vaccinated}

          <PieChartList
            loading={loading}
            keyPrefix='transit-points'
            name={_.property('[0].title')}
            data={transitPoints}
            options={{
              domain: _.constant([0, 1]),
              size: 24,
              palette: colors
            }}
            emptyText='No transit point data available'/>
        </section>
      </div>
    )
  }
})

module.exports = Performance
