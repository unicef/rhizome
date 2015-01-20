'use strict';

var d3 = require('d3');

module.exports = {
	events: {

		'show-annotation': function (d) {
			var svg  = d3.select(this.$el).selectAll('.annotations').data([0]);
			var line = svg.selectAll('.hover-line').data([d]);
			var x    = this.x(d.x);
			var y    = this.y.range();

			line.enter().append('line')
				.attr('class', 'hover-line');

			line.attr('x1', x)
				.attr('y1', y[0])
				.attr('x2', x)
				.attr('y2', y[1]);
		},

		'hide-annotation': function (d) {
			var svg = d3.select(this.$el).selectAll('.annotations').data([0]);

			svg.selectAll('.hover-line')
				.filter(function (l) { return l.x === d.x; })
				.remove();
		}

	}
};
