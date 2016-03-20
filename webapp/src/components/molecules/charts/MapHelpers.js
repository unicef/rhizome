import _ from 'lodash'
import d3 from 'd3'

const MapHelpers = {
  wrap (text, width, x) {
    text.each(function () {
      let text = d3.select(this)
      let words = text.text().split(/\s+/).reverse()
      let word
      let line = []
      let lineNumber = 1
      let lineHeight = 1.1
      let y = text.attr('y')
      let tspan = text.text(null).append('tspan').attr('x', x).attr('y', y)
      while (words.length > 0) {
        word = words.pop()
        line.push(word)
        tspan.text(line.join(' '))
        if (tspan.node().getComputedTextLength() > (width - x)) {
          line.pop()
          tspan.text(line.join(' '))
          line = [word]
          tspan = text.append('tspan').attr('x', x).attr('y', y).attr('dy', (lineNumber * lineHeight) + 'rem').text(word)
          lineNumber += 1
        }
      }
    })
  },

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
  },

  calculateCenter (bounds) {
    const lat = bounds[1][1] + ((bounds[0][1] - bounds[1][1]) / 2)
    const lng = bounds[0][0] + ((bounds[1][0] - bounds[0][0]) / 2)

    return [lng, lat]
  },

  calculatePath (features, width, height) {
    const bounds = MapHelpers.calculateBounds(features)
    const center = MapHelpers.calculateCenter(bounds)
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
  },

  valueForLocation (data, locationObject) {
    let locationIndex = (_.select(data, d => d.location_id === locationObject.location_id))[0]
    return locationIndex.properties.value
  },

  chooseRadius (v, radius) {
    if (v > radius.domain()[1]) {
      return radius.range()[1]
    } else {
      return radius(v)
    }
  },

  roundToTwo (num) {
    return +(Math.round(num + 'e+3') + 'e-3')
  },

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

}

export default MapHelpers
