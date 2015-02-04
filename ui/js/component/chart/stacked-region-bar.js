'use strict';

var _        = require('lodash');
var d3       = require('d3');
var moment   = require('moment');

var stackedBar = require('./renderer/stacked-bar');

module.exports = {

	mixins: [
		require('./bar')
	],

	computed: {
		height: function () {
			var l = _(this.datapoints)
				.pluck('region')
				.uniq()
				.value()
				.length;
			var h = 12;

			console.debug('stacked-region-bar::height', l, h);

			return l * h;
		},

		query: function () {
			return {
				indicator__in: _.map(this.indicators, function (d) {
					return d.id || d;
				}),
				campaign__in     : [this.campaign.id],
				parent_region__in: [this.region],
				level            : 'province'
			};
		},

		renderer: function () {
			var x         = this.xScale;
			var y         = this.yScale;
			var color     = this.colorScale;

			var renderer = stackedBar()
				.height(y.rangeBand())
				.width(function (d) {
					return x(d.y);
				})
				.x(function (d) {
					return x(d.y0);
				})
				.y(function (d) {
					return y(d.region);
				})
				.color(function (d, i) {
					return color(d.indicator);
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

			var campaign = this.campaign;

			var series = _(this.datapoints)
				.groupBy('indicator')
				.map(function (d, indicator) {
					return {
						id    : indicator,
						name  : indicator,
						values: d
					};
				})
				.value();

			var stack = d3.layout.stack()
				.offset('zero')
				.values(function (d) {
					return d.values;
				})
				.x(function (d) {
					return d.region;
				})
				.y(function (d) {
					return d.value;
				});

			return stack(series);
		},

		xScale: function () {
			function x(d) {
				return d.y0 + d.y;
			}

			var scale = d3.scale.linear()
				.range([0, this.contentWidth]);

			if (!this.empty) {
				var flat = _.flatten(_.pluck(this.series, 'values'), true);

				scale.domain([
					Math.min(0, d3.min(flat, x)),
					d3.max(flat, x)
				]);
			}

			return scale;
		},

		yScale: function () {
			var domain = _(this.datapoints)
				.pluck('region')
				.uniq()
				.value();

			return d3.scale.ordinal()
				.domain(domain)
				.rangeRoundBands([this.contentHeight, 0], 0.08)
		}
	}
};
