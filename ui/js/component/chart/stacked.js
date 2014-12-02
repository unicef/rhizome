'use strict';

var _  = require('lodash');
var d3 = require('d3');

module.exports = {
	data: function () {
		return {
			layers: [],
			width : 100,
			height: 100
		};
	},

	methods: {
		draw: function () {
			var svg = d3.select(this.$el);

			var stack = d3.layout.stack()
				.values(function (d) { return d.values; })
				.x(function (d) { return d.x; })
				.y(function (d) { return d.y; });

			var layers = stack(this.layers);

			var chained = _.reduce(layers, function (result, layer) {
				return result.concat(layer.values);
			}, []);

			var area = d3.svg.area()
				.x(function (d) { return x(d.x); })
				.y0(function (d) { return y(d.y0); })
				.y1(function (d) { return y(d.y0 + d.y); });

			var x = d3.scale.linear()
				.domain(d3.extent(chained, function (d) { return d.x; }))
				.range([0, this.width]);

			var y = d3.scale.linear()
				.domain([0, d3.max(chained, function (d) { return d.y0 + d.y; })])
				.range([this.height, 0]);

			var paths = svg.select('.layers').selectAll('.layer')
				.data(layers);

			paths.enter().append('path')
				.attr('class', 'layer');

			paths.style('fill', function (d) { return d.color; })
				.attr('d', function (d) { return area(d.values); });

			paths.exit().remove();

			// FIXME: Copied and pasted from line.js. Bad form!

			// Draw axes

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
		'hook:attached': 'draw'
	},

	watch: {
		'layers': 'draw',
		'width' : 'draw',
		'height': 'draw'
	}
};
