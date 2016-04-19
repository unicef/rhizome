import _ from 'lodash'
import React from 'react'

import HighChart from 'components/molecules/highcharts/HighChart'
import format from 'utilities/format'

class ColumnChart extends HighChart {

  setConfig = function () {
    const first_indicator = this.props.selected_indicators[0]
    const first_location = this.props.selected_locations[0]
    const props = this.props
    this.config = {
      chart: { type: 'column' },
      xAxis: {
        type: 'datetime',
        labels: {
          format: '{value:%b %Y}'
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
        xDateFormat: '%b %Y',
        pointFormatter: function (point) {
          const value = format.autoFormat(this.y, first_indicator.data_format)
          const secondary_text = props.groupBy === 'indicator' ? first_location.name : first_indicator.name
          return `<b>${secondary_text}</b><br/>${this.series.name}: <b>${value}</b><br/>`
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
      group_collection = _.sortBy(group_collection, group => group.campaign.start_date.getTime())
      series.push({
        name: groupByIndicator ? group_collection[0].indicator.name : group_collection[0].location.name,
        data: group_collection.map(datapoint => [datapoint.campaign.start_date.getTime(), datapoint.value])
      })
    })
    return series
  }
}

export default ColumnChart
