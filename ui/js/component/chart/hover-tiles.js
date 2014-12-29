'use strict';

var _  = require('lodash');
var d3 = require('d3');

function getHoverLayer(el) {
	var svg = d3.select(el).selectAll('.hover').data([0]);

	svg.enter().append('g')
		.attr('class', 'hover');

	return svg;
}

function getXValues(series) {
	// Using a plain object as a fake hash set
	var values = {};

	if (!(series instanceof Array)) {
		// End recursion
		values[series.x] = true;

		return values;
	}

	for (var i = 0, l = series.length; i < l; i++) {
		// Recurse and union the hash sets
		_.assign(values, getXValues(series[i]));
	}

	return values;
}

function tile(values, x) {
	var domain = x.domain();
	var tiles  = [];

	if (!values || !(values instanceof Array) || values.length === 0) {
		return [{
			x: x(domain[0]),
			width: x(domain[1]) - x(domain[0]),
			value: x.invert(x(domain[0]) + (x(domain[1]) - x(domain[1])) / 2)
		}];
	}

	var cloned = _.clone(values).sort(function (a, b) {
		return a < b ? -1 : 1;
	});

	var previous = {
		x     : x(domain[0]),
		center: x(cloned[0]),
		value : values[0]
	};

	for (var i = 1, l = cloned.length; i < l; i++) {
		var v = cloned[i];

		previous.width = (previous.center + (Math.abs(x(v) - previous.center) / 2)) - previous.x;

		tiles.push(previous);

		previous = {
			x     : tiles[i - 1].x + tiles[i - 1].width,
			center: x(v),
			value : v
		};
	}

	previous.width = x(domain[1]) - previous.x;
	tiles.push(previous);

	return tiles;
}

/**
 * Vue mixin that creates invisible tiles centered on all of the x-values in a
 * chart for triggering hover interactions.
 */
module.exports = {
	created: function () {
		var self = this;

		self.$on('chart-drawn', function (obj) {
			var x     = obj.x;
			var y     = obj.y;
			var svg   = getHoverLayer(obj.el);
			var xLocs = _.map(_.keys(getXValues(obj.series)), Number).sort();
			var data  = tile(xLocs, x);
			var tiles = svg.selectAll('.hover-tile').data(data);

			tiles.enter().append('rect')
				.attr('class', 'hover-tile')
				.on('mouseover', function (d) {
					var o = { x: d.value };

					self.$dispatch('show-annotation', o);
					self.$emit('show-annotation', o);
				})
				.on('mouseout', function (d) {
					var o = { x: d.value };

					self.$dispatch('hide-annotation', o);
					self.$emit('hide-annotation', o);
				});

			tiles.attr({
				'x'     : function (d) { return d.x; },
				'y'     : Math.min.apply(null, y.range()),
				'width' : function (d) { return d.width; },
				'height': Math.abs(y.range()[1] - y.range()[0])
			});

			tiles.exit().remove();
		});
	}
};
