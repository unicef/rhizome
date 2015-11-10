'use strict'

var _ = require('lodash')
var d3 = require('d3')

var label = require('../renderer/label')

function hoverLine () {
    var datapoints = []
    var diff = function (a, b) { return a - b }
    var height = 1
    var seriesName = null
    var _sort = false
    var top = 0
    var width = 1
    var x = function (d) { return d.x }
    var xFormat = String
    var xScale = d3.scale.linear()
    var y = function (d) { return d.y }
    var yFormat = String
    var yScale = d3.scale.linear()
    var _value = _.property('value')
  var colorRange = '#000000'

    // Use this to keep track of what value we're currently hovering over so we
    // can bail out of onMouseMove if the movement wouldn't change our display
    var _currentTarget = null

    function chart (selection) {
        selection
            .on('mousemove.hoverline', onMouseMove)
            .on('mouseout.hoverline', onMouseOut)
    }

    chart.datapoints = function (value) {
        if (!arguments.length) {
            return datapoints
        }

        datapoints = value
        return chart
    }

    chart.xFormat = function (value) {
        if (!arguments.length) {
            return xFormat
        }

        xFormat = value
        return chart
    }

    chart.yFormat = function (value) {
        if (!arguments.length) {
            return yFormat
        }

        yFormat = value
        return chart
    }

    chart.height = function (value) {
        if (!arguments.length) {
            return height
        }

        height = value
        return chart
    }

    chart.seriesName = function (value) {
        if (!arguments.length) {
            return seriesName
        }

        seriesName = value
        return chart
    }

    chart.sort = function (value) {
        if (!arguments.length) {
            return _sort
        }

        _sort = value
        return chart
    }

    chart.top = function (value) {
        if (!arguments.length) {
            return top
        }

        top = value
        return chart
    }

    chart.xScale = function (value) {
        if (!arguments.length) {
            return xScale
        }

        xScale = value
        return chart
    }

    chart.yScale = function (value) {
        if (!arguments.length) {
            return yScale
        }

        yScale = value
        return chart
    }

    chart.width = function (value) {
        if (!arguments.length) {
            return width
        }

        width = value
        return chart
    }

    chart.x = function (value) {
        if (!arguments.length) {
            return x
        }

        x = value
        return chart
    }

    chart.y = function (value) {
        if (!arguments.length) {
            return y
        }

        y = value
        return chart
    }

    chart.value = function (value) {
        if (!arguments.length) {
            return _value
        }

        _value = value
        return chart
    }

  chart.colorRange = function (value) {
    if (!arguments.length) {
      return colorRange
    }

    colorRange = value
    return chart
  }

    function axisTranslate (d) {
        // jshint validthis:true
        var box = this.getBBox()
        var min = box.width / 2
        var max = width - min

        return 'translate(' +
            Math.max(min, Math.min(max, d)) + ', ' +
            height + ')'
    }

    function onMouseMove () {
        /* jshint validthis: true */
        var cursor = d3.mouse(this)[0]

        var range = _(datapoints)
            .map(_.flow(x, xScale))
            .uniq()
            .sortBy()
            .value()

        var right = d3.bisect(range, cursor)
        var left = right - 1
        var data = []

        if (cursor >= 0 || cursor <= width) {
            if (left < 0) {
                data[0] = range[right]
            } else if (right >= range.length) {
                data[0] = range[left]
            } else {
                var r = range[right]
                var l = range[left]
                var closeToRight = (diff(cursor, l) / diff(r, l) > 0.5)

                data[0] = closeToRight ? range[right] : range[left]
            }
        }

        if (data[0] === _currentTarget) {
            return
        }

        _currentTarget = data[0]

        var svg = d3.select(this)
        var line = svg.select('.annotation').selectAll('line')
            .data(data)

        line.enter()
            .append('line')
            .style({
                'opacity': 0,
                'stroke': '#495356'
            })

        line
            .attr({
                'y1': top,
                'y2': height
            })
            .transition()
            .duration(300)
            .attr({
                'x1': Number,
                'x2': Number
            })
            .style('opacity', 1)

        line.exit()
            .transition()
            .duration(300)
            .style('opacity', 0)
            .remove()

        svg.selectAll('.x.axis text')
            .transition()
            .duration(300)
            .style('opacity', data.length ? 0 : 1)

        // X-axis label
        var xLabel = svg
            .select('.annotation')
            .selectAll('.axis')
            .data(data)

        xLabel.enter()
            .append('text')
            .style({
                'text-anchor': 'middle',
                'opacity': 0
            })
            .attr({
                'dy': '9',
                'class': 'axis',
                'transform': axisTranslate
            })

        xLabel
            .text(function (d) {
                return xFormat(xScale.invert(d))
            })
            .transition()
            .duration(300)
            .attr('transform', axisTranslate)
      .attr({
        'dy': '.71em',
        'y': '9'
      })
            .style('opacity', 1)

        xLabel.exit()
            .transition()
            .duration(300)
            .style('opacity', 0)
            .remove()

        var labelData = _(datapoints)
            .filter(function (d) {
                return xScale(x(d)) === data[0]
            })
            .map(function (d) {
                var name = seriesName ? seriesName(d) + ' ' : ''

                return {
                    x: xScale(x(d)),
                    y: yScale(y(d)),
                    text: name + yFormat(_value(d))
                }
            })
            .value()

        if (_sort) {
            labelData.sort(function (a, b) {
                return a.y - b.y
            })
        } else {
            labelData.reverse()
        }

        // Use a g element to position the labels horizontally at the same
        // position based on the width of the longest label
        var labelGroup = svg.select('.annotation')
            .selectAll('.label-group')
            .data([labelData])

        labelGroup.enter()
            .append('g')
            .attr('class', 'label-group')

    var colorScale = d3.scale.ordinal()
        .domain(_(labelData)
        .map(function (d)  { return d.text })
        .uniq()
        .sortBy()
        .value())
        .range(colorRange)

    var color = _.flow(function (d) { return d.text }, colorScale)

        labelGroup.selectAll('.hover.label')
            .data(function (d) { return d })
            .call(label().addClass('hover').width(width).height(height).scale(color))

            // Determine the label orientation based on the bounding box. We prefer
            // left-aligned, but if that gets cut off, we will right-align the text
            // var box = this.getBBox()
            // var pos = xScale(data[0])
            // var anchor = (pos + box.width + 2) < width ? 'start' : 'end'

        svg.selectAll('.series.label')
            .transition()
            .duration(300)
            .style('opacity', 0)
    }

    function onMouseOut () {
        /* jshint validthis: true */
        var svg = d3.select(this)

        _currentTarget = null

        svg.select('.annotation').selectAll('line, .hover.label, .axis')
            .transition()
            .duration(300)
            .style('opacity', 0)
            .remove()

    svg.selectAll('.x.axis text')
      .transition()
      .duration(300)
      .style('opacity', 1)

    svg.selectAll('.annotation .series.label')
      .transition()
      .duration(300)
      .style('opacity', 1)
    }

    return chart
}

module.exports = hoverLine
