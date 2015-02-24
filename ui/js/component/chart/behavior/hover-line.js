'use strict';

var _      = require('lodash');
var d3     = require('d3');

function hoverLine() {
	var datapoints = [];
	var diff       = function (a, b) { return a - b; };
	var height     = 1;
	var seriesName = null;
	var width      = 1;
	var x          = function (d) { return d.x; };
	var xFormat    = String;
	var xScale     = d3.scale.linear();
	var y          = function (d) { return d.y; };
	var yFormat    = String;
	var yScale     = d3.scale.linear();
	var _value     = function (d) {
		return d.value;
	};

	function chart(selection) {
		selection
			.on('mousemove.hoverline', onMouseMove)
			.on('mouseout.hoverline', onMouseOut);
	}

	chart.datapoints = function (value) {
		if (!arguments.length) {
			return datapoints;
		}

		datapoints = value;
		return chart;
	};

	chart.diff = function (value) {
		if (!arguments.length) {
			return diff;
		}

		diff = value;
		return chart;
	};

	chart.xFormat = function (value) {
		if (!arguments.length) {
			return xFormat;
		}

		xFormat = value;
		return chart;
	};

	chart.yFormat = function (value) {
		if (!arguments.length) {
			return yFormat;
		}

		yFormat = value;
		return chart;
	};

	chart.height = function (value) {
		if (!arguments.length) {
			return height;
		}

		height = value;
		return chart;
	};

	chart.seriesName = function (value) {
		if (!arguments.length) {
			return seriesName;
		}

		seriesName = value;
		return chart;
	};

	chart.xScale = function (value) {
		if (!arguments.length) {
			return xScale;
		}

		xScale = value;
		return chart;
	};

	chart.yScale = function (value) {
		if (!arguments.length) {
			return yScale;
		}

		yScale = value;
		return chart;
	};

	chart.width = function (value) {
		if (!arguments.length) {
			return width;
		}

		width = value;
		return chart;
	};

	chart.x = function (value) {
		if (!arguments.length) {
			return x;
		}

		x = value;
		return chart;
	};

	chart.y = function (value) {
		if (!arguments.length) {
			return y;
		}

		y = value;
		return chart;
	};

	chart.value = function (value) {
		if (!arguments.length) {
			return _value;
		}

		_value = value;
		return chart;
	};

	function onMouseMove() {
		/* jshint validthis: true */
		var cursor = d3.mouse(this)[0];

		var range = _(datapoints)
			.map(x)
			.uniq()
			.sortBy()
			.value();

		var val   = xScale.invert(cursor);
		var right = d3.bisect(range, val);
		var left  = right - 1;
		var data  = [];

		if (cursor >= 0 || cursor <= width) {
			if (left < 0) {
				data[0] = range[right];
			} else if (right >= range.length) {
				data[0] = range[left];
			} else {
				var r            = range[right];
				var l            = range[left];
				var closeToRight = (diff(val, l) / diff(r, l) > 0.5);

				data[0] = closeToRight ? range[right] : range[left];
			}
		}

		var svg  = d3.select(this);
		var line = svg.select('.annotation').selectAll('line')
			.data(data);

		line.enter()
			.append('line')
			.style({
				'opacity': 0,
				'stroke': '#ffcc67'
			});

		line
			.attr({
				'y1': 0,
				'y2': height
			})
			.transition()
			.duration(300)
			.attr({
				'x1': xScale,
				'x2': xScale,
			})
			.style('opacity', 1);

		line.exit()
			.transition()
			.duration(300)
			.style('opacity', 0)
			.remove();

		svg.select('.x.axis')
			.transition()
			.duration(300)
			.style('opacity', data.length ? 0 : 1);

		var label = svg
			.select('.annotation')
			.selectAll('.axis')
			.data(data);

		var yTranslate = height;

		label.enter()
			.append('text')
			.style({
				'text-anchor': 'middle',
				'opacity'    : 0
			})
			.attr({
				'dy'       : '9',
				'class'    : 'axis',
				'transform': function (d) {
					return 'translate(' + xScale(d) + ',' + yTranslate + ')';
				}
			});

		label
			.text(function (d) {
				return xFormat(d);
			})
			.transition()
			.duration(300)
			.attr('transform', function (d) {
				return 'translate(' + xScale(d) + ',' + yTranslate + ')';
			})
			.style('opacity', 1);

		label.exit()
			.transition()
			.duration(300)
			.style('opacity', 0)
			.remove();

		var labelData = datapoints.filter(function (d) {
			return x(d) === data[0];
		});

		label = svg
			.select('.annotation')
			.selectAll('.value.label')
			.data(labelData);

		label.enter()
			.append('text')
			.attr({
				'class'    : 'value label',
				'dx'       : '-2',
				'dy'       : '4',
				'transform': function (d) {
					return 'translate(' + xScale(x(d)) + ',' + yScale(y(d)) + ')';
				}
			})
			.style({
				'opacity': 0,
				'text-anchor': 'end'
			});

		label
			.text(function (d) {
				var name = seriesName ? seriesName(d) + ' ' : '';
				return name + yFormat(_value(d));
			})
			.transition()
			.duration(300)
			.attr('transform', function (d) {
				return 'translate(' + xScale(x(d)) + ',' + yScale(y(d)) + ')';
			})
			.style('opacity', 1);

		label.exit()
			.transition()
			.duration(300)
			.style('opacity', 0)
			.remove();

		svg.selectAll('.series.label')
			.transition()
			.duration(300)
			.style('opacity', 0);
	}

	function onMouseOut() {
		/* jshint validthis: true */
		var svg = d3.select(this);

		svg.select('.annotation').selectAll('line, .value, .axis')
			.transition()
			.duration(300)
			.style('opacity', 0)
			.remove();

			svg.select('.x.axis')
				.transition()
				.duration(300)
				.style('opacity', 1);

			svg.selectAll('.annotation .series.label')
				.transition()
				.duration(300)
				.style('opacity', 1);
	}

	return chart;
}

module.exports = hoverLine;
