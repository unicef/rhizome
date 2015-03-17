'use strict';

var d3     = require('d3');

var colors = require('colors/coolgray');

function scale(categories) {
	var interpolate = d3.interpolate(
		d3.rgb(colors[0]),
		d3.rgb(colors[colors.length - 1]));

	var scale = d3.scale.linear().domain([0, categories.length - 1]);

	// Build up a range of colors for the ordinal scale by interpolating the
	// two extremes of the colors from the coolgray array
	var range = [];
	for (var i = 0, l = categories.length; i < l; i++) {
		range.push(interpolate(scale(i)));
	}

	return d3.scale.ordinal()
		.domain(categories)
		.range(range);
}

module.exports = {
	scale: scale
};
