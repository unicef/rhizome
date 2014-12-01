'use strict';

var _  = require('lodash');
var d3 = require('d3');

module.exports = {
	data: function () {
		return {
			lines : [],
			areas : [],
			width : 100,
			height: 100
		};
	},

	methods: {
		draw: function () {
			var svg = d3.select(this.$el);

			var data = _.reduce(this.lines, function (result, d) {
				return result.concat(d);
			}, []).concat(_.reduce(this.areas, function (result, d) {
				return result.concat(d);
			}, []));

			var x = d3.scale.linear()
				.domain(d3.extent(data, function (d) { return d.x; }))
				.range([0, this.width]);

			var y = d3.scale.linear()
				.domain([0, d3.max(data, function (d) { return d.y; })])
				.range([this.height, 0]);

			var line = d3.svg.line()
				.x(function (d) { return x(d.x); })
				.y(function (d) { return y(d.y); });

			var paths = svg.select('.lines').selectAll('.line')
				.data(this.lines);

			paths.enter().append('path')
				.attr('class', 'line');

			paths.style('stroke', function (d) { return d.color; })
				.transition().duration(300)
				.attr('d', function (d) { return line(d); });

			paths.exit().remove();

			var area = d3.svg.area()
				.x(function (d) { return x(d.x); })
				.y0(this.height)
				.y1(function (d) { return y(d.y); });

			paths = svg.select('.areas').selectAll('.area')
				.data(this.areas);

			paths.enter().append('path')
				.attr('class', 'area');

			paths.transition().duration(300)
				.attr('d', function (d) { return area(d); });

			paths.exit().remove();

			var axis = d3.svg.axis()
				.scale(x)
				.tickSize(0)
				.orient('bottom');

			svg.select('.x.axis').call(axis);

			axis = d3.svg.axis()
				.scale(y)
				.tickSize(this.width)
				.ticks(3)
				.orient('right');

			svg.select('.y.axis').call(axis);
			svg.select('.y.axis').selectAll('text')
				.attr('x', 0)
				.attr('dy', '-.2em');
		}
	},

	on: {
		'hook:attached'  : 'draw',
	},

	watch: {
		lines : 'draw',
		areas : 'draw',
		width : 'draw',
		height: 'draw'
	}
};
