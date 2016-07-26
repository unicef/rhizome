import _ from 'lodash'
import React from 'react'

import HighChart from 'components/highchart/HighChart'
import format from 'utilities/format'

class LineChart extends HighChart {

  setConfig = function () {
    const first_indicator = this.props.selected_indicators[0]
    this.config = {
      chart: { type: 'line' },
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
      plotOptions: {
        line: {
          dataLabels: {
            enabled: true,
            backgroundColor: 'rgba(249, 249, 249, 0.85098)',
            borderRadius: '2',
            borderWidth: '1',
            borderColor: 'rgb(124, 181, 236)',
            padding: 7,
            y: -6,
            formatter: function () {
              return format.autoFormat(this.y, first_indicator.data_format, 1)
            }
          },
          enableMouseTracking: false
        }
      },
      tooltip: {
        xDateFormat: '%b %Y',
        pointFormatter: function (point) {
          const value = format.autoFormat(this.y, first_indicator.data_format, 1)
          return `${this.series.name}: <b>${value}</b><br/>`
        }
      },
      exporting: {
        buttons: {
          customButton: {
            text: 'Labels',
            onclick: this._toggleLabels,
            x: -65,
            y: -30,
            theme: {
              style: {
                color: '#039',
                textDecoration: 'underline'
              }
            }
          }
        }
      },
      legend: {
        itemStyle: {
          fontSize: '14px'
        },
      },
      series: this.setSeries()
    }
  }

  setSeries = function () {
    const data = this.props.datapoints.flattened
    const groupByIndicator = this.props.groupBy === 'indicator'
    const grouped_data = groupByIndicator ? _.groupBy(data, 'indicator.id') : _.groupBy(data, 'location.id')
    const series = []
    _.forEach(grouped_data, group_collection => {
      group_collection = _.sortBy(group_collection, group => group.campaign.start_date.getTime())
      const first_datapoint = group_collection[0]
      const color = this.props.indicator_colors[first_datapoint.indicator.id]
      series.push({
        name: groupByIndicator ? group_collection[0].indicator.name : group_collection[0].location.name,
        color: color,
        data: group_collection.map(datapoint => [datapoint.campaign.start_date.getTime(), datapoint.value])
      })
    })
    return series
  }

  _toggleLabels = () => {
    const self = this
    var opt = this.chart.series[0].options;
    opt.dataLabels.enabled = !opt.dataLabels.enabled
    opt.enableMouseTracking = !opt.enableMouseTracking
    opt.animation.duration = 500
    this.chart.series[0].update(opt);
  }
}

export default LineChart
