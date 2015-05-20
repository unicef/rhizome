/**
 * @module component/chart/pie
 */
'use strict';

var _      = require('lodash');
var d3     = require('d3');
var moment = require('moment');

var colors = require('colors');

module.exports = {
	replace : true,
	template: require('./pie.html'),

	paramAttributes: [
		'data-inner-radius',
		'data-width',
		'data-height'
	],

	mixins: [
		require('./mixin/margin'),
		require('./mixin/with-indicator')
	],

	data: function () {
		return {
			innerRadius : 0,
			domain      : [0, 1]
		};
	},

	computed: {

		colorScale: function () {
			var series = this.series;

			var interpolate = d3.interpolate(
				d3.rgb(colors[0]),
				d3.rgb(colors[colors.length - 1]));

			var scale = d3.scale.linear().domain([0, series.length - 1]);

			// Build up a range of colors for the ordinal scale by interpolating the
			// two extremes of the colors from the coolgray array
			var range = [];
			for (var i = 0, l = series.length; i < l; i++) {
				range.push(interpolate(scale(i)));
			}

			return d3.scale.ordinal()
				.domain(_.map(this.series, function (d) {
					return d.indicator;
				}))
				.range(range);
		},

		query: function () {
			return {
				indicator__in : _.map(this.indicators, function (d) {
					return d.id || d;
				}),
				region__in    : [this.region.id],
				campaign_start: moment(this.campaign.start_date).format('YYYY-MM-DD'),
				campaign_end  : moment(this.campaign.end_date).format('YYYY-MM-DD')
			};
		},

		series: function () {
			if (this.empty) {
				return [];
			}

			var scale = d3.scale.linear()
				.domain(this.domain)
				.range([0, 2 * Math.PI]);

			// Use d3's stack layout instead of the pie layout so that we can control
			// the domain
			var layout = d3.layout.stack()
				.values(function (d) {
					return [d];
				})
				.x(function (d, i) {
					return i;
				})
				.y(function (d) {
					return d.value;
				})
				.out(function (d, y0, y) {
					d.startAngle = scale(y0);
					d.endAngle   = scale(y);
				});

			return layout(this.datapoints);
		}

	},

	methods: {

		draw: function () {
			var colorScale = this.colorScale;
			var color      = function (d) {
				return colorScale(d.indicator);
			};

			var svg = d3.select(this.$el);

			var arc = d3.svg.arc()
				.innerRadius(Number(this.innerRadius))
				.outerRadius(this.contentWidth / 2);

			svg.select('.bg')
				.datum({
					startAngle : 0,
					endAngle   : 2 * Math.PI
				})
				.attr('d', arc);

			var slice = svg.select('.data').selectAll('.slice').data(this.series);

			slice.transition()
				.duration(500)
					.attr('fill', color);

			slice.enter()
				.append('path')
					.attr({
						'class': 'slice',
						'fill': color
					});

			slice.attr('d', arc);

			slice.exit()
				.transition().duration(500)
					.style('opacity', 0)
				.remove();
		}

	},

	watch: {
		'datapoints'  : 'draw',
		'innerRadius' : 'draw',
		'outerRadius' : 'draw',
		'domain'      : 'draw'
	}
};
