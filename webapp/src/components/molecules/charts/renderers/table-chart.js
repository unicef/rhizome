import _ from 'lodash'
import d3 from 'd3'

class TableChartRenderer {

  constructor (data, options, container) {
    this.setTableParams(data, options, container)
  }

  setTableParams (data, options, container) {
    this.container = container
    this.options = options
    this.data = data
    this.h = Math.max(options.default_sort_order.length * options.cellHeight, 0)
    this.z = 160 //  extra margin space needed to add the "z" (parent) axis
    this.w = 3.5 * Math.max(options.headers.length * options.cellHeight, 0)
    this.xDomainProvided = typeof (options.xDomain) !== 'undefined' && options.xDomain.length > 0
    this.xDomain = this.xDomainProvided ? options.xDomain : options.headers.map(ind => ind.short_name)
    this.xScale = d3.scale.ordinal().domain(this.xDomain).rangeBands([0, this.w], 0.1)
    this.sourceFlow = _.flow(options.sourceColumn, this.xScale)
    this.x = _.flow(options.column, this.xScale)
    this.margin = options.margin
    this.scale = d3.scale.ordinal().domain(['bad', 'ok', 'good']).range(options.colors)
    this.domain = this.getDomain(data, options)
    this.yScale = d3.scale.ordinal().domain(this.domain).rangeBands([0, this.h], 0.1)
    this.y = _.flow(options.seriesName, this.yScale)
    this.transform = (d, i) => `translate(${this.z}, ${this.y(d) + 10})`
    this.targets = this.getTargets(options.headers)
    this.fill = d => !_.isNull(d.value) && _.isFinite(d.value) ? this.scale(this.targets[d.indicator.id](d.value)) : '#FFFFFF'
    this.svg = d3.select(container)
  }

  update (data, options, container) {
    this.setTableParams(data, options, container)
    this.render()
  }

  render () {
    this.prepContainer()
    this.renderRows()
    this.renderCells()
    this.renderXAxis()
    this.renderYAxis()
    this.renderZAxis()
    this.renderFooter()
    this.renderLegend()
  }

  // =========================================================================== //
  //                                    RENDER                                   //
  // =========================================================================== //
  prepContainer () {
    const svgHeight = this.margin.top + this.margin.bottom + this.h
    const viewBox = '0 0 ' + this.w + ' ' + svgHeight
    this.svg.attr({
      'viewBox': viewBox,
      'width': this.w,
      'height': this.margin.top + this.margin.bottom + this.h
    })
   .datum(this.data)
    this.svg.select('.margin').attr('transform', 'translate(0, ' + this.margin.top + ')')
  }

  // ROWS
  // ---------------------------------------------------------------------------
  renderRows () {
    const g = this.svg.select('.data')
    g.on('mouseout', () => this.onRowOut.apply(this))
    const rows = g.selectAll('.row').data(this.data)
    rows.enter().append('g').attr({'class': 'row', 'transform': this.transform})
    rows.exit().transition().duration(300).style('opacity', 0).remove()
    rows.on('click', (d, i) => this.onRowClick([d, i]))
    rows.on('mouseover', (d, i) => this.onRowOver([d, i]))
      .transition().duration(750)
      .attr('transform', this.transform)
      .attr('pointer-events', 'none')
      .each('end', () => rows.attr('pointer-events', null))
    this.rows = rows
  }

  // CELLS
  // ---------------------------------------------------------------------------
  renderCells () {
    const cells = this.rows.selectAll('.cell').data(this.options.values)
    cells.exit().transition().duration(300).style('opacity', 0).remove()
    cells.attr('id', d => [d.location.name, d.indicator.short_name].join('-'))
    cells.style('cursor', _.isFunction(this.options.onClick) ? 'pointer' : 'initial')
    cells.on('mousemove', this.options.onMouseMove)
    cells.on('mouseout', this.options.onMouseOut)
    cells.on('click', this.options.onClick)
    cells.transition().duration(500).style('fill', this.fill)
      .attr({
        'height': this.yScale.rangeBand(),
        'width': this.xScale.rangeBand(),
        'x': this.x
      })

    const cg = cells.enter().append('g')
    cg.append('rect')
      .attr({
        'class': 'cell',
        'height': this.yScale.rangeBand(),
        'x': this.x,
        'width': this.xScale.rangeBand()
      })
      .style({ 'opacity': 0, 'fill': this.fill })
      .transition().duration(500)
      .style('opacity', 1)
    cg.append('text')
      .attr({
        'height': this.yScale.rangeBand(),
        'x': d => this.x(d) + this.xScale.rangeBand() / 2,
        'y': (this.options.cellHeight / 2) - (this.options.cellFontSize / 4.3),
        'width': this.xScale.rangeBand(),
        'dominant-baseline': 'central',
        'text-anchor': 'middle',
        'font-weight': 'bold'
      })
      .style({'font-size': this.options.cellFontSize})
      .text(d => d.displayValue)
      .transition().duration(500)
  }

  // X AXIS
  // ---------------------------------------------------------------------------
  renderXAxis () {
    this.svg.select('.x.axis')
      .transition().duration(500)
      .attr({'transform': 'translate(' + this.z + ',-40)'})
      .call(d3.svg.axis().scale(this.xScale).orient('top').outerTickSize(0))
    this.svg.selectAll('.x.axis text').on('click', (d, i) => this.onSetSort(d, i))
    this.svg.selectAll('.x.axis text')
      .call(this.wrap, this.xScale.rangeBand())
  }

