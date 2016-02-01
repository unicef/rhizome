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
  sourceColumn: _.property('short_name'),
  fontSize: 12,
  format: formatUtil.general,
  headerText: _.property('short_name'),
  headers: [],
  onClick: null,
  onColumnHeadOver: null,
  onColumnHeadOut: null,
  onMouseMove: null,
  onMouseOut: null,
  onRowClick: null,
  seriesName: _.property('name'),
  sortValue: _sortValue,
  values: _.property('values'),
  value: _.property('value'),
  sortDirection: 1
}

function TableChart () {}

_.extend(TableChart.prototype, {
  defaults: DEFAULTS,
  sortCol: null,

  initialize: function (el, data, options) {
    options = this._options = _.defaults({}, options, DEFAULTS)

    var svg = this._svg = d3.select(el)
        .append('svg')
        .attr('class', 'heatmap sortable')

    var g = svg.append('g').attr('class', 'margin')

    g.append('g').attr('class', 'z axis')
    g.append('g').attr('class', 'y axis')
    g.append('g').attr('class', 'x axis')
    g.append('g').attr('class', 'data')
    g.append('g').attr('class', 'source-footer')
    g.append('g').attr('class', 'legend')

    this.update(data)
  },

  update: function (data, options) {
    options = _.extend(this._options, options)
    var margin = options.margin

    var self = this
    var parentLocationMap = options.parentLocationMap
    var w = 3 * Math.max(options.headers.length * options.cellSize, 0)
    var h = Math.max(options.defaultSortOrder.length * options.cellSize, 0)
    var z = 160 //  extra margin space needed to add the "z" (parent) axis"

    // hacky way to sclae the view box.. this shoudl be done by taking into
    // account the user's screen size... needs some time to get 100% right.. //
    var viewBoxHeightScale = 1 + (options.headers.length - 8) / 10
    if (viewBoxHeightScale < 1) {
      viewBoxHeightScale = 1
    }
    var viewBox = '0 0 ' + (w + margin.left + margin.right) + ' ' + ((h * viewBoxHeightScale) + margin.top + margin.bottom)
    var svg = this._svg
      .attr({
        'viewBox': viewBox,
        'width': (w + margin.left + margin.right),
        'height': (h + margin.top + margin.bottom)
      })
      .datum(data)

    var xScale = d3.scale.ordinal()
        .domain(_.map(options.headers, options.headerText))
        .rangeBands([0, w], 0.1)

    var x = _.flow(options.column, xScale)
    var sourceFlow = _.flow(options.sourceColumn, xScale)

    // if there is a sortCol set, order the data that way. //
    if (this.sortCol) {
      let sortValue = _.partial(options.sortValue.bind(this), _, this.sortCol)
      var domain = _(data).sortBy(sortValue, this).map(options.seriesName).value()
    } else {
      // if not, show default.  This also applies to the third click of a header
      domain = options.defaultSortOrder
      this.sortDirection = 1
    }

    if (this.sortDirection === -1) {
      domain = domain.reverse()
    }

    // For empty data points i need to add the x axis domain items explicitly //
    // otherwise the domain will be less ( and different the ) the yScale //
    // see trello : https://trello.com/c/bCwyqSWs/277-display-bug-when-creating-table-chart //
    if (domain.length < options.defaultSortOrder.length) {
      var diff = options.defaultSortOrder.filter(function (x) {
        return domain.indexOf(x) < 0
      })
      domain = domain.concat(diff)
    }

    var yScale = d3.scale.ordinal()
      .domain(domain)
      .rangeBands([0, h], 0.1)

    var y = _.flow(options.seriesName, yScale)

    var transform = function (d, i) {
      var yVal = y(d) + 10
      return 'translate(' + z + ' , ' + yVal + ')'
    }

    // THIS SETS THE COLOR... MOVE FROM HERE ONCE THE USER CAN SET A PALLETTE
    var targets = _(options.headers)
      .indexBy('id')
      .mapValues(ind => {
        var extents = [ ind.low_bound, ind.high_bound ]
        var names = ['bad', 'ok', 'good']

        if (ind.low_bound > ind.high_bound) {
          names = ['good', 'ok', 'bad']
        }

        return d3.scale.threshold()
          .domain(extents)
          .range(names)
      })
      .value()

    var scale = d3.scale.ordinal()
      .domain(['bad', 'ok', 'good'])
      .range(['#DB5344', '#79909F', '#2FB0D3'])

    var fill = d => scale(_.get(targets, d.indicator.id, _.noop)(d.value))

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

    var cg = cell.enter().append('g')

    cg.append('rect')
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

    cg.append('text')
          .attr({
            'height': yScale.rangeBand(),
            'x': function (d) { return x(d) + xScale.rangeBand() / 2 },
            'y': options.cellSize / 2,
            'width': xScale.rangeBand(),
            'dominant-baseline': 'central',
            'text-anchor': 'middle',
            'font-weight': 'bold'
          })
          .style({'font-size': options.cellFontSize})
          .text(function (d) { return d.displayValue })
          .transition()
          .duration(500)

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

    // Begin X Axis //

    svg.select('.x.axis')
      .transition().duration(500)
      .attr({'transform': 'translate(' + z + ',0)'})
      .call(d3.svg.axis()
        .scale(xScale)
        .orient('top')
        .outerTickSize(0))

    svg.selectAll('.x.axis text')
      .on('click', function (d, i) { self._setSort(d, i) })

    svg.selectAll('.x.axis text').call(this._wrap, xScale.rangeBand())

    // the z axis shows the parent location//
    svg.select('.z.axis')
      .transition().duration(500)
      .attr({'transform': 'translate(0,10)'})
      .call(d3.svg.axis()
        .scale(yScale)
        .tickFormat(function (d) {
          return parentLocationMap[d].parent_location__name
        })
        .orient('left')
        .outerTickSize(0))

    svg.selectAll('.z.axis text')
      .style('font-size', options.fontSize)
      .on('click', function (d, i) {
        options.onRowClick(d, i, this)
      })

    svg.select('.y.axis')
      .transition().duration(500)
      .attr({'transform': 'translate(' + z + ',10)'})
      .call(d3.svg.axis()
        .scale(yScale)
        .orient('left')
        .outerTickSize(0))

    svg.selectAll('.y.axis text')
      .style('font-size', options.fontSize)
      .on('click', function (d, i) {
        options.onRowClick(d, i, this)
      })

    // BEGIN SOURCE FOOTER //

    var singleRowIndicators = options.headers // chartData[0].values
    var sourceFooter = svg.select('.source-footer').attr({'transform': 'translate(0,' + 10 + ')'})
    var sourceCell = sourceFooter.selectAll('.source-cell').data(singleRowIndicators)
    var sourceG = sourceCell.enter().append('g')

    sourceG.append('rect')
        .attr({
          'class': 'cell',
          'height': yScale.rangeBand() * 1.5,
          'transform': 'translate(' + z + ',' + h + ')',
          'x': sourceFlow,
          'width': xScale.rangeBand()
        })
        .style({
          'opacity': 0,
          'fill': '#F1F1F1'
        })
        .transition()
        .duration(500)
      .style('opacity', 1)

    sourceG.append('text')
            .attr({
              'height': yScale.rangeBand(),
              'transform': 'translate(' + z + ',' + h + ')',
              'x': function (d) { return sourceFlow(d) + 45 },
              'y': options.cellSize / 2,
              'width': xScale.rangeBand(),
              'dominant-baseline': 'central',
              'text-anchor': 'middle',
              'font-weight': 'bold'
            })
            .text(function (d) { return d.source_name })
              .transition()
              .duration(500)

    // END SOURCE FOOTER //

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

  _wrap: function (text, width) {
    text.each(function () {
      var text = d3.select(this)
      var words = text.text().split(/\s+/)
      var line = []
      var lineNumber = 0
      var lineHeight = 1.1 // ems
      var y = text.attr('y') - 10
      var dy = parseFloat(text.attr('dy'))
      var tspan = text.text(null).append('tspan').attr('x', 0).attr('y', y).attr('dy', dy + 'em')
      var i = 0
      for (i = 0; i < words.length; i += 1) {
        var word = words[i]
        line.push(word)
        tspan.text(line.join(' '))
        if (tspan.node().getComputedTextLength() > width) {
          line.pop()
          tspan.text(line.join(' '))
          line = [word]
          tspan = text.append('tspan').attr('x', 0).attr('y', y).attr('dy', ++lineNumber * lineHeight + dy + 'em').text(word)
        }
      }
    })
  },

  _onRowOver: function (d) {
    var seriesName = this._options.seriesName
    this._svg.selectAll('.row')
      .transition().duration(300)
      .style('opacity', function (e) {
        return (seriesName(e) === d[0].name) ? 1 : 0.4
      })
  },

  _onRowOut: function () {
    this._svg.selectAll('.row')
      .transition().duration(300)
      .style('opacity', 1)
  },

  _setSort: function (d) {
    // Fist click, order ascending, Second order descending, third order default
    if (d === this.sortCol && this.sortDirection === -1) {
      this.sortCol = null
    } else if (d === this.sortCol && this.sortDirection === 1) {
      this.sortCol = d
      this.sortDirection = -1
    } else {
      this.sortCol = d
      this.sortDirection = 1
    }

    this.update(this._svg.selectAll('.row').data())
  }
})

export default TableChart
