import _ from 'lodash'
import React from 'react'

import HighChart from 'components/molecules/highcharts/HighChart'
import format from 'utilities/format'

/* For now the StackedPercentColumnChart is same like StackedColumnChart same date based X Axis
But it could be designed to have a kind of categories X axis as below example from HighChart
The below kind of functionality need another helper highcharts lib called grouped-categories.js
http://www.highcharts.com/plugin-registry/single/11/Grouped-Categories
*/
// categories: [{
//         name: "America",
//         categories: [{
//             name: "USA",
//             categories: ["New York", "San Francisco"]
//         }, {
//             name: "Canada",
//             categories: ["Toronto", "Vancouver"]
//         }, {
//             name: "Mexico",
//             categories: ["Acapulco", "Leon"]
//         }]
//     }, {
//         name: "Europe",
//         categories: [{
//             name: "United Kingdom",
//             categories: ["London", "Liverpool"]
//         }, {
//             name: "France",
//             categories: ["Paris", "Marseille"]
//         }, {
//             name: "Germany",
//             categories: ["Berlin", "Munich"]
//         }]
//     }]

class StackedPercentColumnChart extends HighChart {

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
            return format.autoFormat(this.value, '')
          }
        }
      },
      tooltip: {
        xDateFormat: '%b %Y',
        pointFormatter: function (point) {
          const value = this.y
          const perct = format.autoFormat((this.percentage/100), 'pct')
          const secondary_text = props.groupBy === 'indicator' ? first_location.name : first_indicator.name
          return `<b>${secondary_text}</b><br/>${this.series.name}: <b>${value}</b> (${perct})<br/>`
        }
      },
      plotOptions: {
        column: {
          stacking: 'percent'
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

export default StackedPercentColumnChart
