import d3 from 'd3'
import _ from 'lodash'

var colors = ['#377EA4', '#B6D0D4']
const defaultPalette = ['#334B61', '#222222', '#387EA3', '#436380', '#6493A6', '#7BA1A8', '#87939E',
  '#D5E5F2', '#8FB6BD', '#A5B9CC', '#A2AAB3', '#D7D9E1', '#C5D9DD', '#AFC5CD', '#E5E9EC']

function scale (categories, palette) {
  palette = palette || colors
  var interpolate = d3.interpolate(
    d3.rgb(palette[0]),
    d3.rgb(palette[palette.length - 1]))

  var s = d3.scale.linear().domain([0, categories.length - 1])

  // Build up a range of colors for the ordinal scale by interpolating the
  // two extremes of the colors from the coolgray array
  var range = []
  for (var i = 0, l = categories.length; i < l; i++) {
    range.push(interpolate(s(i)))
  }

  return d3.scale.ordinal()
    .domain(categories)
    .range(range)
}

function map (categories, palette) {
  palette = palette || defaultPalette
  let range = _.clone(palette)
  while (range.length < categories.length) {
    range = range.concat(range)
  }
  range = range.slice(0, categories.length)

  return d3.scale.ordinal().domain(categories).range(range)
}

export default {
  scale: scale,
  map: map
}
