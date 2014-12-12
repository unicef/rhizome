'use strict';

var d3 = require('d3');

module.exports = {
	created: function () {
		this.$on('hook:drawn', function () {
			var svg = d3.select(this.$el);
			var g   = svg.selectAll('.x.axis').data([0]);

			g.enter().insert('g', ':first-child')
				.attr('class', 'x axis');

			g.attr('transform', 'translate(0,' + this.height + ')');

			var xAxis = d3.svg.axis()
				.scale(this.x)
				.ticks(3)
				.orient('bottom');

			if (this.xFmt) {
				xAxis.tickFormat(this.xFmt);
			}

			g.call(xAxis);
		});

		this.$on('show-annotation', function (d) {
			var axis = d3.select(this.$el).select('.x.axis');

			axis.selectAll('.tick')
				.transition().duration(300)
				.style('opacity', 0);

			axis.append('text')
				.attr({
					'class'      : 'annotation',
					'text-anchor': 'middle',
					'x'          : this.x(d.x),
					'y'          : '9',
					'dy'         : '.71em'
				})
				.text(this.xFmt ? this.xFmt(d.x) : d.x)
				.style('opacity', '0')
				.transition().duration(300)
				.style('opacity', '1');
		});

		this.$on('hide-annotation', function () {
			var axis = d3.select(this.$el).select('.x.axis');

			axis.selectAll('.tick')
				.transition().duration(300)
				.style('opacity', 1);

			axis.selectAll('.annotation')
				.transition().duration(300)
				.style('opacity', '0')
				.remove();
		});
	}
};
