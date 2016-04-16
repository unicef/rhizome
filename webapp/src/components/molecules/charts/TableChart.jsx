import React, { PropTypes } from 'react'

import Chart from 'components/molecules/charts/Chart'
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
    const filtered_datapoints = this.props.data.filter(datapoint => datapoint.campaign.id === selected_campaign_id)
    this.data = filtered_datapoints.map(datapoint => {
      const values = []
      datapoint.indicators.forEach(i => {
        const indicator_id = i.indicator
        if (i.value != null) {
          let displayValue = i.value
          if (this.props.indicators_index[indicator_id].data_format === 'pct') {
            displayValue = (i.value * 100).toFixed(1) + ' %'
          } else if (this.props.indicators_index[indicator_id].data_format === 'bool' && i.value === 0) {
            displayValue = 'No'
            i.value = -1 // temporary hack to deal with coloring the booleans.
          } else if (this.props.indicators_index[indicator_id].data_format === 'bool' && i.value > 0) {
            displayValue = 'Yes'
            i.value = 2 // temporary hack to deal with coloring the booleans.
          }
          values.push({
            indicator: this.props.indicators_index[indicator_id],
            value: i.value,
            campaign: datapoint.campaign,
            displayValue: displayValue,
            location: this.props.locations_index[datapoint.location]
          })
        } else {
          values.push({
            indicator: this.props.indicators_index[indicator_id],
            value: null,
            campaign: datapoint.campaign,
            displayValue: '',
            location: this.props.locations_index[datapoint.location]
          })
        }
      })
      return {
        name: this.props.locations_index[datapoint.location].name,
        parent_location_id: this.props.locations_index[datapoint.location].parent_location_id,
        values: values,
        campaign_id: datapoint.campaign.id
      }
    })
    return this.data
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
  default_sort_order: PropTypes.array,
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
