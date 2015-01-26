'use strict';

var _         = require('lodash');
var d3        = require('d3');

var colors    = require('../../colors/coolgray');
var lineChart = require('./line-chart');

module.exports = {
	replace : true,
	template: require('./line.html'),

	paramAttributes: [
		'data-height',
		'data-width',
	],

	mixins: [
		require('./resize'),
		require('./margin'),
		require('./with-indicator'),
	],

	partials: {
		'loading-overlay': require('./partials/loading-overlay.html')
	},

	computed: {

		colorScale: function () {
			var scale = d3.scale.ordinal()
				.domain(d3.range(colors.length))
				.range(colors);

			return scale;
		},

		renderer: function () {
			var x     = this.xScale;
			var y     = this.yScale;
			var color = this.colorScale;

			var renderer = lineChart()
				.x(function (d) {
					return x(d.campaign.start_date.getTime());
				})
				.y(function (d) {
					return y(d.value);
				})
				.color(function (d, i) {
					return color(i);
				});

			return renderer
		},

		series: function () {
			console.info('line::series enter');

			if (this.empty) {
				console.info('line::series empty');
				return [];
			}

			// Facet the datapoints by indicator
			console.info('line::series exit');
			return _.values(_.groupBy(this.datapoints, 'indicator'));
		},

		xScale: function () {
			function x (d) {
				return d.campaign.start_date.getTime();
			}

			var datapoints = this.datapoints || [];

			var start = this.domain ?
				this.domain[0] :
				d3.min(datapoints, x) || 0;

			var end = this.domain ?
				this.domain[1] :
				d3.max(datapoints, x) || start + 1;

			return d3.scale.linear()
				.domain([start, end])
				.range([0, this.contentWidth]);
		},

		yScale: function () {
			function y(d) {
				return d.value;
			}

			var datapoints = this.datapoints || [];

			var lower = this.empty ?
				0 :
				Math.min(0, d3.min(datapoints, y)) || 0;

			var upper = this.empty ?
			1 :
			(d3.max(datapoints, y) || 1) * 1.1;

			return d3.scale.linear()
				.domain([lower, upper])
				.range([this.contentHeight, 0]);
		}

	},

	methods: {

		draw: function () {
			console.info('line::draw', 'enter');
			var svg      = d3.select(this.$el).select('.data');
			var renderer = this.renderer;

			var g = svg.selectAll('.' + renderer.className())
				.data(this.series, function (d, i) {
					return d.name || i;
				}).call(renderer);

			console.info('line::draw', 'exit');
		}

	},

	watch: {
		'datapoints': 'draw',
		'width'     : 'draw',
		'height'    : 'draw'
	}
};
