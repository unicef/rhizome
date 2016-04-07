import _ from 'lodash'
import React, { Component, PropTypes } from 'react'
import format from 'utilities/format'
import palettes from 'utilities/palettes'

import ChartFactory from 'components/molecules/highcharts/ChartFactory'

class HighChart extends Component {

  constructor (props) {
    super(props)
    const first_indicator = props.selected_indicators[0]
    this.data = {
      chart: { type: this.getChartType(props.type) },
      xAxis: {
        type: 'datetime',
        labels: {
          format: '{value:%b %d, %Y}'
        }
      },
      yAxis: {
        title: { text: '' },
        labels: {
          formatter: function () {
            return format.autoFormat(this.value, first_indicator.data_format)
          }
        }
      },
      tooltip: {
         pointFormatter: function (point) {
          const value = format.autoFormat(this.y, first_indicator.data_format)
          return `${this.series.name}: <b>${value}</b><br/>`
        }
      }
    }
  }

  getChartType (type) {
    if (type === 'ColumnChart') { return 'column' }
    if (type === 'LineChart') { return 'line' }
    if (type === 'BarChart') { return 'bar' }
  }

  getData () {
    const data = this.props.data
    const groupByIndicator = this.props.groupBy === 'indicator'
    const grouped_data = groupByIndicator ? _.groupBy(data, 'indicator.id') : _.groupBy(data, 'location.id')
    const series = []
    _.forEach(grouped_data, group => {
      _.sortBy(group, _.method('campaign.start_date.getTime'))
      series.push({
        name: groupByIndicator ? group[0].indicator.name : group[0].location.name,
        data: group.map(datapoint => datapoint.value) // Needs to be sorted by date
      })
    })
    return series
  }

  render () { console.info('------ HighChart.render')
    this.data.colors = palettes[this.props.palette]
    this.data.series = this.getData()
    return (
      <div id='highchart-container'>
        <ChartFactory config={this.data} map={this.props.type === 'MapChart'} isPureConfig/>
      </div>
    )
  }
}

export default HighChart

