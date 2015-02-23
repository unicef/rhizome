'use strict';

var _         = require('lodash');
var d3        = require('d3');

var areaChart = require('./renderer/area');

module.exports = {
	replace : true,
	template: require('./chart.html'),

	mixins: [
		require('./line')
	],

	computed: {
		labels: function () {
			if (this.empty) {
				return [];
			}

			var x      = this.xScale;
			var y      = this.yScale;
			var series = this.series;

			var labels = _.map(series, function (d) {
					// lodash.max uses the accessor to find the comparison value, but
					// returns the entire object; d3.max returns the value returned
					// by the accessor
					var last = _.max(d.values, function (v) { return v.campaign.start_date; });

					return {
						text: d.name,
						x   : x(last.campaign.start_date),
						y   : y(last.y0 + last.y)
					};
				});

			return labels;
		},

		renderer: function () {
			var x     = this.xScale;
			var y     = this.yScale;
			var color = this.colorScale;

			var renderer = areaChart()
				.x(function (d) {
					return x(d.campaign.start_date);
				})
				.y0(function (d) {
					return y(d.y0);
				})
				.y1(function (d) {
					return y(d.y0 + d.y);
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

			var stack = d3.layout.stack()
				.order('inside-out')
				.offset('zero')
				.x(function (d) {
					return d.campaign.start_date;
				})
				.y(function (d) {
					return d.value;
				})
				.values(function (d) {
					return d.values;
				});

			var indicators = _.indexBy(this.indicators, 'id');

			// Facet by indicator
			var series = _(this.datapoints)
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

			return stack(series);
		},

		yScale: function () {
			function y(d) {
				return d.y0 + d.y;
			}

			var scale = d3.scale.linear()
				.range([this.contentHeight, 0]);

			if (!this.empty) {
				var flat = _(this.series)
					.pluck('values')
					.flatten(true)
					.value();

				scale.domain([
					Math.min(0, d3.min(flat, y)),
					d3.max(flat, y) * 1.2
				]);
			}

			return scale;
		}

	},

	methods: {
		getY: function (d) {
			return d.y0 + d.y;
		}
	}

};
