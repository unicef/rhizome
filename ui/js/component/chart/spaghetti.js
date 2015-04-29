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
			domain    : null,
			range     : null,
			series    : [],
			xFormat   : String,
			xScale    : d3.time.scale,
			yFormat   : String,
			yScale    : d3.scale.linear
		};
	},

	methods : {
		draw : function () {
			var svg = d3.select(this.$$.canvas);

			var dataset = _.flatten(this.series);
			var xDomain = this.domain || d3.extent(dataset, x);
			var yDomain = this.range || d3.extent(dataset, y);

			var xScale = this.xScale()
				.domain(xDomain)
				.range([0, this.contentWidth]);

			var yScale = this.yScale()
				.domain(yDomain)
				.range([this.contentHeight, 0]);

			svg.select('.data')
				.selectAll('.series')
				.data(this.series)
				.call(line()
					.x(function (d) { return xScale(x(d)); })
					.y(function (d) { return yScale(y(d)); })
					.color(function () { return 'rgb(179, 179, 179)'; }));

			svg.select('.x.axis')
				.call(d3.svg.axis()
					.tickFormat(this.xFormat)
					.outerTickSize(0)
					.scale(xScale)
					.orient('bottom'));

			var gy = svg.select('.y.axis')
				.call(d3.svg.axis()
					.ticks(3)
					.tickFormat(this.yFormat)
					.tickSize(this.contentWidth)
					.scale(yScale)
					.orient('right'));

			gy.selectAll('text')
				.attr({
					'x' : 4,
					'dy': -4
				});
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
