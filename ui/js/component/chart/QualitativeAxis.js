'use strict';

var _  = require('lodash');
var d3 = require('d3');

function qualitativeAxis () {
	var _height = 0;
	var _ticks  = [];
	var _width  = 0;
	var _x      = _.constant(0);
	var _y      = _.constant(0);

	function axis(selection) {
		selection.each(function () {
			var tick = d3.select(this).selectAll('.tick')
				.data(_ticks);

			tick.enter()
				.append('g')
				.attr('class', 'tick');

			tick.exit().remove();

			tick.attr('transform', function () {
				return 'translate(' + _x.apply(this, arguments) + ',' +
					_y.apply(this, arguments) + ')';
			});

			var rect = tick.selectAll('rect').data(_.identity);

			rect.enter().append('rect');

			rect.attr({
				'width'  : _width,
				'height' : _height,
				'fill'   : _.property('fill')
			});

			var label = tick.selectAll('text').data(_.identity);

			label.enter().append('text');

			label.attr('dy', this._height).text(_.property('label'));
		});
	}

	axis.height = function (height) {
		if (!arguments.length) {
			return _height;
		}

		_height = height;
		return axis;
	};

	axis.ticks = function (ticks) {
		if (!arguments.length) {
			return _ticks;
		}

		_ticks = ticks;
		return axis;
	};

	axis.width = function (width) {
		if (!arguments.length) {
			return _width;
		}

		_width = width;
		return axis;
	};

	axis.x = function (x) {
		if (!arguments.length) {
			return _x;
		}

		_x = _.isFunction(x) ? x : _.constant(x);
		return axis;
	};

	axis.y = function (y) {
		if (!arguments.length) {
			return _y;
		}

		_y = _.isFunction(y) ? y : _.constant(y);
		return axis;
	};

	return axis;
}

module.exports = qualitativeAxis;
