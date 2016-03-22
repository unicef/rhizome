import React from 'react'
import _ from 'lodash'
import d3 from 'd3'
import Tooltip from 'components/molecules/Tooltip'
import Layer from 'react-layer'

class ChoroplethMapRenderer {
  constructor (data, options, container) {
    this.setMapParams(data, options, container)
  }

  setMapParams (data, options, container) {
    this.container = container
    this.options = options
    this.data = data
    this.features = _.reject(data, 'properties.isBorder')
    this.w = options.width - options.margin.left - options.margin.right
    this.h = options.height - options.margin.top - options.margin.bottom
    this.path = this.calculatePath(this.features, this.w, this.h)
    this.colorScale = this.getColorScale(options.domain, options.colors)
  }

  update () {
    this.setMapParams(this.data, this.options, this.container)
    this.render()
  }

  //===========================================================================//
  //                                   RENDER                                  //
  //===========================================================================//
  render () {
    const svg = d3.select(this.container)
    const g = svg.select('.data')
    const location = g.selectAll('.location').data(this.features, (d, i) => d['properties.location_id'] || i)
    location.enter().append('path')
    location.attr({
      'd': this.path,
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
      return _.isFinite(v) ? this.getColor(v, this.options.domain, this.options.colors, this.options.data_format) : '#fff'
    })
    .on('click', this._onClick)
    .on('mousemove', this._onMouseMove)
    .on('mouseout', this._onMouseOut)
    location.exit().remove()
  }


  //===========================================================================//
  //                               EVENT HANDLERS                              //
  //===========================================================================//
  _onMouseMove = (location) => {
    const xFormat = value => d3.format(Math.abs(value) < 1 ? '.4f' : 'n')(value)
    let locationValue = xFormat(this.valueForLocation(this.data, location) || 0)
    if (this.options.data_format === 'bool') {
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
    this.options.onClick(location.properties.location_id)
  }

  //===========================================================================//
  //                                    UTILITIES                              //
  //===========================================================================//
  getDomain (domain) {
    if (!_.isArray(domain)) {
      domain = d3.extent(this.features, this.options.value) // Deal with this options.value - not sure how
      domain[0] = Math.min(domain[0], 0)
    }
    return domain
  }

  calculateBounds (features) {
    if (features.length < 1) {
      return [[0, 0], [0, 0]]
    }

    const coordinates = _(features).map(feature => {
      if (feature.geometry.type !== 'MultiPolygon') {
        return _.flatten(feature.geometry.coordinates)
      }
    })
    .flatten()
    .value()

    const lat = _.property(1)
    const lng = _.property(0)
    const left = d3.min(coordinates, lng)
    const right = d3.max(coordinates, lng)
    const bottom = d3.min(coordinates, lat)
    const top = d3.max(coordinates, lat)

    return [[left, top], [right, bottom]]
  }

  calculateCenter (bounds) {
    const lat = bounds[1][1] + ((bounds[0][1] - bounds[1][1]) / 2)
    const lng = bounds[0][0] + ((bounds[1][0] - bounds[0][0]) / 2)

    return [lng, lat]
  }

  calculatePath (features, width, height) {
    const bounds = this.calculateBounds(features)
    const center = this.calculateCenter(bounds)
    const projection = d3.geo.conicEqualArea()
      .parallels([bounds[1][1], bounds[0][1]])
      .rotate([-center[0], 0])   // Rotate the globe so that the country is centered horizontally
      .center([0, center[1]])    // Set the center of the projection so that the polygon is moved vertically into the center of the viewport
      .translate([width / 2, height / 2]) // Translate to the center of the viewport
      .scale(1)
    const b = [projection(bounds[0]), projection(bounds[1])]
    const s = 1 / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height)
    projection.scale(s)
    return d3.geo.path().projection(projection)
  }

  roundToTwo (num) {
    return +(Math.round(num + 'e+3') + 'e-3')
  }

  getColorScale(domain, colors) {
    if (!_.isArray(domain)) {
      domain = d3.extent(this.features, this.options.value) // Deal with this options.value - not sure how
      domain[0] = Math.min(domain[0], 0)
    }
    return d3.scale.threshold().domain(domain.concat()).range(colors.concat())
  }

  getColor (indicatorValue, domain, colors, data_format) {
    const bad_bound = domain()[0]
    const good_bound = domain()[1]
    const reverseBounds = bad_bound > good_bound
    let mapFillColor = ''
    indicatorValue = this.roundToTwo(indicatorValue)
    if (data_format === 'bool') {
      if (indicatorValue === 0) {
        mapFillColor = colors[0]
      } else {
        mapFillColor = colors[1]
      }
    } else {
      if (reverseBounds) {
        if (indicatorValue > good_bound && indicatorValue < bad_bound) {
          mapFillColor = colors[1]
        } else if (indicatorValue <= good_bound) {
          mapFillColor = colors[2]
        } else if (indicatorValue >= bad_bound) {
          mapFillColor = colors[0]
        }
      } else {
        if (indicatorValue < good_bound && indicatorValue > bad_bound) {
          mapFillColor = colors[1]
        } else if (indicatorValue >= good_bound) {
          mapFillColor = colors[2]
        } else if (indicatorValue <= bad_bound) {
          mapFillColor = colors[0]
        }
      }
    }
    return mapFillColor
  }

  valueForLocation (data, locationObject) {
    let locationIndex = (_.select(data, d => d.location_id === locationObject.location_id))[0]
    return locationIndex.properties.value
  }

  chooseRadius (v, radius) {
    if (v > radius.domain()[1]) {
      return radius.range()[1]
    } else {
      return radius(v)
    }
  }


}

export default ChoroplethMapRenderer