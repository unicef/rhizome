import _ from 'lodash'
import React from 'react'

import HighChart from 'components/molecules/highcharts/HighChart'
import format from 'utilities/format'

class LineChart extends HighChart {

  setConfig = function () {
    const first_indicator = this.props.selected_indicators[0]
    this.config = {
      chart: { type: 'line' },
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
        xDateFormat: '%b %d',
        pointFormatter: function (point) {
          const value = format.autoFormat(this.y, first_indicator.data_format)
          return `${this.series.name}: <b>${value}</b><br/>`
        }
      },
      series: this.setSeries()
    }
  }

  setSeries = function () {
    const data = this.props.datapoints.melted
    const groupByIndicator = this.props.groupBy === 'indicator'
    const grouped_data = groupByIndicator ? _.groupBy(data, 'indicator.id') : _.groupBy(data, 'location.id')
    const series = []
    _.forEach(grouped_data, group_collection => {
      group_collection = _.sortBy(group_collection, group => { return group.campaign.start_date.getTime() })
      series.push({
        name: groupByIndicator ? group_collection[0].indicator.name : group_collection[0].location.name,
        data: group_collection.map(datapoint => { return [datapoint.campaign.start_date.getTime(), datapoint.value] })
      })
    })
    return series
  }
}

export default LineChart
