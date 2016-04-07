import React from 'react'

import HighChart from 'components/molecules/highcharts/HighChart'

import format from 'utilities/format'

class ColumnChart extends HighChart {
  constructor (props) {
    super(props)
    const first_indicator = props.selected_indicators[0]
    this.data = {
      chart: { type: 'column' },
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
}

export default ColumnChart
