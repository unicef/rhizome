'use strict';

var _  = require('lodash');
var d3 = require('d3');

module.exports = function lineChart() {
	var className       = 'line';
	var color           = function () { return 'inherit'; };
	var line            = d3.svg.line();
	var transitionSpeed = 500;
	var values          = _.identity;

	function chart(selection) {
		selection.each(function (d, i) {
			var g    = d3.select(this);
			var path = g.selectAll('path').data(d);

			path.enter()
				.append('path')
				.style('stroke', color);

			path
				.attr('class', className)
				.transition()
				.duration(transitionSpeed)
				.attr('d', line)
				.style('stroke', color);

			path.exit()
				.transition()
				.duration(transitionSpeed)
				.style('opacity', 0)
				.remove();
		});
	}

	chart.className = function (value) {
		if (!arguments.length) {
			return className;
		}

		className = value;
		return chart;
	};

	chart.color = function (value) {
		if (!arguments.length) {
			return color;
		}

		color = value;
		return chart;
	};

	chart.defined = function (value) {
		if (!arguments.length) {
			return line.defined();
		}

		line.defined(value);
		return chart;
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

	chart.x = function (value) {
		if (!arguments.length) {
			return line.x();
		}

		line.x(value);
		return chart;
	};

	chart.y = function (value) {
		if (!arguments.length) {
			return line.y();
		}

		line.y(value);
		return chart;
	};

	return chart;
};
