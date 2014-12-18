'use strict';

var d3 = require('d3');

function getAnnotationLayer(el) {
	var svg = d3.select(el).selectAll('.annotations').data([0]);

	svg.enter().append('g').attr('class', 'annotations');

	return svg;
}

module.exports = {
	attached: function () {

		this.$on('show-annotation', function (d) {
			var svg  = getAnnotationLayer(this.$el);
			var line = svg.selectAll('.hover-line').data([d]);
			var x    = this.x(d.x);
			var y    = this.y.range();

			line.enter().append('line')
				.attr('class', 'hover-line');

			line.attr('x1', x)
				.attr('y1', y[0])
				.attr('x2', x)
				.attr('y2', y[1]);
		});

		this.$on('hide-annotation', function (d) {
			var svg = getAnnotationLayer(this.$el);

			svg.selectAll('.hover-line')
				.filter(function (l) { return l.x === d.x; })
				.remove();
		});

	}
};
