import _ from 'lodash'
import React from 'react'

import HighChart from 'components/molecules/highcharts/HighChart'
import format from 'utilities/format'

class StackedColumnChart extends HighChart {

  setConfig = function () {
    const props = this.props
    const first_indicator = props.selected_indicators[0]
    const locations = props.datapoints.raw.map(datapoint => props.locations_index[datapoint.location])

    this.config = {
      chart: { type: 'column' },
      xAxis: {
        categories: locations.map(location => location.name)
      },
      yAxis: {
        title: { text: '' }
      },
      plotOptions: {
        column: { stacking: 'normal' }
      },
      tooltip: {
        xDateFormat: '%b %Y',
        pointFormatter: function (point) {
          const value = format.autoFormat(this.y, first_indicator.data_format)
          return `<b>${this.series.name}</b><br/>${this.category}: <b>${value}</b><br/>`
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
      series.push({
        name: groupByIndicator ? group_collection[0].indicator.name : group_collection[0].location.name,
        data: group_collection.map(datapoint => datapoint.value)
      })
    })
    return series
  }
}

export default StackedColumnChart
