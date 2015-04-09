'use strict';

var _    = require('lodash');
var d3   = require('d3');
var path = require('vue/src/parsers/path');

/**
 * Renderer of stacked columns
 */
module.exports = function () {
	var _className = 'column';
	var _color     = 'inherit';
	var _height    = function (d) { return d.height; };
	var _id        = function (d, i) { return i; };
	var _values    = _.identity;
	var _width     = function (d) { return d.width; };
	var _x         = function (d) { return d.x; };
	var _y         = function (d) { return d.y; };

	/**
	 * @private
	 * Return a CSS selector based on the value of _className
	 */
	function selector() {
		return '.' + _className.split(/\s+/).join('.');
	}

	function chart(selection) {
		selection.each(function (d) {
			var g      = d3.select(this);
			var column = g.selectAll(selector())
				.data(_values(d), _id);

			column.enter()
				.append('rect')
				.attr({
					'height' : 0,
					'width'  : _width,
					'x'      : _x,
					'y'      : _y,
				})
				.style('fill', _color);

			// Update the vertical positions first
			var t = column.transition()
				.duration(500)
				.attr({
					'class'  : _className,
					'height' : _height,
					'y'      : _y,
				});

			// Then reorder and resize the horizontal values. Chained transitions!
			t.transition().attr({
				'x'     : _x,
				'width' : _width
			});

			column.exit()
				.transition()
				.duration(500)
				.attr('height', 0)
				.remove();
		});
	}

	chart.className = function (value) {
		if (!arguments.length) {
			return _className;
		}

		_className = value;
		return chart;
	};

	chart.color = function (value) {
		if (!arguments.length) {
			return _color;
		}

		_color = value;
		return chart;
	};

	chart.height = function (value) {
		if (!arguments.length) {
			return _height;
		}

		if (_.isFunction(value) || _.isNumber(value)) {
			_height = value;
		} else {
			_height = function (d) { return path.get(d, value); };
		}

		return chart;
	};

	chart.id = function (value) {
		if (!arguments.length) {
			return _id;
		}

		_id = value;
		return chart;
	};

	chart.values = function (value) {
		if (!arguments.length) {
			return _values;
		}

		_values = value;
		return chart;
	};

	chart.width = function (value) {
		if (!arguments.length) {
			return _width;
		}

		if (_.isFunction(value) || _.isNumber(value)) {
			_width = value;
		} else {
			_width = function (d) { return path.get(d, value); };
		}


		return chart;
	};

	chart.x = function (value) {
		if (!arguments.length) {
			return _x;
		}

		if (_.isFunction(value) || _.isNumber(value)) {
			_x = value;
		} else {
			_x = function (d) { return path.get(d, value); };
		}

		return chart;
	};

	chart.y = function (value) {
		if (!arguments.length) {
			return _y;
		}

		if(_.isFunction(value) || _.isNumber(value)) {
			_y = value;
		} else {
			_y = function (d) { return path.get(d, value); };
		}

		return chart;
	};

	return chart;
};
