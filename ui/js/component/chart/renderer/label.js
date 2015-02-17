'use strict';

var _  = require('lodash');

function label() {
	var cls             = ['label'];
	var text            = function (d) { return d.text; };
	var transitionSpeed = 300;
	var x               = function (d) { return d.x; };
	var y               = function (d) { return d.y; };

	function chart(selection) {
		selection
			.text(text)
			.transition()
			.duration(transitionSpeed)
			.attr({
				'x': x,
				'y': y
			});

		selection.enter()
			.append('text')
			.style({
				'opacity'    : 0,
				'text-anchor': 'end'
			})
			.attr({
				'dx': '-4',
				'dy': '-4',
				'x' : x,
				'y' : y
			})
			.text(text)
			.transition()
			.duration(transitionSpeed)
			.style('opacity', 1);

		selection.attr('class', cls.join(' '));

		selection.exit()
			.transition()
			.duration(300)
			.style('opacity', 0)
			.remove();
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
