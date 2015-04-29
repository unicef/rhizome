'use strict';

var _  = require('lodash');
var d3 = require('d3');

var line = require('./renderer/line');

function x(d) {
	return d.x;
}

function y(d) {
	return d.y;
}

module.exports = {
	template : require('./chart.html'),

	mixins : [
		require('./mixin/margin'),
		require('./mixin/resize')
	],

	data : function () {
		return {
			chartType : 'spaghetti',
			series    : [],
			domain    : null,
			range     : null
		};
	},

	methods : {
		draw : function () {
			var svg = d3.select(this.$$.canvas);

			var dataset = _.flatten(this.series);
			var xDomain = this.domain || d3.extent(dataset, x);
			var yDomain = this.range || d3.extent(dataset, y);

			var xScale = d3.scale.linear()
				.domain(xDomain)
				.range([0, this.contentWidth]);

			var yScale = d3.scale.linear()
				.domain(yDomain)
				.range([this.contentHeight, 0]);

			svg.select('.data')
				.selectAll('.series')
				.data(this.series)
				.call(line()
					.x(function (d) { return xScale(x(d)); })
					.y(function (d) { return yScale(y(d)); })
					.color(function (d) { return 'rgb(179, 179, 179)'; }));
		},

		resize : function () {
			var svg = d3.select(this.$$.canvas);

		}
	},

	watch : {
		'series' : 'draw',
		'width'  : 'resize',
		'height' : 'resize'
	}
};
