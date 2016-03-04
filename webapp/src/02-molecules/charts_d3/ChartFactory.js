import _ from 'lodash'
import d3 from 'd3'

import browser from '02-molecules/charts_d3/utils/browser'

var CHARTS = {
  BarChart: require('02-molecules/charts_d3/bar_chart/BarChart'),
  BulletChart: require('02-molecules/charts_d3/bullet_chart/BulletChart'),
  ChoroplethMap: require('02-molecules/charts_d3/choropleth_map/ChoroplethMap'),
  ChoroplethMapLegend: require('02-molecules/charts_d3/choropleth_map/ChoroplethMapLegend'),
  ColumnChart: require('02-molecules/charts_d3/column_chart/ColumnChart'),
  GroupedBarChart: require('02-molecules/charts_d3/grouped_bar_chart/GroupedBarChart'),
  HeatmapChart: require('02-molecules/charts_d3/heatmap/Heatmap'),
  Histogram: require('02-molecules/charts_d3/histogram/Histogram'),
  LineChart: require('02-molecules/charts_d3/line_chart/LineChart'),
  AreaChart: require('02-molecules/charts_d3/area_chart/AreaChart'),
  PieChart: require('02-molecules/charts_d3/pie_chart/PieChart'),
  ScatterChart: require('02-molecules/charts_d3/scatter_chart/ScatterChart'),
  TableChart: require('02-molecules/charts_d3/table_chart/TableChart')
}

var DEFAULTS = {
  margin: {
    top: 0,
    right: 0,
    bottom: 0,
    left: 0
  }
}

function ChartFactory (type, el, data, options) {
  if (!_.isFunction(CHARTS[type])) {
    throw new Error(type + ' is not a valid chart type')
  }
  _.defaults(CHARTS[type].prototype, ChartFactory.prototype)

  var chart = new CHARTS[type]()
  chart.initialize(el, data, options)

  return chart
}

ChartFactory.prototype.initialize = function (el, data, options) {
  options = this._options = _.defaults({}, options, this.defaults, DEFAULTS)

  var aspect = _.get(options, 'aspect', 1)
  this._width = _.get(options, 'width', el.clientWidth)
  this._height = _.get(options, 'height', this._width / aspect)

  var svg = this._svg = d3.select(el).append('svg')
    .attr({
      'viewBox': '0 0 ' + this._width + ' ' + this._height
    })

  if (browser.isIE() || browser.isWkhtmlToPdf()) {
    svg.attr({
      'width': this._width,
      'height': this._height
    })
  }
  var h = this._height - options.margin.top - options.margin.bottom

  svg.append('rect')
    .attr({
      'class': 'bg',
      'x': options.margin.left,
      'y': 0,
      'width': this._width - options.margin.left - options.margin.right,
      'height': h
    })

  var g = svg.append('g')
    .attr('transform', 'translate(' + options.margin.left + ', ' +
      options.margin.top + ')')

  g.append('g').attr('class', 'y axis')
  g.append('g').attr({
    'class': 'x axis',
    'transform': 'translate(0, ' + h + ')'
  })
  g.append('g').attr('class', 'data')
  g.append('g').attr('class', 'annotation')

  this.update(data, options)
}

export default ChartFactory
