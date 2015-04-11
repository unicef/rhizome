'use strict';

var _         = require('lodash');
var d3        = require('d3');
var moment    = require('moment');

var dateUtil  = require('util/date');

var lineChart = require('./renderer/line');

module.exports = {

	mixins: [
		require('./line')
	],

	computed: {

		campaign_start: function () {
			if (!this.period) {
				return null;
			}

			var start = moment(this.campaign.start_date);

			start = start.subtract.apply(
					start,
					dateUtil.parseDuration(this.period)
				)
				.startOf('year')
				.format('YYYY-MM-DD');

			return start;
		},

		renderer: function () {
			var x     = this.xScale;
			var y     = this.yScale;
			var color = this.colorScale;

			var renderer = lineChart()
				.x(function (d) {
					return x(d.campaign.start_date.getMonth());
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

		series: function () {
			if (this.empty) {
				return [];
			}

			var series = _(this.datapoints)
				.groupBy(function (d) {
					return d.campaign.start_date.getFullYear();
				})
				.map(function (d, year) {
					return {
						name  : year,
						values: _.sortBy(d, function (o) { return o.campaign.start_date; })
					};
				})
				.value();

			return series;
		},

		xFmt: function () {
			return function (d) {
				return moment().month(d).format('MMM');
			};
		},

		xScale: function () {
			var scale = d3.scale.linear()
				.domain([0, 11])
				.range([0, this.contentWidth]);

			return scale;
		},

		xTicks: function () {
			if (!this.campaign) {
				return [0, 5, 11];
			}

			var ticks = [];
			var now = moment(this.campaign.value, 'YYYY-MM-DD').month();

			// If the current month is April or later, show January
			if (now > 2) {
				ticks.push(0);
			}

			// If the current month is after August, show June
			if (now > 7) {
				ticks.push(5);
			}

			ticks.push(now);

			// if the current month is before November, show December
			if (now < 9) {
				ticks.push(11);
			}

			return ticks;
		}

	}

};
