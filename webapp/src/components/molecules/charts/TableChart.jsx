import React, { PropTypes } from 'react'

import Chart from 'components/molecules/charts/Chart'
import palettes from 'components/molecules/charts/utils/palettes'

class TableChart extends Chart {

  static defaultProps = {
    data: null,
    cellHeight: 30,
    cellFontSize: 14,
    fontSize: 12,
    margin: { top: 40, right: 40, bottom: 40, left: 40 },
    colors: palettes.traffic_light,
    sourceColumn: d => d.short_name,
    column: d => d.indicator.short_name,
    seriesName: d => d.name,
    sortDirection: 1,
    value: d => d ? d.value : null,
    values: d => d.values
  }

  setOptions () {
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

  render () {
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

