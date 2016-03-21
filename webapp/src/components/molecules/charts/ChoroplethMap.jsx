import _ from 'lodash'
import d3 from 'd3'
import React, { PropTypes, Component } from 'react'

import formatUtil from 'components/molecules/charts_d3/utils/format'
import ChoroplethMapRenderer from 'components/molecules/charts/ChoroplethMapRenderer'

class ChoroplethMap extends Component {
  constructor(props) {
    super(props)
  }

  componentDidMount () {
    this.container = React.findDOMNode(this)
    this.map = new ChoroplethMapRenderer(this.props.data, this.props.options, this.container)
    this.map.render()
  }

  componentDidUpdate () {
    this.map.update(this.props.data, this.props.options, this.container)
  }

  render () {
    const viewBox = '0 0 ' + this.props.width + ' ' + this.props.height
    const lineWidth = 10
    const lineHeight = 10
    const lineInterval = 5

    return (
      <svg className='reds' viewBox={viewBox} width={this.props.width} height={this.props.height}>
        <g>
          <g className='data'></g>
          <g className='legend'></g>
        </g>
        <g clasName='bubbles'>
          <g className='data'></g>
          <g className='legend'></g>
        </g>
        <g clasName='stripes'>
          <g className='data'></g>
          <g className='legend'></g>
        </g>
        <defs>
          <pattern id='stripe' patternUnits='userSpaceOnUse' width={lineWidth} height={lineHeight}>
            <line x1={0} y1={0} x2={-lineInterval} y2={lineHeight}></line>
            <line x1={lineInterval} y1={0} x2={0} y2={lineHeight}></line>
            <line x1={2 * lineInterval} y1={0} x2={lineInterval} y2={lineHeight}></line>
            <line strokeLinecap='square' strokeLinejoin='miter' strokeWidth={1}></line>
          </pattern>
        </defs>
      </svg>
    )
  }
}

ChoroplethMap.propTypes = {
  width: PropTypes.number,
  height: PropTypes.number,
  margin: PropTypes.shape({
    top: PropTypes.number,
    right: PropTypes.number,
    bottom: PropTypes.number,
    left: PropTypes.number
  })
}

export default ChoroplethMap

