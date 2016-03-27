import _ from 'lodash'
import d3 from 'd3'
import React, { PropTypes, Component } from 'react'

import formatUtil from 'components/molecules/charts/utils/format'
import palettes from 'components/molecules/charts/utils/palettes'
import ChoroplethMapRenderer from 'components/molecules/charts/renderers/choropleth-map'

class ChoroplethMap extends Component {

  static propTypes = {
    data: PropTypes.array,
    data_format: PropTypes.string,
    domain: PropTypes.func,
    onClick: PropTypes.func,
    value: PropTypes.func,
    colors: PropTypes.array,
    height: PropTypes.number,
    width: PropTypes.number,
    margin: PropTypes.shape({
       top: PropTypes.number,
       right: PropTypes.number,
       bottom: PropTypes.number,
       left: PropTypes.number
    })
  }

  static defaultProps = {
    data: null,
    data_format: 'pct',
    domain: _.noop,
    onClick: _.noop,
    value: d => d.properties.value,
    colors: palettes.orange,
    height: 0,
    width: 0,
    margin: { top: 0, right: 0, bottom: 20, left: 0 }
  }

  constructor(props) {
    super(props)
    this.params = this.props
  }

  componentDidMount () {
    this.container = React.findDOMNode(this)
    const chart = this.getParams()
    this.map = new ChoroplethMapRenderer(chart.data, chart, this.container)
    this.map.render()
  }

  componentDidUpdate () {
    console.log('----------- ChoroplethMap.componentDidUpdate')
    this.params = this.props
    const chart = this.getParams()
    this.map.update(chart.data, chart, this.container)
  }

  getParams () {
    const aspect = this.params.aspect || 1
    this.params.width = this.props.width || this.container.clientWidth
    this.params.height = this.props.height || this.params.width / aspect
    this.params.colors = this.props.colors || this.props.color
    return this.params
  }

  render () {
    const lineWidth = 10
    const lineHeight = 10
    const lineInterval = 5

    return (
      <svg className='reds'>
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

