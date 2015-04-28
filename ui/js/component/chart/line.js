'use strict';

var _         = require('lodash');
var d3        = require('d3');
var moment    = require('moment');

var colors    = require('colors');
var data      = require('util/data');
var hoverLine = require('./behavior/hover-line');
var label     = require('./renderer/label');
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
		'data-format-string',
		'data-x-axis-label',
		'data-y-axis-label'
	],

	mixins: [
		require('./mixin/resize'),
		require('./mixin/margin'),
		require('./mixin/with-indicator'),
	],

	partials: {
		'loading-overlay': require('./partial/loading-overlay.html')
	},

	data : function () {
		return {
			sortLabels : true,
			chartType  : 'line',
			xAxisLabel : '',
			yAxisLabel : '',
			formatString : ',.0f',
		};
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
				.values(function (d) { return d.values; })
				.color(function (d, i) {
					return color(i);
				});

			return renderer;
		},

		labels: function () {
			if (this.empty) {
				return [];
			}

			var x      = this.xScale;
			var y      = this.yScale;
			var series = this.series;
			var fmt    = this.yFmt;

			var labels = _(series)
				.map(function (d) {
					var last   = _.max(d.values, function (v) { return v.campaign.start_date; });

					return {
						text   : d.name + ' ' + fmt(last.value),
						x      : x(last.campaign.start_date),
						y      : y(last.value),
						defined: data.defined(last.value)
					};
				})
				.filter('defined')
				.sortBy('y')
				.value();

			return labels;
		},

		series: function () {
			if (this.empty) {
				return [];
			}

			var indicators = _.indexBy(this.indicators, 'id');

			var series = _(this.datapoints)
				.filter(function (d) {
					return data.defined(d.value);
				})
				.sortBy(function (d) {
					return d.campaign.start_date;
				})
				.groupBy('indicator')
				.map(function (d, indicator) {
					return {
						name  : indicators[indicator].short_name,
						values: d
					};
				})
				.value();

			// Facet the datapoints by indicator
			return series;
		},

		xFmt: function () {
			return d3.time.format('%b %Y');
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
			var months = [0];
			var domain = this.xScale.domain();
			var dt = moment(domain[0]).clone().startOf('month');
			var end = moment(domain[1]);
			var ticks = [];

			while (dt.isBefore(end)) {
				if (months.indexOf(dt.month()) >= 0) {
					ticks.push(dt.clone().toDate());
				}

				dt.add(1, 'months');
			}

			ticks.push(dt.clone().toDate());

			return ticks;
		},

		yFmt: function () {
			return d3.format(this.formatString);
		},

		yScale: function () {
			var datapoints = this.datapoints || [];

			var lower = this.empty ?
				0 :
				Math.min(0, d3.min(datapoints, y)) || 0;

			var upper = this.empty ?
				1 :
				(d3.max(datapoints, y) || 1);

			return d3.scale.linear()
				.domain([lower, upper])
				.range([this.contentHeight, 0]);
		},

		yTicks: function () {
			return this.yScale.ticks(3);
		},
	},

	methods: {
		diffX: function (a, b) {
			return a.getTime() - b.getTime();
		},

		draw: function () {
			var svg        = d3.select(this.$el);
			var renderer   = this.renderer;
			var xScale     = this.xScale;
			var yScale     = this.yScale;
			var range      = yScale.domain();

			// Set up the hover interaction
			svg.select('svg')
				.call(hoverLine()
					.width(this.contentWidth)
					.height(this.contentHeight)
					.top(-this.marginTop)
					.xFormat(this.xFmt)
					.yFormat(this.yFmt)
					.x(this.getX)
					.y(this.getY)
					.xScale(xScale)
					.yScale(yScale)
					.diff(this.diffX)
					.seriesName(this.getSeriesName)
					.sort(this.sortLabels)
					.datapoints(_(this.series).pluck('values').flatten().value())
				);

			svg.select('.data').selectAll('.' + renderer.className())
				.data(this.series, function (d, i) {
					return d.name || i;
				}).call(renderer);

			svg.select('.annotation')
				.selectAll('.series.label')
				.data(this.labels)
				.call(label()
					.addClass('series')
					.width(this.contentWidth)
					.height(this.contentHeight)
					.align(false));

			var xFmt = this.xFmt;

			var gx = svg.select('.x.axis')
				.call(d3.svg.axis()
					.tickFormat(function (d) {
						if (d instanceof Date) {
							if (d.getMonth() === 0) {
								return moment(d).format('MMM YYYY');
							}

							return moment(d).format('MMM');
						}

						return xFmt(d);
					})
					.tickValues(this.xTicks)
					.outerTickSize(0)
					.scale(xScale)
					.orient('bottom'));

			var svgBox = this.$$.canvas.getBoundingClientRect();
			gx.selectAll('text')
				.attr('dx', function () {
					var bbox = this.getBoundingClientRect();
					var dx = null;

					if (bbox.right > svgBox.right) {
						dx = svgBox.right - bbox.right;
					}

					if (bbox.left < svgBox.left) {
						dx = svgBox.left - bbox.left;
					}

					return dx;
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

		getSeriesName: function (d) {
			return _.indexBy(this.indicators, 'id')[d.indicator].short_name;
		},

		getX: function (d) {
			return d.campaign.start_date;
		},

		getY: function (d) {
			return d.value;
		}

	},

	watch: {
		'datapoints': 'draw',
		'width'     : 'draw',
		'height'    : 'draw'
	}
};
