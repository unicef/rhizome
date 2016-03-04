import _ from 'lodash'
import d3 from 'd3'
import palettes from '00-utilities/palettes'
import formatUtil from '02-molecules/charts_d3/utils/format'

var DEFAULTS = {
  cellSize: 16,
  column: _.property('indicator.short_name'),
  color: palettes.blue,
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
    console.log('INIT - data', data)
    console.log('INIT - options', options)
    options = this._options = _.defaults({}, options, DEFAULTS)
    const svg = this._svg = d3.select(el).append('svg').attr('class', 'heatmap sortable')
    const g = svg.append('g').attr('class', 'margin')
    g.append('g').attr('class', 'z axis')
    g.append('g').attr('class', 'y axis')
    g.append('g').attr('class', 'x axis')
    g.append('g').attr('class', 'data')
    g.append('g').attr('class', 'source-footer')
    g.append('g').attr('class', 'legend')

    this.update(data, options)
  },

  update: function (data, options) {
    options = _.extend(this._options, options)

    const h = Math.max(data.length * options.cellSize, 0)
    const z = 160 //  extra margin space needed to add the "z" (parent) axis"
    const w = 3 * Math.max(options.headers.length * options.cellSize, 0)
    const xDomainProvided = typeof (options.xDomain) !== 'undefined' && options.xDomain.length > 0
    const xDomain = xDomainProvided ? options.xDomain : options.indicatorsSelected.map(ind => { return ind.short_name })
    const xScale = d3.scale.ordinal().domain(xDomain).rangeBands([0, w], 0.1)
    const sourceFlow = _.flow(options.sourceColumn, xScale)
    const x = _.flow(options.column, xScale)
    console.log('x', x)
    console.log('w', w)
    console.log('xScale', xScale)
    console.log('xScale.rangeBand()', xScale.rangeBand())
    console.log('xDomain', xDomain)
    console.log('options.headers', options.headers)
    const margin = options.margin
    const scale = d3.scale.ordinal().domain(['bad', 'ok', 'good']).range(options.color)

    const domain = this._getDomain(data, options)
    const yScale = d3.scale.ordinal().domain(domain).rangeBands([0, h], 0.1)
    const y = _.flow(options.seriesName, yScale)
    const transform = (d, i) => (`translate(${z}, ${y(d) + 10})`)

    // COLORS - Move from here once the user can set a pallette
    // ---------------------------------------------------------------------------
    const targets = _(options.headers)
      .indexBy('id')
      .mapValues(ind => {
        const extents = [ ind.bad_bound, ind.good_bound ]
        const boundsReversed = ind.bad_bound > ind.good_bound
        const names = boundsReversed ? ['good', 'ok', 'bad'] : ['bad', 'ok', 'good']
        return d3.scale.threshold().domain(extents).range(names)
      })
      .value()

    // CONTAINER
    // ---------------------------------------------------------------------------
    // hacky way to scale the view box.. this should be done by taking into account the user's screen size
    const calculatedHeightScale = 1 + (options.headers.length - 8) / 10
    const viewBoxHeightScale = calculatedHeightScale < 1 ? calculatedHeightScale : 1
    const viewBox = '0 0 ' + (w + margin.left + margin.right) + ' ' + ((h * viewBoxHeightScale) + margin.top + margin.bottom)
    const svg = this._svg
      .attr({
        'viewBox': viewBox,
        'width': (w + margin.left + margin.right),
        'height': (h + margin.top + margin.bottom)
      })
      .datum(data)

    svg.select('.margin').attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')')

    const g = svg.select('.data')
    g.on('mouseout', () => { this._onRowOut.apply(this) })

    // ROWS
    // ---------------------------------------------------------------------------
    const rows = g.selectAll('.row').data(data)
    rows.enter().append('g').attr({'class': 'row', 'transform': transform})
    rows.exit().transition().duration(300).style('opacity', 0).remove()
    rows.on('click', (d, i) => { this._onRowClick([d, i]) })
    rows.on('mouseover', (d, i) => { this._onRowOver([d, i]) }).transition().duration(750).attr('transform', transform)

    // CELLS
    // ---------------------------------------------------------------------------

    const fill = d => scale(_.get(targets, d.indicator.id, _.noop)(d.value))
    const cells = rows.selectAll('.cell').data(options.values)
    cells.exit().transition().duration(300).style('opacity', 0).remove()
    cells.attr('id', d => [d.location.name, d.indicator.short_name].join('-'))
    cells.style('cursor', _.isFunction(options.onClick) ? 'pointer' : 'initial')
    cells.on('mousemove', options.onMouseMove)
    cells.on('mouseout', options.onMouseOut)
    cells.on('click', options.onClick)
    cells.transition().duration(500).style('fill', fill)
      .attr({
        'height': yScale.rangeBand(),
        'width': xScale.rangeBand(),
        'x': x
      })

    const cg = cells.enter().append('g')
    // console.log('x', x)
    cg.append('rect')
      .attr({
        'class': 'cell',
        'height': yScale.rangeBand(),
        'x': x,
        'width': xScale.rangeBand()
      })
      .style({ 'opacity': 0, 'fill': fill })
      .transition().duration(500)
      .style('opacity', 1)

    cg.append('text')
      .attr({
        'height': yScale.rangeBand(),
        // 'x': d => {
        //   const columnResult = options.column(d)
        //   const xScaleResult = xScale(columnResult)
        //   // const xScale = d3.scale.ordinal().domain(xDomain).rangeBands([0, w], 0.1)
        //   if (!xScaleResult) {
        //     console.log('Something went wrong!!!!')
        //     console.log('d', d)
        //     console.log('w', w)
        //     console.log('columnResult', columnResult)
        //     console.log('d3.scale.ordinal(columnResult)', d3.scale.ordinal(columnResult))
        //     console.log('d3.scale.ordinal().domain(xDomain)', d3.scale.ordinal(columnResult).domain(xDomain))
        //     console.log('d3.scale.ordinal().domain(xDomain).rangeBands()', d3.scale.ordinal().domain(columnResult).rangeBands([0, 1296], 0.1))
        //     console.log('xScaleResult', xScaleResult)
        //   } else {
        //     console.log('something went right')
        //   }

        //   // console.log('x(d)', x(d))
        //   // return x(d) + xScale.rangeBand() / 2
        //   return 700
        // },
        'x': x + xScale.rangeBand() / 2,
        'y': options.cellSize / 2,
        'width': xScale.rangeBand(),
        'dominant-baseline': 'central',
        'text-anchor': 'middle',
        'font-weight': 'bold'
      })
      .style({'font-size': options.cellFontSize})
      .text(d => { return d.displayValue })
      .transition().duration(500)

    // X AXIS
    // ---------------------------------------------------------------------------
    svg.select('.x.axis')
      .transition().duration(500)
      .attr({'transform': 'translate(' + z + ',0)'})
      .call(d3.svg.axis().scale(xScale).orient('top').outerTickSize(0))
    svg.selectAll('.x.axis text').on('click', (d, i) => { this._setSort(d, i) })
    svg.selectAll('.x.axis text').call(this._wrap, xScale.rangeBand())

    // Y AXIS
    // ---------------------------------------------------------------------------
    svg.select('.y.axis')
      .transition().duration(500)
      .attr({'transform': 'translate(' + z + ',10)'})
      .call(d3.svg.axis().scale(yScale).orient('left').outerTickSize(0))
    svg.selectAll('.y.axis text')
      .style('font-size', options.fontSize)
      .on('click', (d, i) => { options.onRowClick(d, i, this) })

    // Z AXIS
    // ---------------------------------------------------------------------------
    // the z axis shows the parent location//
    // svg.select('.z.axis')
    //   .transition().duration(500)
    //   .attr({'transform': 'translate(0,10)'})
    //   .call(d3.svg.axis()
    //     .scale(yScale)
    //     .tickFormat(d => { return options.parentLocationMap[d].parent_location__name })
    //     .orient('left')
    //     .outerTickSize(0))
    // svg.selectAll('.z.axis text')
    //   .style('font-size', options.fontSize)
    //   .on('click', (d, i) => { options.onRowClick(d, i, this) })

    // FOOTER
    // ---------------------------------------------------------------------------
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
      .style({ 'opacity': 0, 'fill': '#F1F1F1' })
      .transition().duration(500)
      .style('opacity', 1)

    sourceG.append('text')
      .attr({
        'height': yScale.rangeBand(),
        'transform': 'translate(' + z + ',' + h + ')',
        'x': d => { return sourceFlow(d) + 45 },
        'y': options.cellSize / 2,
        'width': xScale.rangeBand(),
        'dominant-baseline': 'central',
        'text-anchor': 'middle',
        'font-weight': 'bold'
      })
      .text(d => { return d.source_name })
      .transition().duration(500)
      .call(this._wrap, xScale.rangeBand())

    // LEGEND
    // ---------------------------------------------------------------------------
    if (options.legend) {
      svg.select('.legend')
        .call(options.legend)
        .attr('transform', () => {
          const bbox = this.getBoundingClientRect()
          const dx = w + margin.right - bbox.width
          return `translate(${dx}, 0)`
        })
    } else {
      svg.select('.legend').selectAll('*').remove()
    }
  },

  _getDomain: function (data, options) {
    // if there is a sortCol set, order the data that way.
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
      const diff = options.defaultSortOrder.filter(x => { return domain.indexOf(x) < 0 })
      domain = domain.concat(diff)
    }

    return domain
  },

  _wrap: function (text, width) {
    text.each(function () {
      var text = d3.select(this)
      var words = text.text().split(/\s+/)
      var line = []
      var lineNumber = 0
      var lineHeight = 1.1 // ems
      var y = text.attr('y') - 10
      var x = text.attr('x') !== null ? text.attr('x') : 0
      var dy = 0
      var tspan = text.text(null).append('tspan').attr('x', x).attr('y', y).attr('dy', dy + 'em')
      var i = 0
      for (i = 0; i < words.length; i += 1) {
        var word = words[i]
        line.push(word)
        tspan.text(line.join(' '))
        if (tspan.node().getComputedTextLength() > width) {
          line.pop()
          tspan.text(line.join(' '))
          line = [word]
          tspan = text.append('tspan').attr('x', x).attr('y', y).attr('dy', ++lineNumber * lineHeight + dy + 'em').text(word)
        }
      }
    })
  },

  _onRowOver: function (d) {
    var seriesName = this._options.seriesName
    this._svg.selectAll('.row')
      .transition().duration(300)
      .style('cursor', 'pointer')
      .style('opacity', function (e) {
        return (seriesName(e) === d[0].name) ? 1 : 0.4
      })
  },
  _onRowClick: function (d) {
    console.log('row clicked', d)
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

function _sortValue (s, sortCol) {
  const options = this._options
  if (sortCol === null) {
    return options.seriesName(s)
  }
  return options.value(_.find(options.values(s), d => options.column(d) === sortCol))
}

export default TableChart
