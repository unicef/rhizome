'use strict';

var d3 = require('d3');

module.exports = {
	created: function () {
		this.$on('hook:drawn', function () {
			console.log('yGrid.draw');

			var svg = d3.select(this.$el);
			var g   = svg.select('.y.axis');

			if (g.size() === 0) {
				g = svg.insert('g', ':first-child')
					.attr('class', 'y axis');
			}

			var yAxis = d3.svg.axis()
				.scale(this.$options.y)
				.ticks(3)
				.orient('right')
				.tickSize(this.width);

			g.call(yAxis);

			svg.selectAll('.y.axis text')
				.attr('x', 3)
				.attr('dy', -3);
		});
	}
};
