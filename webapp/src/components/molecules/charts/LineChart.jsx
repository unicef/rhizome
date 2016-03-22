import _ from 'lodash'
import d3 from 'd3'
import React, { PropTypes, Component } from 'react'

import format from 'components/molecules/charts/utils/format'
import palettes from 'components/molecules/charts/utils/palettes'
import LineChartRenderer from 'components/molecules/charts/renderers/line-chart'


const DEFAULTS = {
  margin: {
    top: 12,
    right: 0,
    bottom: 20,
    left: 0
  },
  annotated: false,
  scale: d3.scale.linear,
  seriesName: _.property('name'),
  values: _.property('values'),
  color: palettes.blue,
  x: _.property('campaign.start_date'),
  xFormat: format.timeAxis,
  y: _.property('value'),
  yFormat: d3.format(',d')
}

class LineChart extends Component {
  constructor(props) {
    super(props)
    this.options = _.defaults({}, props.options, DEFAULTS)
  }

  componentDidMount () {
    this.container = React.findDOMNode(this)
    this.chart = new LineChartRenderer(this.props.data, this.options, this.container)
    this.chart.render()
  }

  componentDidUpdate () {
    this.chart.update(this.props.data, this.options, this.container)
  }

  render () {
    const props = this.props
    const margin = props.margin
    const viewBox = '0 0 ' + props.width + ' ' + props.height
    const bg_height = props.height - margin.top - margin.bottom
    const bg_width = props.width - margin.left - margin.right

    return (
      <svg className='line' viewBox={viewBox} width={props.width} height={props.height}>
        <rect className='bg' width={bg_width} height={bg_height} x={margin.left} y={0}></rect>
        <g transform={`translate(${margin.left}, ${margin.top})`}>
          <g className='y axis'></g>
          <g className='x axis' transform={`translate(0, ${bg_height})`}></g>
          <g className='data'></g>
          <g className='annotation'></g>
        </g>
      </svg>
    )
  }
}

LineChart.propTypes = {
  width: PropTypes.number,
  height: PropTypes.number,
  margin: PropTypes.shape({
    top: PropTypes.number,
    right: PropTypes.number,
    bottom: PropTypes.number,
    left: PropTypes.number
  })
}

export default LineChart

