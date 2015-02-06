'use strict';

var _         = require('lodash');
var d3        = require('d3');

var colors    = require('colors/coolgray');
var lineChart = require('./renderer/line');

function x (d) {
	return d.campaign.start_date;
}

function y(d) {
	return d.value;
}

module.exports = {
	replace : true,
	template: require('./chart.html'),

	paramAttributes: [
		'data-height',
		'data-width',
		'data-format-string'
	],

	mixins: [
		require('./mixin/resize'),
		require('./mixin/margin'),
		require('./mixin/with-indicator'),
	],

	partials: {
		'loading-overlay': require('./partial/loading-overlay.html')
	},

	ready: function () {
		d3.select(this.$el)
			.on('mousemove', this.onMouseMove)
			.on('mouseout', function () {
				d3.select(this)
					.select('.annotation')
					.selectAll('line')
					.data([])
					.exit()
					.transition()
					.duration(300)
					.style('opacity', 0)
					.remove();
			});
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
					return x(d.campaign.start_date);
				})
				.y(function (d) {
					return y(d.value);
				})
				.color(function (d, i) {
					return color(i);
				});

			return renderer;
		},

		series: function () {
			if (this.empty) {
				return [];
			}

			var series = _(this.datapoints)
				.sortBy(function (d) {
					return d.campaign.start_date;
				})
				.groupBy('indicator')
				.values()
				.value();

			// Facet the datapoints by indicator
			return series;
		},

		xFmt: function () {
			return function (d) {
				var month   = d3.time.format('%b');
				var newYear = d3.time.format('%b %Y');
				var dt      = new Date(d);

				return dt.getMonth() === 0 ? newYear(dt) : month(dt);
			};
		},

		xScale: function () {
			var datapoints = this.datapoints || [];

			var start = this.domain ?
				this.domain[0] :
				d3.min(datapoints, x) || 0;

			var end = this.domain ?
				this.domain[1] :
				d3.max(datapoints, x) || start + 1;

			return d3.time.scale()
				.domain([start, end])
				.range([0, this.contentWidth]);
		},

		xTicks: function () {
			return this.xScale.ticks(d3.time.months, 3);
		},

		yFmt: function () {
			return d3.format(this.formatString || 's');
		},

		yScale: function () {
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
		},

		yTicks: function () {
			return this.yScale.ticks(3);
		},
	},

	methods: {

		draw: function () {
			var svg      = d3.select(this.$el);
			var renderer = this.renderer;
			var xScale   = this.xScale;
			var yScale   = this.yScale;
			var domain   = xScale.domain();
			var range    = yScale.domain();

			svg.select('.data').selectAll('.' + renderer.className())
				.data(this.series, function (d, i) {
					return d.name || i;
				}).call(renderer);

			var gx = svg.select('.x.axis')
				.call(d3.svg.axis()
					.tickFormat(this.xFmt)
					.tickValues(this.xTicks)
					.scale(xScale)
					.orient('bottom'));

			gx.selectAll('text')
				.style('text-anchor', function (d) {
					return d === domain[0] ?
						'start' :
						d === domain[1] ?
							'end' :
							'middle';
				});

			var gy = svg.select('.y.axis')
				.call(d3.svg.axis()
					.tickFormat(this.yFmt)
					.tickValues(this.yTicks)
					.tickSize(this.contentWidth)
					.scale(yScale)
					.orient('right'));

			gy.selectAll('text')
				.attr({
					'x' : 4,
					'dy': -4
				});

			gy.selectAll('g').classed('minor', function (d) {
				return d !== range[0];
			});
		},

		onMouseMove: function (evt) {
			if (this.empty) {
				return;
			}

			var svg = this.$el.getElementsByTagName('svg')[0];

			var cursor = d3.mouse(svg)[0];

			var range = _(this.datapoints)
				.map(function (d) {
					return d.campaign.start_date;
				})
				.uniq()
				.sortBy()
				.value();

			var x = this.xScale;

			var t = d3.scale.quantize()
				.domain(x.range())
				.range(range);

			var data = [];

			if (cursor >= 0 || cursor <= this.contentWidth) {
				data[0] = t(cursor);
			}

			var line = d3.select(svg)
				.select('.annotation')
				.selectAll('line')
				.data(data);

			line.enter()
				.append('line')
				.style({
					'opacity': 0,
					'stroke': '#ffcc67'
				});

			line
				.attr({
					'y1': 0,
					'y2': this.contentHeight
				})
				.transition()
				.duration(300)
				.attr({
					'x1': x,
					'x2': x,
				})
				.style('opacity', 1);

			line.exit()
				.transition()
				.duration(300)
				.style('opacity', 0)
				.remove();
		}

	},

	watch: {
		'datapoints': 'draw',
		'width'     : 'draw',
		'height'    : 'draw'
	}
};
