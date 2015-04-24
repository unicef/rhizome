'use strict';

var _         = require('lodash');
var d3        = require('d3');

var lineChart = require('./renderer/line');
var data      = require('util/data');

module.exports = {

	mixins: [
		require('./year-over-year')
	],

	computed: {
		renderer: function () {
			var x     = this.xScale;
			var y     = this.yScale;
			var color = this.colorScale;

			var renderer = lineChart()
				.x(function (d) {
					return x(d.month);
				})
				.y(function (d) {
					return y(d.value);
				})
				.values(function (d) {
					return d.values;
				})
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
					// lodash.max uses the accessor to find the comparison value, but
					// returns the entire object; d3.max returns the value returned
					// by the accessor
					var last = _.max(d.values, function (v) { return v.month; });

					return {
						text   : d.name + ' – ' + fmt(last.value),
						x      : x(last.month),
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

			var series = {};
			var year   = null;
			var month  = 0;
			var total  = 0;

			_.forEach(_.sortBy(this.datapoints, function (d) {
					return d.campaign.start_date;
				}), function (d) {
					var y = d.campaign.start_date.getFullYear();

					if (year === null) {
						year         = y;
						series[year] = [];
					}

					// Fill in any missing years...
					while (year < y) {
						// Fill out entries for the rest of the year
						while (month < 11) {
							series[year].push({
								month : month,
								value : total,
								year  : year
							});
							month++;
						}

						// Happy New Year!
						year++;
						total        = 0;
						month        = 0;
						series[year] = [];
					}

					var m = d.campaign.start_date.getMonth();
					while (month < m) {
						series[year].push({
							month : month,
							value : total,
							year  : year
						});
						month++;
					}

					total += d.value;
					series[year].push({
						month : month,
						value : total,
						year  : year
					});
					month++;
				});

			return _.map(series, function (d, year) {
				return {
					name  : year,
					values: d
				};
			});
		},

		yScale: function () {
			function value (d) {
				return d.value;
			}

			var scale = d3.scale.linear()
				.range([this.contentHeight, 0]);

			if (!this.empty) {
				var s = _(this.series)
					.pluck('values')
					.flatten(true)
					.value();

				scale.domain([
					Math.min(d3.min(s, value)),
					d3.max(s, value)
				]);
			}

			return scale;
		}
	},

	methods: {
		diffX: function (a, b) {
			return a - b;
		},

		getSeriesName: function (d) {
			return d.year + ' –';
		},

		getX: function (d) {
			return d.month;
		}
	}
};
