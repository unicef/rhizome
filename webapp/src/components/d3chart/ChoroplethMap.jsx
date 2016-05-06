import _ from 'lodash'
import d3 from 'd3'
import React, { PropTypes } from 'react'

import Chart from 'components/d3chart/Chart'

import palettes from 'utilities/palettes'
import aspects from 'components/d3chart/utils/aspects'

class ChoroplethMap extends Chart {

  static defaultProps = {
    data: null,
    data_format: 'pct',
    domain: _.noop,
    onClick: _.noop,
    value: d => d.properties.value,
    colors: palettes.traffic_light,
    height: 0,
    width: 0,
    margin: { top: 0, right: 0, bottom: 20, left: 0 }
  }

  setData () { console.log('ChoroplethMap.setData')
    const datapoints = this.props.datapoints.melted
    if (!datapoints || datapoints.length === 0) {
      return this.data = this.props.features
    }

    const selected_indicators = this.props.selected_indicators
    const xAxis  = selected_indicators[0] ? selected_indicators[0].id : 0
    const groupedDatapoints = _(datapoints).groupBy('indicator.id').value()
    const index = _.indexBy(groupedDatapoints[xAxis], 'location.id')

    // Make sure we only get data for the current campaign maps can't
    // display historical data. Index by location for quick lookup.
    const dataIdx = _(datapoints)
      .filter(d => d.campaign.id === this.props.selected_campaigns[0])
      .indexBy('location.id')
      .value()

    this.props.features.forEach(feature => {
      var datapoint = dataIdx[feature.properties.location_id]
      if (datapoint) {
        feature.properties[datapoint.indicator.id] = datapoint.value
      }
      // JD -- Ensure that the index has properties for all locations, not just those with data
      if (!index[feature.properties.location_id]) {
        index[feature.properties.location_id] = this.props.locations_index[feature.properties.location_id]
      }
    })

    this.data  = this.props.features.map(feature => {
      const datapoint = index[feature.properties.location_id]
      const properties = _.merge({}, datapoint.location, { value: datapoint['value'] }) || {}
      return _.merge({}, feature, {properties: properties}, datapoint.location)
    })
  }

  setOptions () {
    console.log('------- ChoroplethMap.setOptions')
    const props = this.props
    const options = this.options
    const selected_locations = props.selected_locations
    const selected_indicators = props.selected_indicators
    const selected_locations_index = _.indexBy(selected_locations, 'id')
    const selected_indicators_index = _.indexBy(selected_indicators, 'id')
    options.height = props.height || window.innerHeight - 100
    options.width = props.height || options.height
    options.colors = props.colors || props.color
    options.x = selected_indicators[0] ? selected_indicators[0].id : 0
    options.y = selected_indicators[1] ? selected_indicators[1].id : 0
    options.z = selected_indicators[2] ? selected_indicators[2].id : 0
    const mapIndicator = selected_indicators_index[options.x]
    options.name = d => selected_locations_index[d.properties.location_id].name || ''
    options.border = props.features
    options.data_format = mapIndicator.data_format
    options.domain = () => [mapIndicator.bad_bound, mapIndicator.good_bound]
    options.value = d => d.properties[mapIndicator.id]
    options.xFormat = mapIndicator.data_format === 'pct' ? d3.format(',.1%') : d3.format('')
    options.ticks = this.reverseBounds({bad: mapIndicator.bad_bound, good: mapIndicator.good_bound})
    options.onClick = id => this.props.primaryClick(id)
    return options
  }

  reverseBounds (bounds) {
    bounds.reversed = false
    if (bounds.bad > bounds.good){
      var temp = bounds.bad
      bounds.bad = bounds.good
      bounds.good = temp
      bounds.reversed = true
    }
    return bounds
  }

  render () {
    const lineWidth = 10
    const lineHeight = 10
    const lineInterval = 5

    return (
      <svg className='reds'>
        <g className='colors'>
          <g className='data'></g>
          <g className='legend'></g>
        </g>
        <g className='bubbles'>
          <g className='data'></g>
          <g className='legend'></g>
        </g>
        <g className='stripes'>
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

export default ChoroplethMap

