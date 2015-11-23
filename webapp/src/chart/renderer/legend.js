import d3 from 'd3'
import _ from 'lodash'

function legend (chartOptions) {
  var _clickHandler = null

  var _filled = function () {
    return true
  }

  var _interactive = false
  var _padding = 6
  var _scale = d3.scale.category20b()
  var _size = 8
  var _fontSize = 65

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
      var data = _scale && _scale.domain ? _scale.domain() : []
      var series = g.selectAll('.series')
        .data(data)

      let length = data[0].length

      g.classed('interactive', _interactive)

      var seriesEnter = series.enter()
        .append('g')
        .attr({
          'class': 'series',
          'transform': _.partial(translate, _, _, length)
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
        .attr('transform', _.partial(translate, _, _, length))

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
        .style('font-size', _size + 2)

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

  chart.fontSize = function (value) {
    if (!arguments.length) {
      return _fontSize
    }

    _fontSize = value
    return chart
  }

  function translate (d, i, length) {
    if (chart.chartOptions && chart.chartOptions.chartInDashboard) {
      return 'translate(0, ' + (i / 2 * (_size + _padding * 4)) + ')'
    }
    length = length % 2 === 0 ? length : length + 1

    return i < length / 2
      ? 'translate(' + 0 + ', ' + (i * (_size + _padding)) + ')'
      : 'translate(' + (_fontSize + _size) + ', ' + ((i - length / 2) * (_size + _padding)) + ')'
  }

  chart.chartOptions = chartOptions

  return chart
}

export default legend
