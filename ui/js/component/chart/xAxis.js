'use strict';

var d3 = require('d3');

var DEFAULT_TICKS = 3;

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
				.orient('bottom');

			if (this.tickValues) {
				xAxis.tickValues(this.tickValues(this.x.domain()));
			} else {
				xAxis.ticks(this.ticks || DEFAULT_TICKS);
			}

			if (this.xFmt) {
				xAxis.tickFormat(this.xFmt);
			}

			g.call(xAxis);

			var domain = this.x.domain();

			// Align tick labels to the edges of the chart if they are on the
			// boundaries of the domain
			g.selectAll('.tick').each(function (d) {
				console.log(domain, d);
				if (d === domain[0]) {
					d3.select(this).selectAll('text').style('text-anchor', 'start');
				} else if (d === domain[domain.length - 1]) {
					d3.select(this).selectAll('text').style('text-anchor', 'end');
				}
			});
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
