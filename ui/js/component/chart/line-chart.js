'use strict';

var d3   = require('d3');

module.exports = function lineChart() {
	var transitionSpeed = 500;
	var className       = 'line';
	var line            = d3.svg.line();
	var values          = Object;
	var color           = function () { return 'inherit'; };

	function chart(selection) {
		// The datum for each item in this selection should correspond to an
		// individual series

		// Make sure we have one g element per series
		selection.enter().append('g');

		// Reset class attributes in case the className has changed since
		// the last call
		selection.attr('class', className);

		selection.each(function (d, i) {
			// d should be an array of objects representing each data point
			// in this series
			var g = d3.select(this);

			var path = g.selectAll('path').data([d]);

			path
				.transition().duration(transitionSpeed)
					.style('stroke', color(d, i));

			path.enter()
				.append('path')
					.style('stroke', color(d, i));

			path
				.transition().duration(transitionSpeed)
					.attr('d', line);

			path.exit()
				.transition().duration(transitionSpeed)
					.style('opacity', 0)
					.remove();
		});

		// FIXME: Fade out old series for now, but we really want to shrink the
		// circles and fade the line. We have to be sure the entire g element gets
		// removed, though.
		selection.exit()
			.transition().duration(transitionSpeed)
				.style('opacity', 0)
			.remove();
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

		value = values;
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
