import _ from 'lodash'
import d3 from 'd3'

const TableHelpers = {

  getDomain (data, options) {
      // if there is a sortCol set, order the data that way.
      if (this.sortCol) {
        let sortValue = _.partial(options.sortValue.bind(this), _, this.sortCol)
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
  },

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
  },

  onRowOver (d) {
    var seriesName = this._options.seriesName
    this._svg.selectAll('.row')
      .transition().duration(300)
      .style('cursor', 'pointer')
      .style('opacity', e => seriesName(e) === d[0].name ? 1 : 0.3)
  },

  onRowClick (d) {
    // console.log('row clicked', d)
  },

  onRowOut () {
    this._svg.selectAll('.row')
      .transition().duration(300)
      .style('opacity', 1)
  },

  setSort (d) {
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
  },

  sortValue (s, sortCol) {
    const options = this._options
    if (sortCol === null) {
      return options.seriesName(s)
    }
    return options.value(_.find(options.values(s), d => options.column(d) === sortCol))
  }
}

export default TableHelpers
