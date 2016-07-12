import _ from 'lodash'
import React from 'react'

import HighChart from 'components/highchart/HighChart'
import format from 'utilities/format'

class ColumnChart extends HighChart {

  constructor (props) {
    super(props)
    this.state = { stack_mode: props.type_params.stack_mode }
  }

  setConfig = function () {
    const self = this
    const props = this.props
    const groupedByTime = _.toArray(props.datapoints.grouped).length > 1
    const groupedByYear = props.groupByTime === 'year'
    const groupedByQuarter = props.groupByTime === 'quarter'
    const first_indicator = props.selected_indicators[0]
    const last_indicator = props.selected_indicators[props.selected_indicators.length-1]
    this.config = {
      chart: {
        type: 'column'
      },
      series: this.setSeries(),
      xAxis: this.setXAxis(groupedByTime),
      yAxis: [
        {
          title: { text: '' },
          max: this.state.stack_mode === 'percent' ? 100 : null,
          labels : {
            formatter: function () { return self.yAxisFormatter(this) }
          }
        },
        {
          title: { text: '' },
          labels: {
            formatter: function () { return format.autoFormat(this.value, last_indicator.data_format) }
          },
          opposite: true
        },
      ],
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
          const data_format = this.series.type === 'spline' ? last_indicator.data_format : first_indicator.data_format
          const value = format.autoFormat(this.y, data_format, 1)
          if (groupedByTime) {
            const date = groupedByYear || groupedByQuarter ? this.category.name : format.monthYear(this.category.name)
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
    const groupByYear = this.props.groupByTime === 'year'
    const groupedByQuarter = this.props.groupByTime === 'quarter'
    const groupByIndicator = this.props.groupBy === 'indicator'
    const grouped_data = groupByIndicator ? _.groupBy(data, 'indicator.id') : _.groupBy(data, 'location.id')
    const multipleIndicators = this.props.selected_indicators.length > 1
    const first_indicator = this.props.selected_indicators[0]
    const last_indicator = this.props.selected_indicators[this.props.selected_indicators.length-1]
    const series = []
    _.forEach(grouped_data, datapoints => {
      const first_datapoint = datapoints[0]
      const color = this.props.indicator_colors[first_datapoint.indicator.id]
      if (!groupByYear && !groupedByQuarter) {
        datapoints = _.sortBy(datapoints, datapoint => datapoint.campaign.start_date.getTime())
      } else {
        datapoints = _.sortBy(datapoints, datapoint => datapoint.time_grouping)
      }
      datapoints = _.sortBy(datapoints, datapoint => datapoint.location.name)
      if (multipleIndicators && first_datapoint.indicator.data_format !== first_indicator.data_format) {
        // If the last indicator selected is of a different data type than the rest, turn it into a line
        series.push({
          yAxis: 1,
          name: last_indicator.name,
          color: this.props.indicator_colors[last_indicator.id],
          type: 'spline',
          data: datapoints.map(datapoint => datapoint.value)
        })
      } else {
        series.push({
          name: groupByIndicator ? first_datapoint.indicator.name : first_datapoint.location.name,
          data: datapoints.map(datapoint => datapoint.value),
          stacking: this.state.stack_mode,
          color: color
        })
      }
    })
    return series
  }

  setXAxis = function (groupedByTime) {
    const locations = _.uniq(this.props.datapoints.flattened.map(d => d.location.name))
    if (!groupedByTime) {
      return {categories: locations.sort()}
    }
    let xAxis = {categories: this._getGroupedCategories()}
    if (this.props.groupByTime === 'year' || this.props.groupByTime === 'quarter') {
      xAxis.labels = {
        style: { fontFamily: 'proxima-bold' }
      }
    } else {
      xAxis.labels = {
        format: "{value:%b <br/> %y'}"
      }
    }
    return xAxis
  }

  yAxisFormatter = (point) => {
    const first_indicator = this.props.selected_indicators[0]
    const formatted_value = format.autoFormat(point.value, first_indicator.data_format, 1)
    return this.state.stack_mode === 'percent' ? point.value + '%' : formatted_value
  }

  _getQuarterName = function (time_grouping) {
    const quarter = time_grouping.substr(time_grouping.length - 1)
    const year = time_grouping.slice(0, -1)
    return year + ' Q' + quarter
  }

  _getGroupedCategories = function () {
    // This creates the necessary data structure for a Grouped Category chart.
    // But loading the plugin is troublesome.
    // There is no npm package for it + Importing manually doesnt seem to work
    const groupByYear = this.props.groupByTime === 'year'
    const groupByQuarter = this.props.groupByTime === 'quarter'
    const groupByIndicator = this.props.groupBy === 'indicator'
    const data = this.props.datapoints.flattened
    const grouped_data = !groupByIndicator ? _.groupBy(data, 'indicator.id') : _.groupBy(data, 'location.id')
    const grouped_categories = []
    _.forEach(grouped_data, (group, key) => {
      if (groupByYear) {
        const subGrouped = _.groupBy(group, 'time_grouping')
        grouped_categories.push({
          name: this.props.locations_index[key].name,
          categories: _.map(subGrouped, (group, year) => year)
        })
      } else if (groupByQuarter) {
        const subGrouped = _.groupBy(group, 'time_grouping')
        grouped_categories.push({
          name: this.props.locations_index[key].name,
          categories: _.map(subGrouped, (group, time_grouping) => this._getQuarterName(time_grouping))
        })
      } else {
        const subGrouped = _.groupBy(group, 'campaign.id')
        const subGroupedAndSorted = _.sortBy(subGrouped, group => group[0].campaign.start_date.getTime())
        grouped_categories.push({
          name: this.props.locations_index[key].name,
          categories: _.map(subGroupedAndSorted, group => group[0].campaign.start_date.getTime())
        })
      }
    })
    return _.sortBy(grouped_categories, grouped_category => grouped_category.name)
  }

  _toggleStackMode = () => {
    const self = this
    const stack_modes = ['normal', 'percent', null]
    const index = stack_modes.indexOf(this.state.stack_mode) + 1
    const new_state = index === 3 ? stack_modes[0] : stack_modes[index]
    this.setState({stack_mode: new_state})
    this.props.updateTypeParams('stack_mode', new_state)
    this.chart.series.forEach(s => s.update({stacking: new_state}, false))
    this.chart.yAxis[0].update({
      labels : {
        formatter: function () { return self.yAxisFormatter(this) }
      },
      max: new_state === 'percent' ? 100 : null
    })
    this.chart.redraw()
  }

}

export default ColumnChart
