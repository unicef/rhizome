'use strict';

var _     = require('lodash');
var d3    = require('d3');

var color = require('util/color');

module.exports = {

	mixins : [
		require('./bar')
	],

	methods : {

		draw : function () {
			var svg = d3.select(this.$el);

			// d3.layout.stack stacks the y-value, but we want to stack the x value,
			// so we swap x and y in the layout definition.
			var stack = d3.layout.stack()
				.values(function (d) {
					return d.values;
				})
				.offset('zero')
				.order('default')
				.x(function (d) {
					return d.y;
				})
				.y(function (d) {
					return d.x;
				})
				.out(function (d, y0, y) {
					d.x0 = y0;
					d.x  = y;
				});

			var data = stack(this.series);

			var xScale = d3.scale.linear()
				.range([0, this.contentWidth])
				.domain([0, d3.max(_(data).pluck('values').flatten().value(), function (d) {
					return d.x0 + d.x;
				})]);

			var x = function (d) {
				return xScale(d.x0);
			};

			var width = function (d) {
				return xScale(d.x);
			};

			var yScale = d3.scale.ordinal()
				.domain(this.categories)
				.rangePoints([this.contentHeight, 0]);

			var y = function (d) {
				return yScale(d.y);
			};

			var series = svg.select('.data')
				.selectAll('.series')
				.data(data, function (d) {
					return d.name;
				});

			var height = this.barHeight;

			series.enter().append('g').attr({
				'class'     : 'series',
				'transform' : 'translate(0,' + (-height / 2) + ')'
			});

			var colorScale = color.scale(_.pluck(data, 'name'));

			series.each(function (datum) {
				var g = d3.select(this);

				var bar = g.selectAll('.bar')
					.data(datum.values);

				bar.enter()
					.append('rect')
					.attr({
						'class'  : 'bar',
						'x'      : x,
						'y'      : y,
						'height' : height,
						'width'  : 0,
						'fill'   : colorScale(datum.name)
					});

				bar.transition()
					.duration(300)
					.attr({
						'x'      : x,
						'y'      : y,
						'height' : height,
						'width'  : width
					});

				bar.exit()
					.transition()
					.duration(300)
					.attr('width', 0)
					.remove();
			});

			var xAxis = d3.svg.axis()
				.scale(xScale)
				.orient('bottom');

			svg.select('.x.axis')
				.call(xAxis);

			var yAxis = d3.svg.axis()
				.scale(yScale)
				.tickSize(0)
				.orient('left');

			svg.select('.y.axis')
				.call(yAxis);
		}

	}

};
