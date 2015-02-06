'use strict';

var _         = require('lodash');
var d3        = require('d3');

var lineChart = require('./renderer/line');

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
				.color(function (d, i) {
					return color(i);
				});

			return renderer;
		},

		series: function () {
			if (this.empty) {
				return [];
			}

			var series = {};
			var year   = null;
			var month  = 0;
			var total  = 0;

			_(this.datapoints)
				.sortBy(function (d) {
					return d.campaign.start_date;
				})
				.forEach(function (d) {
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
								month: month,
								value: total
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
							month: month,
							value: total
						});
						month++;
					}

					total += d.value;
					series[year].push({
						month: month,
						value: total
					});
					month++;
				});

			return _.values(series);
		},

		yScale: function () {
			function value (d) {
				return d.value;
			}

			var scale = d3.scale.linear()
				.range([this.contentHeight, 0]);

			if (!this.empty) {
				var s = _.flatten(this.series, true);

				scale.domain([
					Math.min(d3.min(s, value)),
					d3.max(s, value) * 1.1
				]);
			}

			return scale;
		}
	}
};
