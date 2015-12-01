import _ from 'lodash'
import d3 from 'd3'
import moment from 'moment'

import React from 'react'
import Carousel from 'nuka-carousel'
import HomepageCarouselDecorators from './HomepageCarouselDecorators.jsx'

import Chart from 'component/Chart.jsx'
import YTDChart from 'component/YTDChart.jsx'

import ChartUtil from '../utils/ChartUtil.js'

var HomepageCharts = React.createClass({
  propTypes: {
    campaign: React.PropTypes.object.isRequired,
    data: React.PropTypes.object,
    loading: React.PropTypes.bool,
    location: React.PropTypes.string,
    mapLoading: React.PropTypes.bool
  },

  getDefaultProps: function () {
    return {
      data: [],
      loading: false,
      mapLoading: true
    }
  },

  getInitialState: function () {
    return {
      charts: []
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

    var width = 390
    var height = 0.87 * width

    var buildMapChart = function (loading) {
      return <div>
          <h4 className='chart-title'>Missed children, {missedChildrenData.location}</h4>
          <Chart type='ChoroplethMap'
                 data={missedChildrenData.missedChildrenMap}
                 loading={loading}
                 options={{
                   domain: _.constant([0, 0.1]),
                   value: _.property('properties[475]'),
                   xFormat: d3.format('%'),
                   width: width,
                   height: height,
                   homepage: true
                 }}/>
          <h4 className='chart__title--date'>Latest date: {missedChildrenData.date}</h4>
           </div>
    }

    if (!this.state.charts.length) {
      var charts = []

      charts.push({
        isMap: false,
        value: (<div id='polio-cases-ytd'>
          {polioCasesData.title}
          {polioCasesData.newCaseLabel}
          <div style={{ position: 'relative' }}>
            <YTDChart
              data={polioCasesData.data}
              loading={loading}
              options={{
                aspect: 1,
                width: width,
                height: height
              }}/>
          </div>
          <h4 className='chart__title--date'>Latest date: {polioCasesData.date}</h4>
        </div>)
      })

      charts.push({
        isMap: true,
        value: buildMapChart(this.props.mapLoading)
      })

      charts.push({
        isMap: false,
        value: (<div>
          <h4 className='chart-title'>Missed children, trend</h4>
          <Chart type='AreaChart' data={missedChildrenData.missed}
                 loading={loading}
                 options={{
                   aspect: 1,
                   domain: _.constant(missedChildrenData.missedScale),
                   x: d => moment(d.campaign.start_date).startOf('month').valueOf(),
                   xFormat: d => moment(d).format('MMM YYYY'),
                   yFormat: d3.format(',.1%'),
                   range: missedChildrenData.range,
                   width: width,
                   height: height,
                   total: true
                 }}/>
          <h4 className='chart__title--date'>Latest date: {missedChildrenData.date}</h4>
               </div>)
      })

      charts.push({
        isMap: false,
        value: (
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
                     range: underImmunizedData.range,
                     rejectId: 433,
                     processData: true,
                     width: width,
                     height: height
                   }}/>
            <h4 className='chart__title--date'>Latest date: {underImmunizedData.date}</h4>
          </div>)
      })

      this.state.charts = _.shuffle(charts)
    }

    if (!this.props.mapLoading) {
      this.state.charts.forEach(item => {
        if (item.isMap) {
          item.value = buildMapChart(this.props.mapLoading)
        }
      })
    }

    return this.state.charts.map(item => item.value)
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

export default HomepageCharts
