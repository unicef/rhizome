'use strict';

var _  = require('lodash');
var d3 = require('d3');

module.exports = function barChart() {
	var className       = 'bar';
	var color           = function () { return 'inherit'; };
	var height          = null;
	var transitionSpeed = 500;
	var values          = Object;
	var width           = null;
	var x               = null;
	var y               = null;

	function translate(d, i) {
		return 'translate(0,' + y(d, i) + ')';
	}

	function chart(selection) {
		selection.transition()
			.duration(transitionSpeed)
				.attr('transform', translate);

		selection.enter()
			.append('g')
				.attr('transform', translate);

		selection.attr('class', className);

		selection.each(function (d, i) {
			var g   = d3.select(this);
			var bar = g.selectAll('rect').data(values(d));

			bar.transition()
				.duration(transitionSpeed)
					.attr({
						'fill'  : color,
						'height': height,
						'x'     : x
					});

			bar.enter()
				.append('rect')
					.attr({
						'fill'  : color,
						'height': height,
						'x'     : x,
						'width' : 0
					});

			bar.transition()
				.duration(transitionSpeed)
					.attr('width', width);

			bar.exit()
				.transition().duration(transitionSpeed)
					.style('opacity', 0)
				.remove();

			var label = g.selectAll('.label').data([d.name]);

			label.enter()
				.append('text')
					.attr({
						'dy': -4,
						'class': 'label'
					})
					.style('opacity', 0)
					.text(String)
				.transition().duration(transitionSpeed)
					.style('opacity', 1);

			label.text(String);

			label.exit()
				.transition().duration(transitionSpeed)
					.style('opacity', 0)
				.remove();

			var value = g.selectAll('.value').data(values(d));

			value.enter()
				.append('text')
					.attr({
						'dx'       : 2,
						'dy'       : -3,
						'class'    : 'value',
						'transform': function (d) {
							return 'translate(' + x(d) + ',' + height(d) + ')';
						}
					})
					.style('opacity', 0)
					.text(function (d) {
						return d.value;
					})
				.transition().duration(transitionSpeed)
					.style('opacity', 1);

			value.text(function (d) {
				return d3.format('n')(d.value);
			});

			value.exit()
				.transition().duration(transitionSpeed)
					.style('opacity', 0)
				.remove();
		});

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
