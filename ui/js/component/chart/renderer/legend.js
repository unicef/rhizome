'use strict';

var d3 = require('d3');



function legend() {
	var _padding      = 3;
	var _scale        = d3.scale.category20b();
	var _size         = 9;
	var _clickHandler = null;

	function chart (selection) {
		selection.each(function () {
			var g      = d3.select(this);
			var series = g.selectAll('.series').data(_scale.domain());

			var seriesEnter = series.enter()
				.append('g')
				.attr({
					'class'     : 'series',
					'transform' : translate
				});

			seriesEnter.append('rect')
				.attr({
					'width'  : _size,
					'height' : _size
				});

			seriesEnter.append('text')
				.attr({
					'x'  : _size + _padding,
					'y'  : _size / 2,
					'dy' : '0.4em'
				});

			series
				.on('click', _clickHandler)
				.transition()
				.duration(300)
				.attr('transform', translate);

			series.select('rect')
				.attr('fill', _scale)
				.transition()
				.duration(300)
				.attr({
					'width'  : _size,
					'height' : _size
				});

			series.select('text')
				.text(String)
				.transition()
				.duration(300)
				.attr({
					'x' : _size + _padding,
					'y' : _size / 2
				});

			series.exit()
				.transition()
				.duration(300)
				.style('opacity', 0)
				.remove();
		});
	}

	chart.clickHandler = function (value) {
		if (!arguments.length) {
			return _clickHandler;
		}

		_clickHandler = value;
		return chart;
	};

	chart.padding = function (value) {
		if (!arguments.length) {
			return _padding;
		}

		_padding = value;
		return chart;
	};

	chart.scale = function (value) {
		if (!arguments.length) {
			return _scale;
		}

		_scale = value;
		return chart;
	};

	chart.size = function (value) {
		if (!arguments.length) {
			return _size;
		}

		_size = value;
		return chart;
	};

	function translate(d, i) {
		return 'translate(0,' + (i * (_size + _padding)) + ')';
	}

	return chart;
}

module.exports = legend;
