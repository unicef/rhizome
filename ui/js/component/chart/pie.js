/**
 * @module component/chart/pie
 */
'use strict';

var d3 = require('d3');

module.exports = {
	paramAttributes: [
		'data-slices',
		'data-inner-radius',
		'data-outer-radius'
	],

	data: function () {
		return {
			slices     : [],
			innerRadius: 0,
			outerRadius: 100,
		};
	},

	methods: {
		draw: function () {
			var svg = d3.select(this.$el);

			var pie = d3.layout.pie()
				.value(function (d) { return d.value; });

			var arc = d3.svg.arc()
				.innerRadius(this.innerRadius)
				.outerRadius(this.outerRadius);

			var slice = svg.selectAll('.slice')
				.data(pie(this.slices));

			slice.enter().append('path')
				.attr({
					'class': 'slice'
				});

			slice.attr({
				d: arc
			}).style({
				fill: function (d) { return d.data.color; }
			});

			slice.exit().remove();
		}
	},

	on: {
		'hook:attached': 'draw'
	},

	watch: {
		'innerRadius': 'draw',
		'outerRadius': 'draw',
		'slices': 'draw'
	}
};
