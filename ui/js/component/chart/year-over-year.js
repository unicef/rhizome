'use strict';

var _         = require('lodash');

var lineChart = require('./line-chart');

module.exports = {

	mixins: [
		require('./line')
	],

	ready: function () {
		console.info('year-over-year::ready');
		console.debug(this);
	},

	computed: {

		renderer: function () {
			var x     = this.xScale;
			var y     = this.yScale;
			var color = this.colorScale;

			var renderer = lineChart()
				.x(function (d) {
					return x(d.campaign.start_date.getMonth());
				})
				.y(function (d) {
					return y(d.value)
				})
				.color(function (d, i) {
					return color(i);
				});

			return renderer;
		},

		series: function () {
			console.info('year-over-year::series enter');

			if (this.empty) {
				console.info('year-over-year::series empty');
				return [];
			}

			var series = _.values(_.groupBy(this.datapoints, function (d) {
				return d.campaign.start_date.getFullYear();
			}));

			console.debug('year-over-year::series', series);
			console.info('year-over-year::series exit');
			return series;
		},

		xScale: function () {
			var scale = d3.scale.linear()
				.domain([0, 11])
				.range([0, this.contentWidth]);

			return scale;
		}

	}

};
