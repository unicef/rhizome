'use strict';

var d3 = require('d3');

module.exports = {
	attached: function () {
		d3.select(this.$el).append('g').attr('class', 'x axis');
	},

	created: function () {
		this.$on('hook:drawn', function () {
			console.log('xAxis.draw');

			var svg = d3.select(this.$el);
			var g   = svg.select('.x.axis');

			if (g.size() === 0) {
				g = svg.insert('g', ':first-child')
					.attr('class', 'x axis');

				g = svg.select('.x.axis');
			}

			g.attr('transform', 'translate(0,' + this.height + ')');

			var xAxis = d3.svg.axis()
				.scale(this.$options.x)
				.ticks(3)
				.orient('bottom');

			g.call(xAxis);
		});
	}
};
