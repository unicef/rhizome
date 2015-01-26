'use strict';

module.exports = function areaChart() {
	var area            = d3.svg.area();
	var className       = 'area';
	var color           = function () { return 'inherit'; };
	var transitionSpeed = 500;

	function chart(selection) {
		selection.enter().append('g');

		selection.attr('class', className);

		selection.each(function (d, i) {
			var g = d3.select(this);

			var path = g.selectAll('path').data([d]);

			path.enter().append('path');

			path.transition()
				.duration(transitionSpeed)
					.attr('d', area)
					.style('fill', color(d, i));

			path.exit()
				.transition().duration(transitionSpeed)
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

	chart.transitionSpeed = function (value) {
		if (!arguments.length) {
			return transitionSpeed;
		}

		transitionSpeed = value;
		return chart;
	};

	chart.x = function (value) {
		if (!arguments.length) {
			return area.x();
		}

		area.x(value);
		return chart;
	};

	chart.y0 = function (value) {
		if (!arguments.length) {
			return area.y0();
		}

		area.y0(value);
		return chart;
	};

	chart.y1 = function (value) {
		if (!arguments.length) {
			return area.y1();
		}

		area.y1(value);
		return chart;
	};

	return chart;
};
