import React, { PropTypes } from 'react'

import Chart from 'components/molecules/charts/Chart'
import palettes from 'components/molecules/charts/utils/palettes'

class TableChart extends Chart {

  static defaultProps = {
    data: null,
    cellHeight: 30,
    cellFontSize: 14,
    fontSize: 12,
    margin: {},
    colors: palettes.traffic_light,
    sourceColumn: d => d.short_name,
    column: d => d.indicator.short_name,
    seriesName: d => d.name,
    sortDirection: 1,
    value: d => d.value,
    values: d => d.values
  }

  getParams () {
    const aspect = this.params.aspect || 1
    this.params.width = this.props.width || this.container.clientWidth
    this.params.height = this.props.height || this.params.width / aspect
    this.params.headers = this.params.selected_indicators
    this.params.xDomain = this.params.headers.map(indicator => indicator.short_name)
    this.params.x = this.params.selected_indicators[0]
    this.params.y = this.params.selected_indicators[1] ? this.params.selected_indicators[1].id : 0
    this.params.z = this.params.selected_indicators[2] ? this.params.selected_indicators[2].id : 0
    return this.params
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

