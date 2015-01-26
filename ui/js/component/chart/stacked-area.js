'use strict';

var _         = require('lodash');
var d3        = require('d3');

var areaChart = require('./area');

module.exports = {
	replace : true,
	template: require('./chart.html'),

	mixins: [
		require('./line')
	],

	computed: {

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
				});

			// Facet by indicator
			var series = _(this.datapoints).groupBy('indicator').values().value();

			return stack(series);
		},

		yScale: function () {
			function y(d) {
				return d.y0 + d.y;
			}

			var scale = d3.scale.linear()
				.range([this.contentHeight, 0]);

			if (!this.empty) {
				var flat = _.flatten(this.series, true);
				scale.domain([
					Math.min(0, d3.min(flat, y)),
					d3.max(flat, y) * 1.1
				]);
			}

			return scale;
		}

	}

};