  // Y AXIS
  // ---------------------------------------------------------------------------
  renderYAxis () {
    this.svg.select('.y.axis')
      .transition().duration(500)
      .attr({'transform': 'translate(' + this.z + ',10)'})
      .call(d3.svg.axis().scale(this.yScale).orient('left').outerTickSize(0))
    this.svg.selectAll('.y.axis text')
      .style('font-size', this.options.fontSize + 2)
      .on('click', (d, i) => this.options.onRowClick(d, i, this))
  }

  // Z AXIS
  // ---------------------------------------------------------------------------
  renderZAxis () {
    this.svg.select('.z.axis')
      .transition().duration(500)
      .attr({'transform': 'translate(20,10)'})
      .call(d3.svg.axis()
        .scale(this.yScale)
        .tickFormat(d => this.options.parent_location_map[d].parent_location__name)
        .orient('left')
        .outerTickSize(0))
    this.svg.selectAll('.z.axis text')
      .style('font-size', this.options.fontSize)
      .on('click', (d, i) => this.options.onRowClick(this.options.parent_location_map[d].parent_location__name, i, this))
  }

  // FOOTER
  // ---------------------------------------------------------------------------
  renderFooter () {
    const singleRowIndicators = this.options.headers // chartData[0].values
    const sourceFooter = this.svg.select('.source-footer').attr({'transform': 'translate(0,' + 10 + ')'})
    const sourceCell = sourceFooter.selectAll('.source-cell').data(singleRowIndicators)
    const sourceG = sourceCell.enter().append('g')
    sourceG.append('rect')
      .attr({
        'class': 'cell',
        'height': this.yScale.rangeBand() * 1.5,
        'transform': `translate(${this.z}, ${this.h})`,
        'x': this.sourceFlow,
        'width': this.xScale.rangeBand()
      })
      .style({ 'opacity': 0 })

    sourceG.append('text')
      .attr({
        'height': this.yScale.rangeBand(),
        'transform': `translate(${this.z + 16}, ${this.h + 5})`,
        'x': d => this.sourceFlow(d) + this.options.cellHeight * 1.33,
        'y': this.options.cellHeight / 2,
        'width': this.xScale.rangeBand(),
        'dominant-baseline': 'central',
        'text-anchor': 'middle',
        'font-weight': 'bold'
      })
      .text(d => d.source_name)
      .transition().duration(500)
      .call(this.wrap, this.xScale.rangeBand())
  }

  // LEGEND
  // ---------------------------------------------------------------------------
  renderLegend () {
    if (this.options.legend) {
      this.svg.select('.legend')
        .call(this.options.legend)
        .attr('transform', () => {
          const bbox = this.getBoundingClientRect()
          const dx = this.w + this.margin.right - bbox.width
          return `translate(${dx}, 0)`
        })
    } else {
      this.svg.select('.legend').selectAll('*').remove()
    }
  }

  // =========================================================================== //
  //                                EVENT HANDLERS                               //
  // =========================================================================== //
  onRowOver (d) {
    this.rows
      .transition().duration(300)
      .style('cursor', 'pointer')
      .style('opacity', e => this.options.seriesName(e) === d[0].name ? 1 : 0.3)
  }

  onRowClick (d) {
    // console.log('row clicked', d)
  }

  onRowOut () {
    this.rows.transition().duration(300).style('opacity', 1)
  }

  onSetSort (d) {
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

    this.update(this.data, this.options, this.container)
  }

  // =========================================================================== //
  //                                     UTILITIES                               //
  // =========================================================================== //
  getTargets (headers) {
    // COLORS - Move from here once the user can set a pallette
    // ---------------------------------------------------------------------------
    return _(headers).indexBy('id').mapValues(ind => {
      const boundsReversed = ind.bad_bound > ind.good_bound
      const names = boundsReversed ? ['good', 'ok', 'bad'] : ['bad', 'ok', 'good']
      const extents = boundsReversed ? [ ind.good_bound, ind.bad_bound ] : [ ind.bad_bound, ind.good_bound ]
      return d3.scale.threshold().domain(extents).range(names)
    })
    .value()
  }

  getDomain (data, options) {
    // if there is a sortCol set, order the data that way.
    if (this.sortCol) {
      let sortValue = _.partial(this.getSortValue.bind(this), _, this.sortCol)
      var domain = _(data).sortBy(sortValue, this).map(options.seriesName).value()
    } else {
      // if not, show default.  This also applies to the third click of a header
      domain = options.default_sort_order
      this.sortDirection = 1
    }
    if (this.sortDirection === -1) {
      domain = domain.reverse()
    }

    // For empty data points i need to add the x axis domain items explicitly //
    // otherwise the domain will be less ( and different the ) the yScale //
    // see trello : https://trello.com/c/bCwyqSWs/277-display-bug-when-creating-table-chart //
    if (domain.length < options.default_sort_order.length) {
      const diff = options.default_sort_order.filter(x => domain.indexOf(x) < 0)
      domain = domain.concat(diff)
    }

    return domain
  }

  getSortValue (s, sortCol) {
    const options = this.options
    if (sortCol === null) {
      return options.seriesName(s)
    }
    return options.value(_.find(options.values(s), d => {
      if (d.value === null || !_.isFinite(d.value)) {
        d.value = this.sortDirection !== 1 ? -Infinity : Infinity
      }
      return options.column(d) === sortCol
    }))
  }

  wrap (text, width) {
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
  }

}

export default TableChartRenderer
