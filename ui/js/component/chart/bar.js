'use strict';

var _        = require('lodash');
var d3       = require('d3');

var barChart = require('./bar-chart');
var colors   = require('../../colors/coolgray');

module.exports = {

	replace : true,
	template: require('./bar-chart.html'),

	mixins: [
		require('./margin'),
		require('./resize'),
		require('./with-indicator')
	],

	data: function () {
		return {
			aspect      : false, // Disable auto-setting height
			barHeight   : 14,
			marginBottom: 24,
			padding     : 18
		};
	},

	computed: {
		colorScale: function () {
			return d3.scale.ordinal()
				.domain(d3.range(colors.length))
				.range(colors);
		},

		empty: function () {
			return !this.datapoints || this.datapoints.length < 1;
		},

		height: function () {
			var l       = this.series.length;
			var padding = l * this.padding;
			var h       = Math.max(0, l * this.barHeight + padding);

			return h + this.marginTop + this.marginBottom;
		},

		query: function () {
			return {
				indicator__in: _.map(this.indicators, function (d) {
					return d.id || d;
				}),
				region__in   : [this.region],
				limit        : 1
			};
		},

		renderer: function () {
			var x         = this.xScale;
			var y         = this.yScale;
			var color     = this.colorScale;
			var barHeight = this.barHeight;

			var renderer = barChart()
				.height(function () {
					return barHeight;
				})
				.width(function (d) {
					return x(d.value);
				})
				.x(function () {
					return x(0);
				})
				.y(y)
				.color(function (d, i) {
					return color(i);
				})
				.values(function (d) {
					return d.values;
				});

			return renderer;
		},

		series: function () {
			if (this.empty) {
				return [];
			}

			var indicators = _.indexBy(this.indicators, 'id');
			var series = _(this.datapoints).groupBy('indicator').map(function (d, indicator) {
				return {
					id    : indicator,
					name  : indicators[indicator].short_name,
					values: d
				};
			}).value();

			return series;
		},

		xFmt: function () {
			return d3.format('s');
		},

		xScale: function () {
			function x(d) {
				return d.value;
			}

			var datapoints = this.datapoints || [];

			var domain = this.domain || [];

			if (domain.length < 2) {
				domain[0] = Math.min(0, d3.min(datapoints, x)) || 0;
				domain[1] = d3.max(datapoints, x) || domain[0] + 1;
			}

			return d3.scale.linear()
				.domain(domain)
				.range([0, this.contentWidth]);
		},

		xTicks: function () {
			return this.xScale.ticks(4);
		},

		yScale: function () {
			var padding = this.padding;
			var step   = this.barHeight + padding;

			return function (d, i) {
				return padding + step * i;
			};
		}
	},

	methods: {

		draw: function () {
			var svg      = d3.select(this.$el);
			var renderer = this.renderer;

			svg.select('.data').selectAll(renderer.selector())
				.data(this.series, function (d) {
					return d.id;
				})
				.call(renderer);
		}

	},

	watch: {
		'datapoints': 'draw',
		'width'     : 'draw',
		'height'    : 'draw'
	}

};
