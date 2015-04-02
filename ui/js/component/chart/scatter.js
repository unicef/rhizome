'use strict';

var _      = require('lodash');
var d3     = require('d3');
var moment = require('moment');

function x(d) {
	return d.x;
}

function y(d) {
	return d.y;
}

module.exports = {

	template: require('./chart.html'),
	replace : true,

	paramAttributes: [
		'data-format-x',
		'data-format-y'
	],

	mixins: [
		require('component/chart/mixin/margin'),
		require('component/chart/mixin/resize')
	],

	data: function () {
		return {
			marginLeft   : 24,
			marginBottom : 24,
			series       : [],
			formatX      : 's',
			formatY      : 's'
		};
	},

	computed: {
	},

	methods: {
		draw: function () {
			function cx(d) {
				return xScale(d.x);
			}

			function cy(d) {
				return yScale(d.y);
			}

			var svg = d3.select(this.$el);

			var series = this.series || [];

			var xScale = d3.scale.linear()
				.domain([0, d3.max(series, function (d) { return d.x; })])
				.range([0, this.contentWidth]);

			var yScale = d3.scale.linear()
				.domain([0, d3.max(series, function (d) { return d.y; })])
				.range([this.contentHeight, 0]);

			var point = svg
				.select('.data')
				.selectAll('.point')
				.data(series, function (d, i) {
					return d.id || i;
				});

			// FIXME: Hard-coded transition speed
			point
				.transition()
				.duration(500)
				.attr({
					'cx': cx,
					'cy': cy
				});

			// FIXME: Hard-coded transition speed
			point.enter()
				.append('circle')
				.attr({
					'class': 'point',
					'cx'   : cx,
					'cy'   : cy,
					'r'    : 0
				})
				.style('fill', '#d5dfe2')
				.transition()
				.duration(500)
				.attr('r', 2);

			// FIXME: Hard-coded transition speed
			point.exit()
				.transition()
				.duration(500)
				.attr('r', 0)
				.remove();

			var xAxis = d3.svg.axis()
				.scale(xScale)
				.tickFormat(d3.format(this.formatX))
				.ticks(3)
				.orient('bottom');

			svg
				.select('.x.axis')
				.call(xAxis);

			var yAxis = d3.svg.axis()
				.scale(yScale)
				.tickFormat(d3.format(this.formatY))
				.ticks(3)
				.orient('left');

			svg
				.select('.y.axis')
				.call(yAxis);
		}
	},

	watch: {
		'series' : 'draw',
		'width'  : 'draw',
		'height' : 'draw'
	}
};
