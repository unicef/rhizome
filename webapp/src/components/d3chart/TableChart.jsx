import _ from 'lodash'
import React, { PropTypes } from 'react'

import Chart from 'components/d3chart/Chart'
import palettes from 'utilities/palettes'

class TableChart extends Chart {

  static defaultProps = {
    data: null,
    cellHeight: 30,
    cellFontSize: 14,
    fontSize: 12,
    margin: { top: 100, right: 40, bottom: 40, left: 40 },
    colors: palettes.traffic_light,
    sourceColumn: d => d.short_name,
    column: d => d.indicator.short_name,
    seriesName: d => d.name,
    sortDirection: 1,
    value: d => d ? d.value : null,
    values: d => d.values
  }

  setData = function () {
    const selected_campaign_id = this.props.selected_campaigns[0].id
    const filtered_datapoints = this.props.datapoints.flattened.filter(datapoint => datapoint.campaign.id === selected_campaign_id)
    const data = _.groupBy(filtered_datapoints, 'location.id')
    this.options.default_sort_order = _.map(data, datapoint_group => datapoint_group[0].location.name)
    this.options.parent_location_map = _.map(data, datapoint_group => {
      const parent_location = this.props.locations_index[datapoint_group[0].location.parent_location_id]
      return {
        name: datapoint_group[0].location.name,
        parent_location_name: parent_location? parent_location.name : ''
      }
    })
    this.options.parent_location_map = _.indexBy(this.options.parent_location_map, 'name')
    this.data = _.toArray(data).map(datapoint_group => {
      const values = []
      datapoint_group.forEach(datapoint => {
        console.log('datapoint.value', datapoint.value)
        values.push({
          indicator: datapoint.indicator,
          value: datapoint.value,
          campaign: datapoint.campaign,
          displayValue: this.getFormattedValue(datapoint),
          location: datapoint.location
        })
      })
      return {
        name: datapoint_group[0].location.name,
        parent_location_id: datapoint_group[0].location.parent_location_id,
        values: values,
        campaign_id: datapoint_group[0].campaign.id
      }
    })
    return this.data
  }

  getFormattedValue = function (datapoint) {
    const data_format = datapoint.indicator.data_format
    if (_.isNull(datapoint.value)) {
      return ''
    } else if (data_format === 'pct' && datapoint.value === 0) {
      return '0 %'
    } else if (data_format === 'pct' && datapoint.value !== 0) {
      return (datapoint.value * 100).toFixed(1) + ' %'
    } else if (data_format === 'bool' && datapoint.value === 0) {
      datapoint.value = -1 // temporary hack to deal with coloring the booleans.
      return 'No'
    } else if (data_format === 'bool' && datapoint.value > 0) {
      datapoint.value = 2 // temporary hack to deal with coloring the booleans.
      return 'Yes'
    } else {
      return datapoint.value
    }
  }

  setOptions = function () {
    const aspect = this.options.aspect || 1
    this.options.width = this.props.width || this.container.clientWidth
    this.options.height = this.props.height || this.options.width / aspect
    this.options.headers = this.options.selected_indicators
    this.options.xDomain = this.options.headers.map(indicator => indicator.short_name)
    this.options.x = this.options.selected_indicators[0]
    this.options.y = this.options.selected_indicators[1] ? this.options.selected_indicators[1].id : 0
    this.options.z = this.options.selected_indicators[2] ? this.options.selected_indicators[2].id : 0
    return this.options
  }

  render = function () {
    return (
      <svg className='heatmap sortable'>
        <g className='margin'>
          <g className='z axis'></g>
          <g className='y axis'></g>
          <g className='x axis'></g>
          <g className='data'></g>
          <g className='source-footer'></g>
          <g className='legend'></g>
        </g>
      </svg>
    )
  }
}

TableChart.propTypes = {
  // Chart Data
  data: PropTypes.array,
  headers: PropTypes.array,
  parent_location_map: PropTypes.object,
  selected_campaigns: PropTypes.array,
  // Look and Feel
  colors: PropTypes.array,
  cellHeight: PropTypes.number,
  cellFontSize: PropTypes.number,
  fontSize: PropTypes.number,
  width: PropTypes.number,
  height: PropTypes.number,
  margin: PropTypes.shape({
    top: PropTypes.number,
    right: PropTypes.number,
    bottom: PropTypes.number,
    left: PropTypes.number
  }),
  // Functions to map data to table
  sourceColumn: PropTypes.func,
  column: PropTypes.func,
  seriesName: PropTypes.func,
  sortDirection: PropTypes.func,
  value: PropTypes.func,
  values: PropTypes.func
}

export default TableChart
