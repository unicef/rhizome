'use strict'

var _ = require('lodash')
var d3 = require('d3')
var moment = require('moment')

var React = require('react')
var Carousel = require('nuka-carousel')
var HomepageCarouselDecorators = require('./HomepageCarouselDecorators.jsx')

var Chart = require('component/Chart.jsx')
var YtDChart = require('component/YtDChart.jsx')

var ChartUtil = require('../utils/ChartUtil.js')

var HomepageCharts = React.createClass({
  propTypes: {
    campaign: React.PropTypes.object.isRequired,
    data: React.PropTypes.object,
    loading: React.PropTypes.bool
  },

  getDefaultProps: function () {
    return {
      data: [],
      loading: false
    }
  },

  prepareChartsData: function () {
    var loading = this.props.loading

    var missedChildrenData = ChartUtil.prepareMissedChildrenData({
      data: this.props.data.performance,
      campaign: this.props.campaign,
      location: this.props.location
    })

    var underImmunizedData = ChartUtil.prepareUnderImmunizedData({
      data: this.props.data.impact.underImmunizedChildren,
      campaign: this.props.campaign
    })

    var polioCasesData = ChartUtil.preparePolioCasesData({
      data: this.props.data.impact.polioCasesYtd,
      campaign: this.props.campaign
    })

    var charts = []

    charts.push(
      <div id='polio-cases-ytd'>
        {polioCasesData.title}
        <div style={{ position: 'relative' }}>
          {polioCasesData.newCaseLabel}
          <YtDChart
            data={polioCasesData.data}
            loading={loading}
            options={{
              color: _.flow(_.property('name'), polioCasesData.colors),
              aspect: 1,
              width: 390,
              height: 390
            }} />
          </div>
        </div>
    )

    charts.push(
      <div>
        <h4 className='chart-title'>Missed children, {missedChildrenData.location}</h4>
        <Chart type='ChoroplethMap'
        data={missedChildrenData.missedChildrenMap}
        loading={loading}
        options={{
          domain: _.constant([0, 0.1]),
          value: _.property('properties[475]'),
          yFormat: d3.format('%'),
          width: 390,
          height: 390
        }}
      />
      </div>
      )

    charts.push(
      <div>
        <h4 className='chart-title'>Missed children, trend</h4>
        <Chart type='AreaChart' data={missedChildrenData.missed}
          loading={loading}
          options={{
            aspect: 1,
            domain: _.constant(missedChildrenData.missedScale),
            x: d => moment(d.campaign.start_date).startOf('month').valueOf(),
            xFormat: d => moment(d).format('MMM YYYY'),
            yFormat: d3.format(',.1%'),
            width: 390,
            height: 390
          }}
        />
      </div>)

    charts.push(
      <div>
        <h4 className='chart-title'>Under Immunized Children</h4>
        <Chart type='ColumnChart'
          data={underImmunizedData.data}
          loading={loading}
          options={{
            aspect: 1,
            color: underImmunizedData.color,
            domain: _.constant(underImmunizedData.immunityScale),
            values: _.property('values'),
            x: function (d) { return moment(d.campaign.start_date).startOf('quarter').valueOf() },
            xFormat: function (d) { return moment(d).format('[Q]Q [ ]YYYY') },
            y0: _.property('y0'),
            yFormat: d3.format('%'),
            width: 390,
            height: 390
          }}
        />
      </div>)

    return _.shuffle(charts)
  },

  render: function () {
    var list = this.prepareChartsData()

    return (
      <Carousel decorators={HomepageCarouselDecorators}>
          {list}
      </Carousel>
    )
  }
})

module.exports = HomepageCharts
