/**
 * @module component/chart/pie
 */
'use strict';

var _      = require('lodash');
var d3     = require('d3');

var colors = require('colors/coolgray');

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
			innerRadius: 0
		};
	},

	computed: {

		colorScale: function () {
			return d3.scale.ordinal()
				.domain(d3.range(colors.length))
				.range(colors);
		},

		query: function () {
			return {
				indicator__in : _.map(this.indicators, function (d) {
					return d.id || d;
				}),
				region__in    : [this.region],
				campaign_start: this.campaign.end,
				campaign_end  : this.campaign.end
			};
		},

		series: function () {
			if (this.empty) {
				return [];
			}

			var layout = d3.layout.pie()
				.value(function (d) {
					return d.value;
				})
				.sort(function (a, b) {
					if (a.indicator === 'other') {
						return 1;
					}

					if (b.indicator === 'other') {
						return -1;
					}

					return d3.descending(a.value, b.value);
				});

			var total = _.reduce(this.datapoints, function (result, d) {
				return result + d.value;
			}, 0);

			// Assume that if the total value of the pie chart is < 1, it's meant to
			// show a percentage out of 100 and fill in the missing piece.
			var data = (total < 1) ?
				[{ value: 1 - total, indicator: 'other' }].concat(this.datapoints) :
				this.datapoints;

			return layout(data);
		}

	},

	methods: {

		draw: function () {
			var colorScale = this.colorScale;
			var color      = function (d, i) {
				return colorScale(i);
			};

			var svg = d3.select(this.$el);

			var arc = d3.svg.arc()
				.innerRadius(this.innerRadius)
				.outerRadius(this.contentWidth / 2);

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

			slice.transition()
				.duration(500)
					.attr('d', arc);

			slice.exit()
				.transition().duration(500)
					.style('opacity', 0)
				.remove();
		}

	},

	watch: {
		'datapoints' : 'draw',
		'innerRadius': 'draw',
		'outerRadius': 'draw'
	}
};
