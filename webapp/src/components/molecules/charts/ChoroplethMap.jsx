import _ from 'lodash'
import d3 from 'd3'
import React, { PropTypes, Component } from 'react'
import browser from 'components/molecules/charts_d3/utils/browser'
import palettes from 'components/molecules/charts_d3/utils/palettes'
import legend from 'components/molecules/charts_d3/renderer/legend'
import MapHelpers from 'components/molecules/charts/MapHelpers'
import Tooltip from 'components/molecules/Tooltip'
import Layer from 'react-layer'

class ChoroplethMap extends Component {

	componentDidMount() {
		this.container = React.findDOMNode(this)
		this.renderMap(this.props.data)
	}

	componentDidUpdate() {
		this.renderMap(this.props.data)
	}

  renderMap(data) {
  	const props = this.props
    const features = _.reject(data, 'properties.isBorder')
    const w = props.width - props.margin.left - props.margin.right
    const h = props.height - props.margin.top - props.margin.bottom
		const path = MapHelpers.calculatePath(features, w, h)
    let domain = props.domain()
    if (!_.isArray(domain)) {
      domain = d3.extent(features, options.value) // Deal with this options.value - not sure how
      domain[0] = Math.min(domain[0], 0)
    }
    const colorScale = d3.scale.threshold().domain(domain.concat()).range(props.colors.concat())
    this.renderMapLocations(features, path)
  }

  renderMapLocations(features, path) {
  	const props = this.props
    const svg = d3.select(this.container)
    const g = svg.select('.data')
  	const location = g.selectAll('.location').data(features, (d, i) => d['properties.location_id'] || i)
    location.enter().append('path')
    location.attr({
      'd': path,
      'class': d => {
        let classNames = ['location']
        if (_.isFinite(d.properties.value)) {
          classNames.push('clickable')
        }
        return classNames.join(' ')
      }
    })
    .style('fill', d => {
      var v = d.properties.value
      return _.isFinite(v) ? MapHelpers.getColor(v, props.domain, props.colors, props.data_format) : '#fff'
    })
    .on('click', this._onClick)
    .on('mousemove', this._onMouseMove)
    .on('mouseout', this._onMouseOut)
    location.exit().remove()
  }

  _onMouseMove = (location) => {
    const xFormat = value => d3.format(Math.abs(value) < 1 ? '.4f' : 'n')(value)
    let locationValue = xFormat(MapHelpers.valueForLocation(this.props.data, location) || 0)
    if (this.props.data_format === 'bool') {
      locationValue = Math.abs(locationValue) !== 0 ? 'Yes' : 'No'
    }
    const displayValue = location.properties.name + ': ' + locationValue
    const evt = d3.event
    const render = () => <Tooltip left={evt.pageX + 2} top={ evt.pageY + 2}>{displayValue}</Tooltip>
    this.layer ? this.layer._render = render : this.layer = new Layer(document.body, render)
    this.layer.render()
  }

  _onMouseOut = () => {
    if (this.layer) {
      this.layer.destroy()
      this.layer = null
    }
  }

  _onClick = (location) => {
    if (this.layer) {
      this.layer.destroy()
      this.layer = null
    }
    this.props.onClick(location.properties.location_id)
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
	data: PropTypes.array,
	colors: PropTypes.array,
	data_format: PropTypes.string,
	domain: PropTypes.func,
	width: PropTypes.number,
	height: PropTypes.number,
	onClick: PropTypes.func,
  margin: PropTypes.shape({
    top: PropTypes.number,
    right: PropTypes.number,
    bottom: PropTypes.number,
    left: PropTypes.number
  })
}

export default ChoroplethMap

