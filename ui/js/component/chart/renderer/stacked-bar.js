'use strict';

var _  = require('lodash');
var d3 = require('d3');

module.exports = function stackedBar() {
	var className       = 'layer';
	var color           = function () { return 'inherit'; };
	var height          = 0;
	var transitionSpeed = 500;
	var values          = Object;
	var width           = Number;
	var x               = d3.scale.linear();
	var y               = d3.scale.ordinal();

	function chart(g) {
		g.enter()
			.append('g')
			.attr('class', className);

		g.style('fill', color);

		var rect = g.selectAll('rect')
			.data(function (d) { return values(d); });

		rect
			.transition()
			.duration(transitionSpeed)
			.attr({
				'x': x,
				'y': y,
			});

		rect.enter()
			.append('rect')
			.attr({
				'x'     : x,
				'y'     : y,
				'width' : 0,
				'height': height
			});

		rect
			.transition()
			.duration(transitionSpeed)
			.attr('width', width);

		rect.exit()
			.transition()
			.duration(transitionSpeed)
			.attr('width', 0)
			.remove();
	}

	chart.color = function (value) {
		if (!arguments.length) {
			return color;
		}

		color = value;
		return chart;
	};

	chart.height = function (value) {
		if (!arguments.length) {
			return height;
		}

		height = value;
		return chart;
	};

	chart.selector = function () {
		var names = className;

		if (_.isString(names)) {
			names = names.split(/\s+/);
		}

		if (!_.isArray(names)) {
			names = [names];
		}

		return '.' + names.join('.');
	};

	chart.transitionSpeed = function (value) {
		if (!arguments.length) {
			return transitionSpeed;
		}

		transitionSpeed = value;
		return chart;
	};

	chart.values = function (value) {
		if (!arguments.length) {
			return values;
		}

		values = value;
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

	return chart;
};
