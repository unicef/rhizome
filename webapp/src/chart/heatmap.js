'use strict'

import _ from 'lodash'
import d3 from 'd3'

import formatUtil from 'util/format'

function _sortValue (s, sortCol) {
  // jshint validthis: true
  var options = this._options

  var val = (sortCol === null)
    ? options.seriesName(s)
    : options.value(_.find(options.values(s), d => options.column(d) === sortCol))

  return val
}

var DEFAULTS = {
  cellSize: 16,
  column: _.property('indicator.short_name'),
  fontSize: 12,
  format: formatUtil.general,
  headerText: _.property('short_name'),
  headers: [],
  margin: {
    top: 120,
    right: 120,
    bottom: 0,
    left: 120
  },
  onClick: null,
  onColumnHeadOver: null,
  onColumnHeadOut: null,
  onMouseMove: null,
  onMouseOut: null,
  onRowClick: null,
  seriesName: _.property('name'),
  sortValue: _sortValue,
  values: _.property('values'),
  value: _.property('value')
}

function Heatmap () {}

_.extend(Heatmap.prototype, {
  defaults: DEFAULTS,
  sortCol: null,

  initialize: function (el, data, options) {
    options = this._options = _.defaults({}, options, DEFAULTS)

    var svg = this._svg = d3.select(el)
        .append('svg')
        .attr('class', 'heatmap sortable')

    var g = svg.append('g').attr('class', 'margin')

    g.append('g').attr('class', 'y axis')
    g.append('g').attr('class', 'x axis')
    g.append('g').attr('class', 'data')
    g.append('g').attr('class', 'legend')

    this.update(data)
  },

  update: function (data, options) {
    options = _.extend(this._options, options)
    var margin = options.margin

    var self = this

    var w = Math.max(options.headers.length * options.cellSize, 0)
    var h = Math.max(data.length * options.cellSize, 0)

    var svg = this._svg
      .attr({
        'viewBox': '0 0 ' + (w + margin.left + margin.right) + ' ' + (h + margin.top + margin.bottom),
        'width': (w + margin.left + margin.right),
        'height': (h + margin.top + margin.bottom)
      })
      .datum(data)

    var xScale = d3.scale.ordinal()
        .domain(_.map(options.headers, options.headerText))
        .rangeBands([0, w], 0.1)

    var x = _.flow(options.column, xScale)

    var sortCol = this.sortCol
    var sortValue = _.partial(options.sortValue.bind(this), _, sortCol)

    var yScale = d3.scale.ordinal()
      .domain(_(data).sortBy(sortValue, this).map(options.seriesName).value())
      .rangeBands([0, h], 0.1)

    var y = _.flow(options.seriesName, yScale)

    var transform = function (d, i) {
      return 'translate(0, ' + y(d) + ')'
    }

    var fill = options.scale

    svg.select('.margin')
        .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')')

    var g = svg.select('.data')

    g.on('mouseout', function () { self._onRowOut.apply(self) })

    var row = g.selectAll('.row').data(data)

    row.enter().append('g')
        .attr({
          'class': 'row',
          'transform': transform
        })

    row.exit()
      .transition().duration(300)
      .style('opacity', 0)
      .remove()

    row.on('mouseover', function (d, i) {
      self._onRowOver([d, i])
    })
    .transition()
    .duration(750)
    .attr('transform', transform)

    // Add cells to each row
    var cell = row.selectAll('.cell').data(options.values)

    cell.transition()
      .duration(500)
      .style('fill', fill)
      .attr({
        'height': yScale.rangeBand(),
        'width': xScale.rangeBand(),
        'x': x
      })

    cell.enter().append('rect')
      .attr({
        'class': 'cell',
        'height': yScale.rangeBand(),
        'x': x,
        'width': xScale.rangeBand()
      })
      .style({
        'opacity': 0,
        'fill': fill
      })
      .transition()
      .duration(500)
      .style('opacity', 1)

    cell.exit()
      .transition()
      .duration(300)
      .style('opacity', 0)
      .remove()

    cell
      .attr('id', d => [d.location.name, d.indicator.short_name].join('-'))
        .style('cursor', _.isFunction(options.onClick) ? 'pointer' : 'initial')
        .on('mousemove', options.onMouseMove)
        .on('mouseout', options.onMouseOut)
        .on('click', options.onClick)

    svg.select('.x.axis')
      .transition().duration(500)
      .call(d3.svg.axis()
        .scale(xScale)
        .orient('top')
        .outerTickSize(0))

    svg.selectAll('.x.axis text')
      .style({
        'text-anchor': 'start',
        'font-size': options.fontSize,
        'font-weight': function (d) {
          return (d === sortCol)
            ? 'bold'
            : 'normal'
        }
      })
      .attr('transform', 'translate(' + (xScale.rangeBand() / 2) + ', 0) rotate(-45)')
      .on('click', function (d, i) { self._setSort(d, i) })
      .on('mouseover', function (d, i) {
        options.onColumnHeadOver(d, i, this)
      })
      .on('mouseout', function (d, i) {
        options.onColumnHeadOut(d, i, this)
      })

    svg.select('.y.axis')
      .transition().duration(500)
      .call(d3.svg.axis()
        .scale(yScale)
        .orient('left')
        .outerTickSize(0))

    svg.selectAll('.y.axis text')
      .style('font-size', options.fontSize)
      .on('click', function (d, i) {
        options.onRowClick(d, i, this)
      })

    if (options.legend) {
      svg.select('.legend')
        .call(options.legend)
        .attr('transform', function () {
          var bbox = this.getBoundingClientRect()
          var dx = w + margin.right - bbox.width
          var dy = 0

          return 'translate(' + dx + ', ' + dy + ')'
        })
    } else {
      svg.select('.legend').selectAll('*').remove()
    }
  },

  _onRowOver: function (d) {
    var seriesName = this._options.seriesName
    var target = seriesName(d)

    this._svg.selectAll('.row')
      .transition().duration(300)
      .style('opacity', function (e) {
        return (seriesName(e) === target) ? 1 : 0.4
      })
  },

  _onRowOut: function () {
    this._svg.selectAll('.row')
      .transition().duration(300)
      .style('opacity', 1)
  },

  _setSort: function (d) {
    this.sortCol = (d === this.sortCol) ? null : d
    this.update(this._svg.selectAll('.row').data())
  }
})

export default Heatmap
