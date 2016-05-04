import _ from 'lodash'
import React from 'react'

import HighChart from 'components/molecules/highcharts/HighChart'
import format from 'utilities/format'

class ColumnChart extends HighChart {

  setConfig = function () {
    const first_indicator = this.props.selected_indicators[0]
    const first_location = this.props.selected_locations[0]
    const last_indicator = this.props.selected_indicators[this.props.selected_indicators.length-1]
    const props = this.props
    this.config = {
      xAxis: {
        type: 'datetime',
        labels: {
          format: '{value:%b %Y}'
        }
      },
      yAxis: [
        {
          title: { text: '' },
          labels: {
            formatter: function () {
              return format.autoFormat(this.value, first_indicator.data_format)
            }
          }
        },
        {
          title: { text: '' },
          labels: {
            formatter: function () {
              return format.autoFormat(this.value, last_indicator.data_format)
            }
          },
          opposite: true
        },
      ],
      tooltip: {
        xDateFormat: '%b %Y',
        pointFormatter: function () {
          const data_format = this.series.name === last_indicator.name ? last_indicator.data_format : first_indicator.data_format
          const value = format.autoFormat(this.y, data_format, 1)
          const secondary_text = props.groupBy === 'indicator' ? first_location.name : first_indicator.name
          return `<b>${secondary_text}</b><br/>${this.series.name}: <b>${value}</b><br/>`
        }
      },
      series: this.setSeries()
    }
  }

  setSeries = function () {
    const multiIndicator = this.props.selected_indicators.length > 1
    const groupByIndicator = this.props.groupBy === 'indicator'
    const last_indicator = this.props.selected_indicators[this.props.selected_indicators.length-1]
    const data = this.props.datapoints.melted
    const grouped_data = groupByIndicator ? _.groupBy(data, 'indicator.id') : _.groupBy(data, 'location.id')
    const series = []

    // Set column data for all indicators except the last one
    // In the case of a multi-indicator chart, the last indicator is displayed as a line
    _.forEach(grouped_data, (group_collection, key) => {
      if (!multiIndicator || parseInt(last_indicator.id) !== parseInt(key)) {
        const sorted_column_data = _.sortBy(group_collection, group => group.campaign.start_date.getTime())
        const color = this.props.indicator_colors[sorted_column_data[0].indicator.id]
        series.push({
          name: groupByIndicator ? sorted_column_data[0].indicator.name : sorted_column_data[0].location.name,
          color: color,
          type: 'column',
          data: sorted_column_data.map(datapoint => [datapoint.campaign.start_date.getTime(), datapoint.value])
        })
      }
    })

    // Set the line data for the last indicator
    if (multiIndicator) {
      const sorted_line_data = _.sortBy(grouped_data[last_indicator.id], group => group.campaign.start_date.getTime())
      const color = this.props.indicator_colors[last_indicator.id]
      series.push({
        yAxis: 1,
        name: last_indicator.name,
        color: color,
        type: 'spline',
        data: sorted_line_data.map(datapoint => [datapoint.campaign.start_date.getTime(), datapoint.value])
      })
    }
    console.log('series', series)
    return series
  }
}

export default ColumnChart
