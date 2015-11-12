'use strict'

var _ = require('lodash')
var d3 = require('d3')
var React = require('react')
var moment = require('moment')

var Chart = require('component/Chart.jsx')

function getOptions (chart, campaign, data) {
  var opts = {}

  if (chart.hasOwnProperty('yFormat')) {
    opts.yFormat = _.isString(chart.yFormat) ? d3.format(chart.yFormat) : chart.xFormat
  }

  switch (chart.type) {
    case 'ScatterChart':
      opts.x = _.property('[' + chart.indicators[0] + ']')
      opts.y = _.property('[' + chart.indicators[1] + ']')

      // Only scatter charts should be providing custom formatting for
      // the x-axis
      if (chart.hasOwnProperty('xFormat')) {
        opts.xFormat = _.isString(chart.xFormat) ? d3.format(chart.xFormat) : chart.xFormat
      }
      break

    case 'ChoroplethMap':
      opts.value = _.property('.properties[' + chart.indicators[0] + ']')
      break

    case 'BarChart':
      opts.y = _.property((chart.groupBy === 'indicator')
        ? 'location.name'
        : 'indicator.short_name'
      )

      opts.xFormat = opts.yFormat
      opts.yFormat = String
      break

    case 'ColumnChart':
      var upper = moment(campaign.start_date)
      var lower = upper.clone().subtract(chart.timeRange)

      opts.domain = _.constant(_.map(d3.time.scale()
            .domain([lower.valueOf(), upper.valueOf()])
            .ticks(d3.time.month, 1),
          _.method('getTime')
        ))

      opts.x = d => moment(d.campaign.start_date).valueOf()
      opts.xFormat = d => moment(d).format('MMM YY')
      break

    case 'PieChart':
      opts.margin = {
        top: 0,
        right: 80,
        bottom: 0,
        left: 0
      }

      break

    default:
      break
  }

  return opts
}

var CustomDashboard = React.createClass({
  propTypes: {
    editable: React.PropTypes.bool,
    onAddChart: React.PropTypes.func,
    onDeleteChart: React.PropTypes.func,
    onEditChart: React.PropTypes.func,
    onMoveForward: React.PropTypes.func,
    onMoveBackward: React.PropTypes.func
  },

  getDefaultProps: function () {
    return {
      editable: false,
      onAddChart: _.noop,
      onDeleteChart: _.noop,
      onEditChart: _.noop,
      onMoveForward: _.noop,
      onMoveBackward: _.noop
    }
  },

  render: function () {
    let campaignIndex = _.indexBy(this.props.campaigns, 'id')

    var data = this.props.data
    var loading = this.props.loading
    var editable = this.props.editable

    var charts = _.map(this.props.dashboard.charts, (chart, i) => {
      var title = chart.title
      var key = _.get(chart, 'id', _.kebabCase(title))
      var id = _.get(chart, 'id', _.camelCase(title))
      var series = data[id]

      var controls
      if (editable) {
        controls = (
          <div className='button-bar' style={{float: 'right'}}>
            <span className='button-bar__edit' onClick={this.props.onMoveBackward.bind(null, i)}>
              <i className='fa fa-icon fa-arrow-left fa-fw'></i>
            </span>
            <span className='button-bar__edit' onClick={this.props.onMoveForward.bind(null, i)}>
              <i className='fa fa-icon fa-arrow-right fa-fw'></i>
            </span>
            <span className='button-bar__edit' onClick={this.props.onDeleteChart.bind(null, i)}>
              <i className='fa fa-icon fa-trash fa-fw'></i>
            </span>
            <span className='button-bar__edit' onClick={this.props.onEditChart.bind(null, i)}>
              <i className='fa fa-icon fa-pencil fa-fw'></i>
            </span>
          </div>
        )
      }

      let cols = ''
      switch(this.props.dashboard.layout) {
        case 1: // Single
          cols = 'small-12 end columns'
          break
        case 3: // Triptych
          cols = chart.type === 'BarChart'
            ? 'small-10 end columns'
            : 'medium-4 columns end cd-chart-size'
          break
        default: // Default (Basic)
          break
      }

      let campaign = chart.campaignValue ? campaignIndex[chart.campaignValue] : this.props.campaigns[0]
      var options = getOptions(chart, campaign, data)

      return (
        <div key={key} className={cols} style={{ paddingBottom: '1.5rem' }}>
          <h4>{title} {controls}</h4>
          <Chart type={chart.type} data={series} options={options}
            loading={loading} />
        </div>
      )
    })

    var addChart
    switch(this.props.dashboard.layout) {
      case 2: // Default (Basic)
        return (
          <div className='layout-basic'>
            <div className='row'>
              <div className='medium-6 columns'>
                <div className='row'>
                  <div className='medium-6 columns'>{charts[0]}</div>
                  <div className='medium-6 columns'>{charts[1]}</div>
                </div>
                <div className='row'>
                  <div className='medium-6 columns'>{charts[2]}</div>
                  <div className='medium-6 columns'>{charts[3]}</div>
                </div>
              </div>
              <div className='medium-6 columns'>
                <div>{charts[4]}</div>
              </div>
            </div>
            <div className='row'>
              <div className='medium-4 columns'>{charts[5]}</div>
              <div className='medium-4 columns'>{charts[6]}</div>
              <div className='medium-4 columns'>{charts[7]}</div>
            </div>
            {addChart}
          </div>
        )
      default: // Any others
        return (
          <div className='row cd-charts'>
            {charts}
            {addChart}
          </div>
        )
    }
  }
})

module.exports = CustomDashboard
