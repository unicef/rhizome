/**
 * @module component/chart/pie
 */
'use strict';

var d3 = require('d3');

module.exports = {
	replace : true,

	data: function () {
		return {
			slices: [],
			radius: {
				inner: 0,
				outer: 100,
			}
		};
	},

	ready: function () {
		this.$watch('radius', this.draw, true);
	},

	methods: {
		draw: function () {
			var svg = d3.select(this.$el);

			var arc = d3.svg.arc()
				.innerRadius(this.radius.inner)
				.outerRadius(this.radius.outer);

			var pie = d3.layout.pie()
				.value(function (d) { return d.value; });

			var paths = svg.select('.pie').selectAll('.arc')
				.data(pie(this.slices));

			paths.enter().append('path')
				.attr('class', 'arc');

			paths.attr({
				d   : arc,
				fill: function (d) { return d.data.color; }
			});
		}
	},

	on: {
		'hook:attached': 'draw'
	},

	watch: {
		slices  : 'draw'
	}
};
