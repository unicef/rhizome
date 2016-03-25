import _ from 'lodash'
import d3 from 'd3'
import React, { PropTypes, Component } from 'react'

import formatUtil from 'components/molecules/charts/utils/format'
import ChoroplethMapRenderer from 'components/molecules/charts/renderers/choropleth-map'

class ChoroplethMap extends Component {
  constructor(props) {
    super(props)
    this.params = {}
  }

  componentDidMount () {
    this.container = React.findDOMNode(this)
    this.map = new ChoroplethMapRenderer(this.getParams(), this.container)
    this.map.render()
  }

  componentDidUpdate () {
    this.map.update(this.getParams(), this.container)
  }

  getParams () {
    const aspect = this.params.aspect || 1
    this.params = this.props
    this.params.width = this.props.width || this.container.clientWidth
    this.params.height = this.props.height || this.params.width / aspect
    this.params.colors = this.props.colors || this.props.color
    return this.params
  }

  render () {
    const width = this.params.width || 100
    const height = this.params.height || 100
    const viewBox = '0 0 ' + width + ' ' + height
    const lineWidth = 10
    const lineHeight = 10
    const lineInterval = 5

    return (
      <svg className='reds' viewBox={viewBox} width={width} height={height}>
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

export default ChoroplethMap

