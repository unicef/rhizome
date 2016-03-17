import _ from 'lodash'
import React, { Component, PropTypes } from 'react'
import palettes from 'components/molecules/charts_d3/utils/palettes'
import Chart from 'components/molecules/Chart'

class TableChart extends Component {
  render () {
  	const props = this.props
  	const color = typeof props.color === 'string' ? palettes[props.color] : props.color

  	const tableChart = props.data
	      ? <Chart type='TableChart'
	          data={props.data}
	          options={{
	            color: color,
	            cellSize: props.cellSize,
	            cellFontSize: props.cellFontSize,
	            onRowClick: props.onRowClick,
	            headers: props.indicators,
	            xDomain: _.map(props.indicators, 'short_name'),
	            default_sort_order: props.default_sort_order,
              parentLocationMap: props.parentLocationMap,
	            margin: props.margin
	          }}
	        />
	      : <div className='loading'>
	        	<i className='fa fa-spinner fa-spin fa-5x'></i>
	          <div>Loading</div>
	        </div>

		return tableChart
	}
}

TableChart.defaultProps = {
  data: [],
  indicators: [],
  default_sort_order: [],
  onRowClick: null,
  color: 'traffic_light',
  cellSize: 40,
  cellFontSize: 14,
  margin: {
    top: 100,
    right: 40,
    bottom: 40,
    left: 40,
  }
}

TableChart.propTypes = {
  data: PropTypes.array,
  indicators: PropTypes.arrayOf(PropTypes.object).isRequired,
  default_sort_order: PropTypes.arrayOf(PropTypes.string).isRequired,
  onRowClick: PropTypes.func,
  color: PropTypes.oneOfType([
      PropTypes.string,
		  PropTypes.arrayOf(PropTypes.string),
  ]),
  cellFontSize: PropTypes.number,
  cellSize: PropTypes.number,
  margin: PropTypes.shape({
     top: PropTypes.number,
     right: PropTypes.number,
     bottom: PropTypes.number,
     left: PropTypes.number,
  })
}

export default TableChart
