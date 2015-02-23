'use strict';

var _  = require('lodash');
var d3 = require('d3');

function label() {
	var cls             = ['label'];
	var height          = 1;
	var text            = function (d) { return d.text; };
	var transitionSpeed = 300;
	var width           = 1;
	var x               = function (d) { return d.x; };
	var y               = function (d) { return d.y; };

	function chart(labels) {
		var labelEnter = labels.enter()
			.append('text')
			.style({
				'opacity'    : 0,
				'text-anchor': 'end'
			})
			.attr({
				'dx': '-4',
				'dy': '-4'
			})
			.text(text);

		var labelData = labels.data();

		labelData.forEach(function (d) {
			d.targetY = d.y;
			d.targetX = d.x;
		});

		d3.layout.force()
			.nodes(labelData)
			.charge(-10)
			.gravity(0)
			.size([width, height])
			.on('tick', function (e) {
				var k = 0.1 * e.alpha;

				labelData.forEach(function (d) {
					d.y += (d.targetY - d.y) * k;
					// FIXME: Hard-coded bounds to ensure that labels don't get pushed
					// off the chart. Based on the size of the labels inspected in
					// Chrome, but should be calculated dynamically.
					d.y = Math.min(Math.max(d.y, 20), height);
					d.x = d.targetX;
				});
			})
			.on('end', function () {
				labels
					.text(text)
					.transition()
					.duration(300)
					.attr({
						'x': x,
						'y': y
					});

				labelEnter
					.attr({
						'x': x,
						'y': y
					})
					.transition()
					.duration(transitionSpeed)
					.style('opacity', 1);

				labels.attr('class', cls.join(' '));

				labels.exit()
					.transition()
					.duration(300)
					.style('opacity', 0)
					.remove();
			})
			.start();
	}

	chart.addClass = function (value) {
		if (!chart.hasClass(value)) {
			cls.push(value);
		}

		return chart;
	};

	chart.classes = function (value) {
		if (!arguments.length) {
			return cls;
		}

		if (_.isString(value)) {
			value = value.split(/\s+/);
		} else if (!_.isArray(value)) {
			value = [String(value)];
		}

		cls = value;

		return chart;
	};

	chart.hasClass = function (value) {
		return cls.indexOf(value) > -1;
	};

	chart.height = function (value) {
		if (!arguments.length) {
			return height;
		}

		height = value;
		return chart;
	};

	chart.removeClass = function (value) {
		var i = cls.indexOf(value);

		if (i > -1) {
			cls.splice(i, 1);
		}

		return chart;
	};

	chart.text = function (value) {
		if (!arguments.length) {
			return text;
		}

		text = value;
		return chart;
	};

	chart.transitionSpeed = function (value) {
		if (!arguments.length) {
			return transitionSpeed;
		}

		transitionSpeed = value;
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
}

module.exports = label;
