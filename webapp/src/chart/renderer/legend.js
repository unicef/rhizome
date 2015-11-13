'use strict'

var d3 = require('d3')

function legend () {
  var _clickHandler = null
  var _filled = function () {
    return true
  }
  var _interactive = false
  var _padding = 5
  var _scale = d3.scale.category20b()
  var _size = 7
  var _fontSize = 65
  var _margin = 20

  function fill (d, i) {
    if (!_interactive || _filled(d, i)) {
      return _scale(d)
    }

    return 'transparent'
  }

  function stroke (d, i) {
    return _scale(d)
  }

  function chart (selection) {
    selection.each(function () {
      var g = d3.select(this)
      var series = g.selectAll('.series')
        .data(_scale && _scale.domain ? _scale.domain() : [])

      g.classed('interactive', _interactive)

      var seriesEnter = series.enter()
        .append('g')
        .attr({
          'class': 'series',
          'transform': translate
        })

      seriesEnter.append('rect')
        .attr({
          'width': _size,
          'height': _size
        })

      seriesEnter.append('text')
        .attr({
          'x': _size + _padding,
          'y': _size / 2,
          'dy': '0.4em'
        })

      series
        .on('click', _clickHandler)
        .transition()
        .duration(300)
        .attr('transform', translate)

      series.select('rect')
        .attr({
          'fill': fill,
          'stroke': stroke
        })
        .transition()
        .duration(300)
        .attr({
          'width': _size,
          'height': _size
        })

      series.select('text')
        .text(String)
        .transition()
        .duration(300)
        .attr({
          'x': _size + _padding,
          'y': _size / 2
        })
        .style('font-size', Math.max(_size * 7 / 9, 9))

      series.exit()
        .transition()
        .duration(300)
        .style('opacity', 0)
        .remove()
    })
  }

  chart.clickHandler = function (value) {
    if (!arguments.length) {
      return _clickHandler
    }

    _clickHandler = value
    return chart
  }

  chart.filled = function (value) {
    if (!arguments.length) {
      return _filled
    }

    _filled = value

    return chart
  }

  chart.interactive = function (value) {
    if (!arguments.length) {
      return _interactive
    }

    _interactive = value
    return chart
  }

  chart.padding = function (value) {
    if (!arguments.length) {
      return _padding
    }

    _padding = value
    return chart
  }

  chart.scale = function (value) {
    if (!arguments.length) {
      return _scale
    }

    _scale = value
    return chart
  }

  chart.size = function (value) {
    if (!arguments.length) {
      return _size
    }

    _size = value
    return chart
  }

  function translate (d, i) {
    return i % 2 === 0
      ? 'translate(' + _margin + ', ' + (i / 2 * (_size + _padding)) + ')'
      : 'translate(' + (_fontSize + _size + _margin) + ', ' + ((i - 1) / 2 * (_size + _padding)) + ')'
  }

  return chart
}

module.exports = legend
