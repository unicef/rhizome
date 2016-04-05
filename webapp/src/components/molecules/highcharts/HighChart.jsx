import _ from 'lodash'
import Highcharts from 'react-highcharts/dist/bundle/highcharts'
import React, { Component, PropTypes } from 'react'
import format from 'utilities/format'


import LineChartRenderer from 'components/molecules/highcharts/renderers/line-chart'

class HighChart extends Component {

  static propTypes = {
    chart: PropTypes.object,
    colors: PropTypes.array,
    credits: PropTypes.object,
    data: PropTypes.object,
    drilldown: PropTypes.object,
    exporting: PropTypes.object,
    labels: PropTypes.object,
    legend: PropTypes.object,
    loading: PropTypes.object,
    navigation: PropTypes.object,
    noData: PropTypes.object,
    pane: PropTypes.object,
    plotOptions: PropTypes.object,
    series: PropTypes.arrayOf(PropTypes.object),
    subtitle: PropTypes.object,
    title: PropTypes.object,
    tooltip: PropTypes.object,
    xAxis: PropTypes.object,
    yAxis: PropTypes.object
  }

  constructor (props) {
    super(props)
    const first_indicator = props.selected_indicators[0]
    this.data = {
      chart: { type: this.getChartType(props.type) },
      credits: { enabled: false },
      title: '',
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
      series: [{
        name: first_indicator.name,
        data: props.data.map(datapoint => [datapoint.campaign.start_date.getTime(), datapoint.value]),
      }],
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

  render () { console.info('------ HighChart.render')
    return (
      <div id='highchart-container'>
        <Highcharts config={this.data} />
      </div>
    )
  }
}

export default HighChart

