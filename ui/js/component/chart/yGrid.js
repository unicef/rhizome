'use strict';

var d3 = require('d3');

module.exports = {
	created: function () {
		this.$on('hook:drawn', function () {
			var svg = d3.select(this.$el);
			var g   = svg.select('.y.axis');

			if (g.size() === 0) {
				g = svg.insert('g', ':first-child')
					.attr('class', 'y axis');
			}

			var yAxis = d3.svg.axis()
				.scale(this.y)
				.ticks(3)
				.orient('right')
				.tickSize(this.width || 0);

			if (this.yFmt) {
				yAxis.tickFormat(this.yFmt);
			}

			g.call(yAxis);

			svg.selectAll('.y.axis text')
				.attr('x', 3)
				.attr('dy', -3);
		});
	}
};
