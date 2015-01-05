'use strict';

var d3   = require('d3');
var Vue  = require('vue');

var util = require('../../util/data');

var TRANSITION_SPEED = 500;

module.exports = Vue.extend({
	paramAttributes: [
		'data-series',
		'data-width',
		'data-height'
	],

	mixins: [
		require('./labels'),
		require('./hover-tiles'),
		require('./hover-line'),
		require('./yGrid'),
		require('./xAxis')
	],

	data: function () {
		return {
			series: [],
			width : 100,
			height: 100,
			x     : d3.scale.linear(),
			y     : d3.scale.linear()
		};
	},

	methods: {
		draw: function () {
			function getX(d) { return d.x; }

			function getY(d) { return d.y; }

			function getScaledX(d) { return x(getX(d)); }

			function getScaledY(d) { return y(getY(d)); }

			function defined(d) { return util.defined(getY(d)); }

			function getPoints(d) { return d.points; }

			var svg     = d3.select(this.$el);

			var series  = this.series || [];
			var dataset = series.map(getPoints).sort(function (a, b) {
				return a.x < b.x ? -1 : 1;
			});

			var start   = this.domain ? this.domain[0] : util.min(dataset, getX);
			var end     = this.domain ? this.domain[1] : util.max(dataset, getX);
			var lower   = Math.min(0, util.min(dataset, getY));
			var upper   = util.max(dataset, getY) * 1.1;

			var x       = this.x;
			var y       = this.y;

			x.domain([start, end])
				.range([0, this.width]);
			y.domain([lower, upper])
				.range([this.height, 0]);

			var line = d3.svg.line()
				.defined(defined)
				.x(getScaledX)
				.y(getScaledY);

			var lines = svg.selectAll('.line').data(series, function (d, i) {
				return d.name || i;
			});

			lines.enter().append('path')
				.attr('class', 'line');

			lines.transition().duration(TRANSITION_SPEED)
				.attr('d', function (d) {
					return line(getPoints(d));
				})
				.style('stroke', function (d) { return d.color; });

			lines.exit().remove();

			var point = svg.selectAll('.point')
				.data(Array.prototype.concat.apply([], dataset));

			point.enter().append('circle')
				.attr({
					'class': 'point',
					'r'    : 2,
				});

			point.transition().duration(TRANSITION_SPEED).attr({
				'cx': getScaledX,
				'cy': getScaledY
			});

			point.exit().remove();

			this._callHook('drawn');
			this.$emit('chart-drawn', {
				el    : this.$el,
				series: dataset,
				x     : this.x,
				y     : this.y
			});
		}
	},

	on: {
		'hook:attached': 'draw'
	},

	watch: {
		'series': 'draw',
		'width' : 'draw',
		'height': 'draw'
	}
});
