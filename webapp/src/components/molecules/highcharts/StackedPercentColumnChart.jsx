import _ from 'lodash'
import React from 'react'

import HighChart from 'components/molecules/highcharts/HighChart'
import format from 'utilities/format'

class StackedPercentColumnChart extends HighChart {

  constructor (props) {
    super(props)
    this.state = { stack_mode: props.type_params.stack_mode }
  }

  _toggleStackMode = () => {
    const stack_modes = ['normal', 'percent', null]
    const index = stack_modes.indexOf(this.state.stack_mode) + 1
    const new_state = index === 3 ? stack_modes[0] : stack_modes[index]
    this.setState({stack_mode: new_state})
    this.props.updateTypeParams('stack_mode', new_state)
    this.chart.series.forEach(s => s.update({stacking: new_state}, false))
    this.chart.yAxis[0].update({
      labels: {format: new_state === 'percent' ? '{value}%' : '{value}'},
      max: new_state === 'percent' ? 100 : null
    })
    this.chart.redraw()
  }

  setConfig = function () {
    const props = this.props
    const first_indicator = props.selected_indicators[0]
    const multipleCampaigns = props.datapoints.meta.campaign_list.length > 1

    this.config = {
      chart: {
        type: 'column'
      },
      series: this.setSeries(),
      xAxis: this.setXAxis(multipleCampaigns),
      yAxis: {
        title: { text: '' },
        max: this.state.stack_mode === 'percent' ? 100 : null,
        labels : {
          format: this.state.stack_mode === 'percent' ? '{value}%' : '{value}'
        }
      },
      exporting: {
        buttons: {
          customButton: {
            text: 'Column Stacking',
            onclick: this._toggleStackMode,
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
      tooltip: {
        headerFormat: '<b>{series.name}</b><br/>',
        pointFormatter: function () {
          const value = format.autoFormat(this.y, first_indicator.data_format, 1)
          if (multipleCampaigns) {
            const date = format.monthYear(this.category.name)
            const location = this.category.parent.name
            return `${location}: <strong>${value}</strong><br/>${date}`
          }
          return `${this.category}: <strong>${value}</strong><br/>`
        }
      }
    }
  }

  setSeries = function () {
    const data = this.props.datapoints.flattened
    const groupByIndicator = this.props.groupBy === 'indicator'
    const grouped_data = groupByIndicator ? _.groupBy(data, 'indicator.id') : _.groupBy(data, 'location.id')
    const series = []
    _.forEach(grouped_data, group_collection => {
      const first_datapoint = group_collection[0]
      const color = this.props.indicator_colors[first_datapoint.indicator.id]
      group_collection = _.sortBy(group_collection, group => group.campaign.start_date.getTime())
      group_collection = _.sortBy(group_collection, group => group.location.name)
      series.push({
        name: groupByIndicator ? first_datapoint.indicator.name : first_datapoint.location.name,
        data: group_collection.map(datapoint => datapoint.value),
        stacking: this.state.stack_mode,
        color: color
      })
    })
    return series
  }

  setXAxis = function (multipleCampaigns) {
    const locations = this.props.datapoints.raw.map(d => this.props.locations_index[d.location])
    if (!multipleCampaigns) {
      return {categories: locations}
    }
    let xAxis = {categories: this._getGroupedCategories()}
    if (this.props.groupByTime === 'year') {
      xAxis.labels = {
        format: '{value:%Y}',
        style: { fontFamily: 'proxima-bold' }
      }
    } else {
      xAxis.labels = {
        format: "{value:%b <br/> %y'}"
      }
    }
    return xAxis
  }

  _getGroupedCategories = function () {
    // This creates the necessary data structure for a Grouped Category chart.
    // But loading the plugin is troublesome.
    // There is no npm package for it + Importing manually doesnt seem to work
    const data = this.props.datapoints.melted
    const groupByIndicator = this.props.groupBy === 'indicator'
    const grouped_data = !groupByIndicator ? _.groupBy(data, 'indicator.id') : _.groupBy(data, 'location.id')
    const grouped_categories = []
    _.forEach(grouped_data, (group, key) => {
      const subGrouped = _.groupBy(group, 'campaign.id')
      const subGroupedAndSorted = _.sortBy(subGrouped, group => group[0].campaign.start_date.getTime())
      grouped_categories.push({
        name: this.props.locations_index[key].name,
        categories: _.map(subGroupedAndSorted, group => group[0].campaign.start_date.getTime())
      })
    })
    return _.sortBy(grouped_categories, grouped_category => grouped_category.name)
  }
}

export default StackedPercentColumnChart
