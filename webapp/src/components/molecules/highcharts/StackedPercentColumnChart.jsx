import _ from 'lodash'
import React from 'react'

import HighChart from 'components/molecules/highcharts/HighChart'
import format from 'utilities/format'

class StackedPercentColumnChart extends HighChart {

  _getGroupedCategories = function () {
    // This creates the necessary data structure for a Grouped Category chart.
    // But loading the plugin is troublesome.
    // There is no npm package for it + Importing manually doesnt seem to work
    const data = this.props.datapoints.melted
    const groupByIndicator = this.props.groupBy === 'indicator'
    const grouped_data = !groupByIndicator ? _.groupBy(data, 'indicator.id') : _.groupBy(data, 'location.id')
    const grouped_categories = []
    _.forEach(grouped_data, (group, key) => {
      const grouped = _.groupBy(group, 'campaign.id')
      grouped_categories.push({
        name: this.props.locations_index[key].name,
        categories: _.map(grouped, group => group[0].campaign.start_date.getTime())
      })
    })
    return grouped_categories
  }

  setConfig = function () {
    const props = this.props
    const first_indicator = props.selected_indicators[0]
    const locations = props.datapoints.raw.map(datapoint => props.locations_index[datapoint.location])
    const multipleCampaigns = props.datapoints.meta.campaign_list.length > 0

    this.config = {
      chart: { type: 'column' },
      xAxis: {
        categories: multipleCampaigns ? this._getGroupedCategories() : locations,
      },
      yAxis: {
        title: { text: 'Percent' }
      },
      plotOptions: {
        column: { stacking: 'percent' }
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
    if (multipleCampaigns) {
      this.config.xAxis.labels = { format: "{value:%b <br/> %y'}" }
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

export default StackedPercentColumnChart
